from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any

class WebhookPayload(BaseModel):
    event_id: str
    event_type: str
    payload: dict[str, Any]

class PaymentResponse(BaseModel):
    payment_id: str
    order_id: Optional[str] = None
    customer_id: Optional[str] = None
    amount: float
    currency: str
    method: Optional[str] = None
    status: str
    failure_reason: Optional[str] = None
    recovery_status: Optional[str] = None
    recovery_probability: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RecoveryAttemptResponse(BaseModel):
    id: int
    payment_id: str
    attempt_number: int
    channel: str
    strategy: str
    message: Optional[str] = None
    status: str
    result: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnalyticsOverview(BaseModel):
    total_payments: int
    failed_payments: int
    recovery_attempts: int
    recovered_payments: int
    recovery_rate: float
    revenue_recovered: float

class FailureBreakdown(BaseModel):
    reason: str
    count: int
    percentage: float

class ChannelEffectiveness(BaseModel):
    channel: str
    attempts: int
    recovered: int
    rate: float
