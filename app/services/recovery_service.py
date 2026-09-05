from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.recovery import RecoveryAttempt
from app.models.payment import Payment
from datetime import datetime

class RecoveryService:
    """Service for managing recovery attempts."""
    def __init__(self, db: Session):
        self.db = db

    def create_recovery_attempt(self, payment_id: str, customer_id: str, attempt_number: int, channel: str, strategy: str, message: str, scheduled_at: datetime | None = None) -> RecoveryAttempt:
        attempt = RecoveryAttempt(
            payment_id=payment_id,
            customer_id=customer_id,
            attempt_number=attempt_number,
            channel=channel,
            strategy=strategy,
            message=message,
            scheduled_at=scheduled_at,
            status="pending"
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def get_recovery_attempts(self, payment_id: str) -> list[RecoveryAttempt]:
        return self.db.query(RecoveryAttempt).filter(RecoveryAttempt.payment_id == payment_id).all()

    def get_attempt_count(self, payment_id: str) -> int:
        return self.db.query(RecoveryAttempt).filter(RecoveryAttempt.payment_id == payment_id).count()

    def update_attempt_status(self, attempt_id: int, status: str, result: str | None = None) -> RecoveryAttempt | None:
        attempt = self.db.query(RecoveryAttempt).filter(RecoveryAttempt.id == attempt_id).first()
        if attempt:
            attempt.status = status
            attempt.result = result
            self.db.commit()
            self.db.refresh(attempt)
        return attempt

    def get_all_attempts(self, skip: int = 0, limit: int = 100) -> list[RecoveryAttempt]:
        return self.db.query(RecoveryAttempt).offset(skip).limit(limit).all()

    def get_recovered_count(self) -> int:
        return self.db.query(Payment).filter(Payment.recovery_status == "recovered").count()

    def get_total_recovered_revenue(self, db: Session) -> float:
        result = db.query(func.sum(Payment.amount)).filter(Payment.recovery_status == "recovered").scalar()
        return float(result) if result else 0.0

    def cancel_pending_attempts(self, payment_id: str) -> int:
        count = self.db.query(RecoveryAttempt).filter(
            RecoveryAttempt.payment_id == payment_id,
            RecoveryAttempt.status == "pending"
        ).update({"status": "cancelled"})
        self.db.commit()
        return count
