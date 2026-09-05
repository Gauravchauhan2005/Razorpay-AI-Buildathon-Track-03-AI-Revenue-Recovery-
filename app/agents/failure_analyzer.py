from enum import Enum
from pydantic import BaseModel

class FailureCategory(str, Enum):
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    BANK_DECLINE = "BANK_DECLINE"
    NETWORK_FAILURE = "NETWORK_FAILURE"
    AUTHENTICATION_FAILURE = "AUTHENTICATION_FAILURE"
    INVALID_DETAILS = "INVALID_DETAILS"
    UPI_FAILURE = "UPI_FAILURE"
    TIMEOUT = "TIMEOUT"
    CUSTOMER_ABANDONED = "CUSTOMER_ABANDONED"
    LIMIT_EXCEEDED = "LIMIT_EXCEEDED"
    UNKNOWN = "UNKNOWN"

class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Recoverability(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"

class FailureAnalysisResult(BaseModel):
    category: FailureCategory
    severity: Severity
    recoverability: Recoverability
    description: str
    recommended_wait_minutes: int

class FailureAnalyzer:
    """Analyzes payment failure reasons and categorizes them."""
    
    def __init__(self):
        self.category_mapping = {
            "insufficient_funds": FailureCategory.INSUFFICIENT_FUNDS,
            "bank_decline": FailureCategory.BANK_DECLINE,
            "network_failure": FailureCategory.NETWORK_FAILURE,
            "network_error": FailureCategory.NETWORK_FAILURE,
            "authentication_failure": FailureCategory.AUTHENTICATION_FAILURE,
            "auth_failure": FailureCategory.AUTHENTICATION_FAILURE,
            "invalid_details": FailureCategory.INVALID_DETAILS,
            "upi_failure": FailureCategory.UPI_FAILURE,
            "upi_error": FailureCategory.UPI_FAILURE,
            "timeout": FailureCategory.TIMEOUT,
            "customer_abandoned": FailureCategory.CUSTOMER_ABANDONED,
            "user_abandoned": FailureCategory.CUSTOMER_ABANDONED,
            "limit_exceeded": FailureCategory.LIMIT_EXCEEDED,
        }
    
    def analyze(self, failure_reason: str) -> FailureAnalysisResult:
        """Analyzes a failure reason string and returns structured insights."""
        category = self.category_mapping.get(failure_reason.lower(), FailureCategory.UNKNOWN)
        
        severity_map = {
            FailureCategory.NETWORK_FAILURE: Severity.MEDIUM,
            FailureCategory.TIMEOUT: Severity.MEDIUM,
            FailureCategory.BANK_DECLINE: Severity.HIGH,
            FailureCategory.AUTHENTICATION_FAILURE: Severity.HIGH,
            FailureCategory.INSUFFICIENT_FUNDS: Severity.MEDIUM,
            FailureCategory.CUSTOMER_ABANDONED: Severity.LOW,
            FailureCategory.INVALID_DETAILS: Severity.LOW,
            FailureCategory.UPI_FAILURE: Severity.MEDIUM,
            FailureCategory.LIMIT_EXCEEDED: Severity.MEDIUM,
            FailureCategory.UNKNOWN: Severity.LOW,
        }
        
        recoverability_map = {
            FailureCategory.NETWORK_FAILURE: Recoverability.HIGH,
            FailureCategory.TIMEOUT: Recoverability.HIGH,
            FailureCategory.INSUFFICIENT_FUNDS: Recoverability.MEDIUM,
            FailureCategory.UPI_FAILURE: Recoverability.MEDIUM,
            FailureCategory.BANK_DECLINE: Recoverability.LOW,
            FailureCategory.AUTHENTICATION_FAILURE: Recoverability.LOW,
            FailureCategory.CUSTOMER_ABANDONED: Recoverability.NONE,
            FailureCategory.INVALID_DETAILS: Recoverability.NONE,
            FailureCategory.LIMIT_EXCEEDED: Recoverability.LOW,
            FailureCategory.UNKNOWN: Recoverability.LOW,
        }
        
        wait_time_map = {
            FailureCategory.NETWORK_FAILURE: 5,
            FailureCategory.TIMEOUT: 5,
            FailureCategory.INSUFFICIENT_FUNDS: 360,
            FailureCategory.BANK_DECLINE: 1440,
            FailureCategory.AUTHENTICATION_FAILURE: 60,
            FailureCategory.UPI_FAILURE: 15,
            FailureCategory.CUSTOMER_ABANDONED: 0,
            FailureCategory.INVALID_DETAILS: 0,
            FailureCategory.LIMIT_EXCEEDED: 1440,
            FailureCategory.UNKNOWN: 60,
        }
        
        return FailureAnalysisResult(
            category=category,
            severity=severity_map.get(category, Severity.LOW),
            recoverability=recoverability_map.get(category, Recoverability.LOW),
            description=f"Failure due to {category.value}",
            recommended_wait_minutes=wait_time_map.get(category, 60)
        )
