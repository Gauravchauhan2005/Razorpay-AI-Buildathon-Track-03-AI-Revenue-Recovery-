from enum import Enum
from pydantic import BaseModel
from typing import Optional
from app.agents.failure_analyzer import FailureAnalysisResult, FailureCategory

class RecoveryAction(str, Enum):
    NO_ACTION = "NO_ACTION"
    RETRY_NOW = "RETRY_NOW"
    RETRY_LATER = "RETRY_LATER"
    SEND_REMINDER = "SEND_REMINDER"
    SEND_PAYMENT_LINK = "SEND_PAYMENT_LINK"
    CHANGE_CHANNEL = "CHANGE_CHANNEL"
    OFFER_ASSISTANCE = "OFFER_ASSISTANCE"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"

class RecoveryDecision(BaseModel):
    payment_id: str
    recovery_probability: float
    failure_category: str
    recommended_action: RecoveryAction
    channel: str
    priority: str
    attempt_number: int
    retry_after_minutes: int
    reason: str
    should_stop: bool
    message: Optional[str] = None

class StrategyAgent:
    """Determines the best strategy to recover a failed payment."""
    
    def decide(
        self, 
        payment_id: str, 
        failure_analysis: FailureAnalysisResult, 
        recovery_probability: float, 
        attempt_number: int, 
        customer_segment: str, 
        preferred_channel: str, 
        max_attempts: int = 3
    ) -> RecoveryDecision:
        """Determines the recovery decision based on rules."""
        
        should_stop = False
        action = RecoveryAction.NO_ACTION
        retry_after = 0
        reason = "No action determined."
        
        priority = "low"
        if recovery_probability >= 0.8:
            priority = "high"
        elif recovery_probability >= 0.5:
            priority = "medium"
            
        if customer_segment == "high_value":
            if priority == "low": priority = "medium"
            elif priority == "medium": priority = "high"
            elif priority == "high": priority = "critical"
            
        channel = preferred_channel if preferred_channel else "whatsapp"
        if channel not in ["whatsapp", "sms", "email"]:
            channel = "whatsapp"
            
        if attempt_number >= max_attempts:
            action = RecoveryAction.NO_ACTION
            should_stop = True
            reason = "Max recovery attempts reached."
        elif recovery_probability < 0.20:
            action = RecoveryAction.NO_ACTION
            reason = f"Low recovery probability ({recovery_probability:.2f})."
        elif recovery_probability >= 0.80 and attempt_number == 0 and failure_analysis.category in [FailureCategory.NETWORK_FAILURE, FailureCategory.TIMEOUT]:
            action = RecoveryAction.RETRY_NOW
            reason = f"High recovery probability ({recovery_probability*100:.0f}%) with temporary network failure. First attempt — immediate retry recommended."
        elif failure_analysis.category == FailureCategory.INSUFFICIENT_FUNDS:
            action = RecoveryAction.RETRY_LATER
            retry_after = 360
            reason = "Insufficient funds detected. Retrying later (6 hours)."
        elif failure_analysis.category in [FailureCategory.NETWORK_FAILURE, FailureCategory.TIMEOUT]:
            action = RecoveryAction.RETRY_LATER
            retry_after = 15
            reason = "Network or timeout issue. Retrying later (15 min)."
        elif customer_segment == "high_value" and recovery_probability >= 0.60:
            action = RecoveryAction.ESCALATE_TO_HUMAN
            reason = "High value customer with decent recovery probability. Escalating to human."
        elif recovery_probability >= 0.50:
            action = RecoveryAction.SEND_PAYMENT_LINK
            reason = "Good recovery probability. Sending payment link."
        elif recovery_probability >= 0.30:
            action = RecoveryAction.SEND_REMINDER
            reason = "Fair recovery probability. Sending reminder."
            
        return RecoveryDecision(
            payment_id=payment_id,
            recovery_probability=recovery_probability,
            failure_category=failure_analysis.category.value,
            recommended_action=action,
            channel=channel,
            priority=priority,
            attempt_number=attempt_number,
            retry_after_minutes=retry_after,
            reason=reason,
            should_stop=should_stop
        )
