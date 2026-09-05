from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from app.database.database import get_db
from app.services.recovery_service import RecoveryService
from app.services.payment_service import PaymentService
from app.services.notification_service import NotificationService
from app.services.audit_service import AuditService
from app.services.ptp_service import PTPService
from app.agents.recovery_agent import RecoveryAgent
from app.agents.strategy_agent import RecoveryDecision
from app.utils.validators import RecoveryAttemptResponse
from app.models.customer import Customer
from app.models.ptp import PromiseToPay

router = APIRouter(prefix="/recovery", tags=["Recovery"])


class PTPRequest(BaseModel):
    promised_hours_delay: int = 4  # e.g., will pay in 4 hours


@router.get("", response_model=list[RecoveryAttemptResponse])
@router.get("/", response_model=list[RecoveryAttemptResponse], include_in_schema=False)
def get_all_attempts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = RecoveryService(db)
    return service.get_all_attempts(skip=skip, limit=limit)


@router.get("/{payment_id}", response_model=list[RecoveryAttemptResponse])
def get_payment_attempts(payment_id: str, db: Session = Depends(get_db)):
    service = RecoveryService(db)
    return service.get_recovery_attempts(payment_id)


def _get_agent_context(payment_id: str, db: Session):
    payment = PaymentService(db).get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
        
    customer = db.query(Customer).filter(Customer.customer_id == payment.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    recovery_service = RecoveryService(db)
    attempt_count = recovery_service.get_attempt_count(payment_id)

    payment_data = {
        "payment_id": payment.payment_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "method": payment.method,
        "failure_reason": payment.failure_reason,
        "status": payment.status,
        "recovery_status": payment.recovery_status,
        "attempt_number": attempt_count,
        "payment_link": f"https://razorpay.me/pay/{payment.payment_id}",
    }
    customer_data = {
        "customer_id": customer.customer_id,
        "name": customer.customer_id.replace("_", " ").title(),
        "email": customer.email,
        "phone": customer.phone,
        "segment": customer.segment,
        "preferred_channel": customer.preferred_channel,
        "total_transactions": customer.total_transactions,
        "successful_transactions": customer.successful_transactions,
        "previous_success_rate": (
            customer.successful_transactions / customer.total_transactions
            if customer.total_transactions > 0 else 0.5
        ),
    }
    return payment, customer, payment_data, customer_data, attempt_count


@router.post("/agent/analyze/{payment_id}")
def analyze_payment(
    payment_id: str, 
    language: str = Query("english", pattern="^(english|hinglish|hindi)$"),
    db: Session = Depends(get_db)
):
    payment, customer, payment_data, customer_data, _ = _get_agent_context(payment_id, db)
    agent = RecoveryAgent()
    decision = agent.process_failed_payment(payment_data, customer_data, language=language)

    # Save calculated probability to payment record
    payment.recovery_probability = decision.recovery_probability
    db.commit()

    # Log to Audit Trail
    audit_service = AuditService(db)
    audit_service.log_event(
        payment_id=payment_id,
        customer_id=customer.customer_id,
        action="ANALYZED",
        component="RECOVERY_AGENT",
        recovery_probability=decision.recovery_probability,
        rule_applied=decision.reason,
        compliance_passed=not decision.should_stop,
        details=f"Action: {decision.recommended_action.value}, Priority: {decision.priority}, Channel: {decision.channel}, Language: {language}"
    )

    res = decision.model_dump()
    res["probability"] = decision.recovery_probability
    res["action"] = decision.recommended_action.value
    res["language"] = language
    return res


@router.post("/agent/recover/{payment_id}")
@router.post("/{payment_id}/retry")
def recover_payment(
    payment_id: str, 
    language: str = Query("english", pattern="^(english|hinglish|hindi)$"),
    db: Session = Depends(get_db)
):
    payment, customer, payment_data, customer_data, attempt_count = _get_agent_context(payment_id, db)
    
    agent = RecoveryAgent()
    decision = agent.process_failed_payment(payment_data, customer_data, language=language)
    
    notification_service = NotificationService()
    recovery_service = RecoveryService(db)
    audit_service = AuditService(db)

    # Execute recovery action if not stopped
    notification_result = None
    if not decision.should_stop and decision.recommended_action.value != "NO_ACTION":
        # Dispatch notification
        notification_result = notification_service.send(
            channel=decision.channel,
            customer=customer_data,
            message=decision.message or f"Please retry your payment: {payment_data['payment_link']}"
        )
        
        # Record attempt
        attempt = recovery_service.create_recovery_attempt(
            payment_id=payment.payment_id,
            customer_id=customer.customer_id,
            attempt_number=attempt_count + 1,
            channel=decision.channel,
            strategy=decision.recommended_action.value,
            message=decision.message or "",
            scheduled_at=datetime.utcnow()
        )
        
        payment.recovery_status = "contacted"
        payment.recovery_probability = decision.recovery_probability
        db.commit()

        # Record in Audit Trail
        audit_service.log_event(
            payment_id=payment_id,
            customer_id=customer.customer_id,
            action="DISPATCHED",
            component="NOTIFICATION_SERVICE",
            recovery_probability=decision.recovery_probability,
            rule_applied=decision.recommended_action.value,
            compliance_passed=True,
            details=f"Dispatched via {decision.channel}. Attempt #{attempt.attempt_number}. Message: {decision.message[:80]}..."
        )

        return {
            "status": "recovery_executed",
            "payment_id": payment_id,
            "attempt_number": attempt.attempt_number,
            "channel": decision.channel,
            "action": decision.recommended_action.value,
            "message": decision.message,
            "probability": decision.recovery_probability,
            "notification": notification_result
        }
    else:
        new_status = "escalated" if decision.recommended_action.value == "ESCALATE_TO_HUMAN" else ("closed" if decision.should_stop else "not_recoverable")
        payment.recovery_status = new_status
        db.commit()

        audit_service.log_event(
            payment_id=payment_id,
            customer_id=customer.customer_id,
            action="STOPPED" if decision.should_stop else "ESCALATED",
            component="COMPLIANCE_GUARD",
            recovery_probability=decision.recovery_probability,
            rule_applied=decision.reason,
            compliance_passed=False,
            details=f"Action: {decision.recommended_action.value}, Reason: {decision.reason}"
        )

        return {
            "status": "recovery_stopped",
            "payment_id": payment_id,
            "reason": decision.reason,
            "action": decision.recommended_action.value,
            "probability": decision.recovery_probability
        }


@router.post("/{payment_id}/promise-to-pay")
def record_promise_to_pay(payment_id: str, req: PTPRequest, db: Session = Depends(get_db)):
    """Records customer Promise-to-Pay and reschedules recovery."""
    payment, customer, _, _, _ = _get_agent_context(payment_id, db)
    ptp_service = PTPService(db)
    audit_service = AuditService(db)

    promised_time = datetime.utcnow() + timedelta(hours=req.promised_hours_delay)
    ptp = ptp_service.record_promise(
        payment_id=payment.payment_id,
        customer_id=customer.customer_id,
        amount=payment.amount,
        promised_timestamp=promised_time
    )

    audit_service.log_event(
        payment_id=payment_id,
        customer_id=customer.customer_id,
        action="PTP_RECORDED",
        component="PTP_SERVICE",
        recovery_probability=payment.recovery_probability,
        rule_applied="PROMISE_TO_PAY_POLICY",
        compliance_passed=True,
        details=f"Customer promised payment after {req.promised_hours_delay} hours ({promised_time.isoformat()} UTC)."
    )

    return {
        "status": "promise_recorded",
        "payment_id": payment_id,
        "promised_amount": ptp.promised_amount,
        "promised_timestamp": ptp.promised_timestamp.isoformat(),
        "scheduled_nudge_delay_hours": req.promised_hours_delay
    }
