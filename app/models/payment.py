"""Payment model."""
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.database import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.recovery import RecoveryAttempt

class Payment(Base):
    """Payment entity."""
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payment_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    order_id: Mapped[str | None] = mapped_column(String, nullable=True)
    customer_id: Mapped[str | None] = mapped_column(String, ForeignKey('customers.customer_id'), index=True)
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default='INR')
    method: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    failure_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    failure_category: Mapped[str | None] = mapped_column(String, nullable=True)
    recovery_status: Mapped[str | None] = mapped_column(String, nullable=True)
    recovery_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    device_type: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=datetime.utcnow, nullable=True)

    customer: Mapped["Customer"] = relationship("Customer", back_populates="payments")
    recovery_attempts: Mapped[List["RecoveryAttempt"]] = relationship("RecoveryAttempt", back_populates="payment")
