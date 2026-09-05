"""Promise-to-Pay (PTP) Management Service."""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from app.models.ptp import PromiseToPay
from app.models.payment import Payment


class PTPService:
    """Manages customer commitments and scheduled recovery nudges."""

    def __init__(self, db: Session):
        self.db = db

    def record_promise(
        self,
        payment_id: str,
        customer_id: str,
        amount: float,
        promised_timestamp: datetime
    ) -> PromiseToPay:
        """Records a customer promise-to-pay timestamp and pauses active outreach."""
        ptp = self.db.query(PromiseToPay).filter(PromiseToPay.payment_id == payment_id).first()
        if not ptp:
            ptp = PromiseToPay(
                payment_id=payment_id,
                customer_id=customer_id,
                promised_amount=amount,
                promised_timestamp=promised_timestamp,
                status="pending",
                nudge_sent=False
            )
            self.db.add(ptp)
        else:
            ptp.promised_timestamp = promised_timestamp
            ptp.status = "pending"
            ptp.nudge_sent = False

        # Update payment recovery status
        payment = self.db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if payment:
            payment.recovery_status = "scheduled"

        self.db.commit()
        self.db.refresh(ptp)
        return ptp

    def get_active_promises(self) -> List[PromiseToPay]:
        """Lists pending promise commitments."""
        return self.db.query(PromiseToPay).filter(PromiseToPay.status == "pending").all()

    def get_due_nudges(self) -> List[PromiseToPay]:
        """Finds promises where the promised time has arrived and no nudge has been sent."""
        now = datetime.utcnow()
        return self.db.query(PromiseToPay).filter(
            PromiseToPay.status == "pending",
            PromiseToPay.promised_timestamp <= now,
            PromiseToPay.nudge_sent == False
        ).all()

    def mark_nudge_sent(self, payment_id: str) -> None:
        """Marks that the scheduled PTP reminder nudge was dispatched."""
        ptp = self.db.query(PromiseToPay).filter(PromiseToPay.payment_id == payment_id).first()
        if ptp:
            ptp.nudge_sent = True
            self.db.commit()

    def mark_fulfilled(self, payment_id: str) -> None:
        """Marks the promise as successfully honored when payment is captured."""
        ptp = self.db.query(PromiseToPay).filter(PromiseToPay.payment_id == payment_id).first()
        if ptp:
            ptp.status = "fulfilled"
            self.db.commit()
