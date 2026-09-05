from fastapi import APIRouter, Request, Header, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import json
from app.database.database import get_db
from app.core.config import settings
from app.core.security import verify_webhook_signature
from app.models.event import Event
from app.models.customer import Customer
from app.services.payment_service import PaymentService
from app.services.recovery_service import RecoveryService
from app.agents.recovery_agent import RecoveryAgent
from datetime import datetime

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

def process_recovery_task(payment_data: dict, customer_data: dict, db: Session):
    agent = RecoveryAgent()
    decision = agent.process_failed_payment(payment_data, customer_data)
    # Just processing for now

@router.post("/razorpay")
async def razorpay_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_razorpay_signature: str | None = Header(None),
    db: Session = Depends(get_db)
):
    body = await request.body()
    
    if settings.razorpay_webhook_secret and x_razorpay_signature:
        if not verify_webhook_signature(body, x_razorpay_signature, settings.razorpay_webhook_secret):
            raise HTTPException(status_code=400, detail="Invalid signature")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # This assumes standard razorpay webhook format (often contained in x-razorpay-event-id header, or inside payload)
    event_id = request.headers.get("x-razorpay-event-id", "mock-" + str(datetime.now().timestamp()))
    event_type = payload.get("event")

    existing_event = db.query(Event).filter(Event.event_id == event_id).first()
    if existing_event:
        return {"status": "ok"}

    payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
    payment_id = payment_entity.get("id")

    event = Event(
        event_id=event_id,
        event_type=event_type,
        payment_id=payment_id,
        payload=json.dumps(payload),
        received_at=datetime.utcnow(),
        processing_status="received"
    )
    db.add(event)
    db.commit()

    if event_type == "payment.failed":
        payment_service = PaymentService(db)
        customer_id = payment_entity.get("customer_id", f"cust_{payment_id}")
        
        customer_data = {
            "customer_id": customer_id,
            "email": payment_entity.get("email"),
            "phone": payment_entity.get("contact"),
        }
        
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            customer = Customer(**customer_data)
            db.add(customer)
            db.commit()

        payment_data = {
            "payment_id": payment_id,
            "order_id": payment_entity.get("order_id"),
            "customer_id": customer_id,
            "amount": payment_entity.get("amount") / 100 if payment_entity.get("amount") else 0, # Assuming paisa
            "currency": payment_entity.get("currency"),
            "method": payment_entity.get("method"),
            "status": "failed",
            "failure_reason": payment_entity.get("error_description"),
        }
        
        existing_payment = payment_service.get_payment(payment_id)
        if existing_payment:
            payment_service.update_payment_status(payment_id, "failed", failure_reason=payment_data["failure_reason"])
        else:
            payment_service.create_payment(payment_data)

        # Trigger background recovery task
        background_tasks.add_task(process_recovery_task, payment_data, customer_data, db)

    elif event_type == "payment.captured":
        payment_service = PaymentService(db)
        recovery_service = RecoveryService(db)
        
        existing_payment = payment_service.get_payment(payment_id)
        if existing_payment:
            payment_service.update_payment_status(payment_id, "captured", recovery_status="recovered")
            recovery_service.cancel_pending_attempts(payment_id)

    event.processed_at = datetime.utcnow()
    event.processing_status = "processed"
    db.commit()

    return {"status": "ok"}
