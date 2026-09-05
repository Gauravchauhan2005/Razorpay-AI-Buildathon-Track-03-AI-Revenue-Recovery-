"""Audit Trail Logging Service."""
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from app.models.audit import AuditLog


class AuditService:
    """Records and retrieves immutable audit trails for compliance."""

    def __init__(self, db: Session):
        self.db = db

    def log_event(
        self,
        payment_id: str,
        action: str,
        component: str,
        customer_id: Optional[str] = None,
        recovery_probability: Optional[float] = None,
        rule_applied: Optional[str] = None,
        compliance_passed: bool = True,
        details: Optional[str] = None,
    ) -> AuditLog:
        """Appends an immutable audit event."""
        log = AuditLog(
            payment_id=payment_id,
            customer_id=customer_id,
            action=action,
            component=component,
            recovery_probability=recovery_probability,
            rule_applied=rule_applied,
            compliance_passed=compliance_passed,
            details=details,
            created_at=datetime.utcnow()
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_logs(
        self,
        payment_id: Optional[str] = None,
        action: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Retrieves audit trail with filtering and pagination."""
        query = self.db.query(AuditLog)
        if payment_id:
            query = query.filter(AuditLog.payment_id == payment_id)
        if action:
            query = query.filter(AuditLog.action == action)
        return query.order_by(AuditLog.id.desc()).offset(skip).limit(limit).all()

    def get_log_count(self) -> int:
        """Returns total audit events count."""
        return self.db.query(AuditLog).count()
