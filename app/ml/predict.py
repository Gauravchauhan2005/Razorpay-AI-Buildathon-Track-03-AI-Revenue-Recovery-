import os
import joblib
from typing import Dict, Any
from app.ml.features import FeatureEngineer

class RecoveryPredictor:
    """Predicts the probability of successful payment recovery."""
    
    def __init__(self):
        self.model_path = "app/ml/model.pkl"
        self.model = None
        self.engineer = FeatureEngineer()
        
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception as e:
                print(f"Error loading model: {e}")
                
    @property
    def has_model(self) -> bool:
        return self.model is not None
        
    def predict(self, features: dict) -> float:
        """Predicts recovery probability. Uses ML model if available, else heuristic."""
        if self.has_model:
            vector = self.engineer.to_feature_vector(features)
            try:
                return float(self.model.predict_proba([vector])[0][1])
            except Exception:
                pass 
                
        reason = str(features.get("failure_reason", "")).lower()
        base_prob = {
            "network_failure": 0.85,
            "network_error": 0.85,
            "timeout": 0.80,
            "insufficient_funds": 0.65,
            "upi_failure": 0.55,
            "upi_error": 0.55,
            "bank_decline": 0.35,
            "authentication_failure": 0.30,
            "auth_failure": 0.30,
            "invalid_details": 0.20,
            "customer_abandoned": 0.15,
            "user_abandoned": 0.15,
            "limit_exceeded": 0.10
        }.get(reason, 0.30)
        
        success_rate = float(features.get("previous_success_rate", 0.5) or 0.5)
        base_prob *= (0.5 + success_rate)
        
        attempts = int(features.get("previous_attempts", 0) or 0)
        base_prob -= (attempts * 0.15)
        
        return max(0.0, min(1.0, base_prob))
