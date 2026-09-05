"""RecoveryAttempt model."""
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.payment import Payment
    from app.models.customer import Customer

class RecoveryAttempt(Base):
    """Recovery attempt entity."""
    __tablename__ = "recovery_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payment_id: Mapped[str] = mapped_column(String, ForeignKey('payments.payment_id'), index=True)
    customer_id: Mapped[str] = mapped_column(String, ForeignKey('customers.customer_id'))
    attempt_number: Mapped[int] = mapped_column(Integer)
    channel: Mapped[str] = mapped_column(String)
    strategy: Mapped[str] = mapped_column(String)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    executed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String)
    result: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    payment: Mapped["Payment"] = relationship("Payment", back_populates="recovery_attempts")
    customer: Mapped["Customer"] = relationship("Customer")
