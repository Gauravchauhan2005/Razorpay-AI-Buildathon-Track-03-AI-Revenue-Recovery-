"""Compliance & Bounded Stopping Rules Engine.
Enforces TRAI/RBI outreach limits, quiet hours, cooldown frequency caps, and stopping policies.
"""
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import Optional


class ComplianceCheckResult(BaseModel):
    allowed: bool
    reason: str
    rule_name: str
    escalate_to_human: bool = False
    schedule_delay_minutes: int = 0


class ComplianceGuard:
    """Evaluates regulatory, frequency, and stopping rules before executing recovery actions."""

    MAX_LIFETIME_ATTEMPTS = 3
    HIGH_VALUE_THRESHOLD_INR = 15000.0
    PROBABILITY_FLOOR = 0.20

    @staticmethod
    def get_ist_now() -> datetime:
        """Returns current time in Indian Standard Time (UTC+5:30)."""
        return datetime.now(timezone(timedelta(hours=5, minutes=30)))

    def evaluate(
        self,
        payment_id: str,
        amount: float,
        status: str,
        recovery_status: Optional[str],
        attempt_count: int,
        recovery_probability: float,
        last_attempt_time: Optional[datetime] = None,
        is_opted_out: bool = False,
        customer_segment: str = "new"
    ) -> ComplianceCheckResult:
        """Evaluates strict stopping and compliance policies."""
        
        # 1. Payment Already Succeeded / Closed Stopping Rule
        if status == "captured" or recovery_status == "recovered":
            return ComplianceCheckResult(
                allowed=False,
                reason="Payment is already captured and recovered. Outreach prohibited.",
                rule_name="ALREADY_RECOVERED_STOP"
            )

        # 2. Customer Opt-Out / DND Stopping Rule
        if is_opted_out:
            return ComplianceCheckResult(
                allowed=False,
                reason="Customer has opted out / registered on DND. Outreach prohibited.",
                rule_name="OPT_OUT_DND_STOP"
            )

        # 3. Maximum Lifetime Attempts Bounded Rule
        if attempt_count >= self.MAX_LIFETIME_ATTEMPTS:
            return ComplianceCheckResult(
                allowed=False,
                reason=f"Reached hard limit of {self.MAX_LIFETIME_ATTEMPTS} attempts. Ceasing automated retries.",
                rule_name="MAX_ATTEMPTS_EXCEEDED_STOP"
            )

        # 4. Low Probability Floor Stopping Rule
        if recovery_probability < self.PROBABILITY_FLOOR:
            return ComplianceCheckResult(
                allowed=False,
                reason=f"Recovery probability ({recovery_probability*100:.1f}%) is below recovery threshold ({self.PROBABILITY_FLOOR*100:.0f}%). Stopping intervention.",
                rule_name="LOW_PROBABILITY_FLOOR_STOP"
            )

        # 5. High-Value Escalation Rule
        if (amount >= self.HIGH_VALUE_THRESHOLD_INR or customer_segment == "high_value") and attempt_count >= 1:
            return ComplianceCheckResult(
                allowed=False,
                escalate_to_human=True,
                reason=f"High transaction value (₹{amount:,.0f}) requires high-touch relationship manager escalation.",
                rule_name="HIGH_VALUE_CONCIERGE_ESCALATION"
            )

        # 6. TRAI / RBI Quiet Hours Compliance (9 PM - 9 AM IST)
        ist_now = self.get_ist_now()
        current_hour = ist_now.hour
        if current_hour >= 21 or current_hour < 9:
            # Calculate delay until 09:15 AM IST
            target_time = ist_now.replace(hour=9, minute=15, second=0, microsecond=0)
            if current_hour >= 21:
                target_time += timedelta(days=1)
            delay_minutes = max(1, int((target_time - ist_now).total_seconds() / 60))
            
            return ComplianceCheckResult(
                allowed=False,
                schedule_delay_minutes=delay_minutes,
                reason=f"TRAI Quiet Hours Active ({current_hour:02d}:{ist_now.minute:02d} IST). Automated outreach rescheduled to 09:15 AM IST.",
                rule_name="QUIET_HOURS_RESCHEDULE"
            )

        # 7. Minimum Frequency Cooldown Cap (at least 30 mins between consecutive outreach)
        if last_attempt_time:
            time_since_last = (datetime.utcnow() - last_attempt_time).total_seconds() / 60
            if time_since_last < 30:
                delay = int(30 - time_since_last)
                return ComplianceCheckResult(
                    allowed=False,
                    schedule_delay_minutes=delay,
                    reason=f"Cooldown active ({int(time_since_last)}m since last outreach). Minimum gap is 30 minutes.",
                    rule_name="FREQUENCY_COOLDOWN_CAP"
                )

        # All policies passed
        return ComplianceCheckResult(
            allowed=True,
            reason="All compliance and stopping policies validated successfully.",
            rule_name="POLICY_PASSED"
        )
