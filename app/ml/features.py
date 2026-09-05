class FeatureEngineer:
    """Extracts machine learning features from payment event data."""
    
    def __init__(self):
        self.payment_method_mapping = {"upi": 0, "card": 1, "netbanking": 2, "wallet": 3}
        self.failure_reason_mapping = {
            "insufficient_funds": 0,
            "bank_decline": 1,
            "network_failure": 2,
            "network_error": 2,
            "authentication_failure": 3,
            "auth_failure": 3,
            "invalid_details": 4,
            "upi_failure": 5,
            "upi_error": 5,
            "timeout": 6,
            "customer_abandoned": 7,
            "user_abandoned": 7,
            "limit_exceeded": 8,
            "unknown": 9
        }
        self.feature_names = [
            "amount", "payment_method_encoded", "failure_reason_encoded",
            "previous_attempts", "previous_success_rate", "customer_age_days",
            "hour", "day_of_week", "previous_recovery_success", "is_high_value",
            "customer_segment_encoded"
        ]

    def extract_features(self, event_data: dict) -> dict:
        """Extracts features into a dictionary."""
        amount = event_data.get("amount", 0) / 10000.0
        method = str(event_data.get("method", event_data.get("payment_method", ""))).lower()
        reason = str(event_data.get("failure_reason", "")).lower()
        
        customer_segment_map = {"new": 0, "low_probability": 1, "at_risk": 2, "loyal": 3, "high_value": 4}
        segment = str(event_data.get("segment", event_data.get("customer_segment", "new"))).lower()
        
        return {
            "amount": amount,
            "payment_method_encoded": self.payment_method_mapping.get(method, -1),
            "failure_reason_encoded": self.failure_reason_mapping.get(reason, 9),
            "previous_attempts": int(event_data.get("attempt_number", 0) or 0),
            "previous_success_rate": float(event_data.get("previous_success_rate", 0.0) or 0.0),
            "customer_age_days": min(int(event_data.get("customer_age_days", 0) or 0), 1000),
            "hour": int(event_data.get("hour", 12) or 12),
            "day_of_week": int(event_data.get("day_of_week", 0) or 0),
            "previous_recovery_success": float(event_data.get("previous_recovery_success", 0.0) or 0.0),
            "is_high_value": 1 if float(event_data.get("amount", 0) or 0) > 5000 else 0,
            "customer_segment_encoded": customer_segment_map.get(segment, 0)
        }
        
    def to_feature_vector(self, features: dict) -> list[float]:
        """Converts feature dictionary to ordered list."""
        return [float(features.get(f, 0.0)) for f in self.feature_names]
        
    def get_feature_names(self) -> list[str]:
        """Returns ordered feature names."""
        return self.feature_names
