"""Tests for Compliance Guard, Audit Trail, and Hinglish Messaging."""
from app.agents.compliance_guard import ComplianceGuard
from app.agents.message_agent import MessageAgent
from app.services.audit_service import AuditService


def test_compliance_stopping_rules():
    guard = ComplianceGuard()
    
    # 1. Max attempts stopping rule
    res = guard.evaluate(
        payment_id="pay_test_01",
        amount=1000.0,
        status="failed",
        recovery_status=None,
        attempt_count=3,
        recovery_probability=0.85
    )
    assert res.allowed is False
    assert res.rule_name == "MAX_ATTEMPTS_EXCEEDED_STOP"

    # 2. Low probability floor stopping rule (< 20%)
    res2 = guard.evaluate(
        payment_id="pay_test_02",
        amount=1000.0,
        status="failed",
        recovery_status=None,
        attempt_count=0,
        recovery_probability=0.12
    )
    assert res2.allowed is False
    assert res2.rule_name == "LOW_PROBABILITY_FLOOR_STOP"

    # 3. Already recovered stopping rule
    res3 = guard.evaluate(
        payment_id="pay_test_03",
        amount=1000.0,
        status="captured",
        recovery_status="recovered",
        attempt_count=0,
        recovery_probability=0.90
    )
    assert res3.allowed is False
    assert res3.rule_name == "ALREADY_RECOVERED_STOP"


def test_hinglish_messaging():
    agent = MessageAgent()
    msg = agent.generate_message(
        customer_name="Rahul",
        amount=2499.0,
        currency="INR",
        failure_reason_display="NETWORK_FAILURE",
        recommended_action="RETRY_NOW",
        payment_link="https://razorpay.me/pay/pay_123",
        language="hinglish"
    )
    assert "Rahul" in msg
    assert "2,499" in msg
    assert "https://razorpay.me/pay/pay_123" in msg
    assert ("Namaste" in msg or "Hi" in msg or "payment" in msg)


def test_audit_logging(test_db):
    service = AuditService(test_db)
    log = service.log_event(
        payment_id="pay_test_audit",
        customer_id="cust_test_audit",
        action="ANALYZED",
        component="RECOVERY_AGENT",
        recovery_probability=0.75,
        rule_applied="RETRY_NOW",
        compliance_passed=True,
        details="Test audit entry"
    )
    assert log.id is not None
    assert log.payment_id == "pay_test_audit"

    logs = service.get_logs(payment_id="pay_test_audit")
    assert len(logs) == 1
    assert logs[0].action == "ANALYZED"
