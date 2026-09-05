import logging
from typing import Dict, Any, Optional
from app.agents.failure_analyzer import FailureAnalyzer
from app.agents.strategy_agent import StrategyAgent, RecoveryDecision, RecoveryAction
from app.agents.message_agent import MessageAgent
from app.agents.compliance_guard import ComplianceGuard
from app.ml.features import FeatureEngineer
from app.ml.predict import RecoveryPredictor
from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger("recovery_agent")


class RecoveryAgent:
    """Master orchestrator for autonomous payment recovery pipeline."""
    
    def __init__(self):
        self.analyzer = FailureAnalyzer()
        self.strategy = StrategyAgent()
        self.messenger = MessageAgent()
        self.engineer = FeatureEngineer()
        self.predictor = RecoveryPredictor()
        self.compliance = ComplianceGuard()
        
    def should_process(self, payment_data: dict) -> bool:
        """Checks if a payment is eligible for recovery intervention."""
        if payment_data.get("status") != "failed":
            return False
            
        attempts = payment_data.get("attempt_number", 0)
        if attempts >= getattr(settings, "max_recovery_attempts", 3):
            return False
            
        return True
        
    def process_failed_payment(
        self,
        payment_data: dict,
        customer_data: dict,
        language: str = "english"
    ) -> RecoveryDecision:
        """Processes a failed payment and determines the optimal, compliant recovery strategy."""
        payment_id = payment_data.get("payment_id", "unknown")
        logger.info(f"Processing failed payment {payment_id}")
        
        # 1. Failure Analysis
        failure_reason = payment_data.get("failure_reason", "")
        analysis = self.analyzer.analyze(failure_reason)
        logger.debug(f"Failure analysis: {analysis.category.value}")
        
        # 2. Feature Extraction & Machine Learning Prediction
        event_data = {**payment_data, **customer_data}
        features = self.engineer.extract_features(event_data)
        
        event_data.update(features)
        probability = self.predictor.predict(event_data)
        logger.debug(f"Recovery probability: {probability:.2f}")
        
        attempt_number = payment_data.get("attempt_number", 0)
        segment = customer_data.get("segment", "new")
        channel = customer_data.get("preferred_channel", "whatsapp")
        amount = float(payment_data.get("amount", 0.0) or 0.0)
        
        # 3. Compliance & Bounded Stopping Rules Evaluation
        compliance_check = self.compliance.evaluate(
            payment_id=payment_id,
            amount=amount,
            status=payment_data.get("status", "failed"),
            recovery_status=payment_data.get("recovery_status"),
            attempt_count=attempt_number,
            recovery_probability=probability,
            customer_segment=segment
        )
        
        # 4. Strategy Engine Decision
        if not compliance_check.allowed:
            if compliance_check.escalate_to_human:
                decision = RecoveryDecision(
                    payment_id=payment_id,
                    recovery_probability=probability,
                    failure_category=analysis.category.value,
                    recommended_action=RecoveryAction.ESCALATE_TO_HUMAN,
                    channel=channel,
                    priority="critical",
                    attempt_number=attempt_number,
                    retry_after_minutes=0,
                    reason=f"[Compliance Gate] {compliance_check.reason}",
                    should_stop=False
                )
            elif compliance_check.schedule_delay_minutes > 0:
                decision = RecoveryDecision(
                    payment_id=payment_id,
                    recovery_probability=probability,
                    failure_category=analysis.category.value,
                    recommended_action=RecoveryAction.RETRY_LATER,
                    channel=channel,
                    priority="medium",
                    attempt_number=attempt_number,
                    retry_after_minutes=compliance_check.schedule_delay_minutes,
                    reason=f"[Compliance Gate] {compliance_check.reason}",
                    should_stop=False
                )
            else:
                decision = RecoveryDecision(
                    payment_id=payment_id,
                    recovery_probability=probability,
                    failure_category=analysis.category.value,
                    recommended_action=RecoveryAction.NO_ACTION,
                    channel=channel,
                    priority="low",
                    attempt_number=attempt_number,
                    retry_after_minutes=0,
                    reason=f"[Stopping Rule] {compliance_check.reason}",
                    should_stop=True
                )
        else:
            decision = self.strategy.decide(
                payment_id=payment_id,
                failure_analysis=analysis,
                recovery_probability=probability,
                attempt_number=attempt_number,
                customer_segment=segment,
                preferred_channel=channel,
                max_attempts=getattr(settings, "max_recovery_attempts", 3)
            )
            
        logger.info(f"Decision: {decision.recommended_action.value} for {payment_id}")
        
        # 5. Personalized Communication Generation
        if not decision.should_stop and decision.recommended_action.value != "NO_ACTION":
            customer_name = customer_data.get("name", "Customer")
            currency = payment_data.get("currency", "INR")
            link = payment_data.get("payment_link", f"https://razorpay.me/pay/{payment_id}")
            
            msg = self.messenger.generate_message(
                customer_name=customer_name,
                amount=amount,
                currency=currency,
                failure_reason_display=decision.failure_category,
                recommended_action=decision.recommended_action.value,
                payment_link=link,
                language=language,
                customer_segment=segment
            )
            decision.message = msg
            
        return decision
