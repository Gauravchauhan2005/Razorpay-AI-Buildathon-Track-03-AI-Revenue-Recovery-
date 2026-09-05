"""Audit Log Model for Compliance & Audit Trail."""
from sqlalchemy import Integer, String, Text, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database.database import Base


class AuditLog(Base):
    """Immutable audit entry for every decision, rule check, and recovery action."""
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    payment_id: Mapped[str] = mapped_column(String, index=True)
    customer_id: Mapped[str | None] = mapped_column(String, nullable=True)
    action: Mapped[str] = mapped_column(String)  # e.g., ANALYZED, STOPPED, DISPATCHED, ESCALATED, RECOVERED
    component: Mapped[str] = mapped_column(String)  # e.g., FAILURE_ANALYZER, STRATEGY_ENGINE, COMPLIANCE_GUARD, MESSAGE_AGENT
    recovery_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    rule_applied: Mapped[str | None] = mapped_column(String, nullable=True)
    compliance_passed: Mapped[bool] = mapped_column(default=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON or text description
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
