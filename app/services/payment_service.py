from sqlalchemy.orm import Session
from app.models.payment import Payment

class PaymentService:
    """Service for managing payments."""
    def __init__(self, db: Session):
        self.db = db
        
    def create_payment(self, payment_data: dict) -> Payment:
        payment = Payment(**payment_data)
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_payment(self, payment_id: str) -> Payment | None:
        return self.db.query(Payment).filter(Payment.payment_id == payment_id).first()

    def get_payments(self, skip: int = 0, limit: int = 100, status: str | None = None) -> list[Payment]:
        query = self.db.query(Payment)
        if status:
            query = query.filter(Payment.status == status)
        return query.offset(skip).limit(limit).all()

    def update_payment_status(self, payment_id: str, status: str, **kwargs) -> Payment | None:
        payment = self.get_payment(payment_id)
        if payment:
            payment.status = status
            for key, value in kwargs.items():
                setattr(payment, key, value)
            self.db.commit()
            self.db.refresh(payment)
        return payment

    def get_failed_payments(self, skip: int = 0, limit: int = 100) -> list[Payment]:
        return self.get_payments(skip, limit, status="failed")

    def get_payment_count(self, status: str | None = None) -> int:
        query = self.db.query(Payment)
        if status:
            query = query.filter(Payment.status == status)
        return query.count()
