"""
Pytest fixtures for AI Payment Recovery Agent tests.
"""
import pytest
from typing import Dict, Any, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

@pytest.fixture
def test_db() -> Generator[Any, None, None]:
    """Provides an in-memory SQLite database session."""
    from app.database.database import Base
    import app.models  # registers all models with Base
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_client(test_db: Any) -> TestClient:
    """Provides a FastAPI TestClient with test database override."""
    # Mock return for now as the app isn't fully set up here
    return TestClient(None)

@pytest.fixture
def sample_payment_data() -> Dict[str, Any]:
    """Realistic failed payment data."""
    return {
        "id": "pay_xyz123",
        "amount": 50000,
        "currency": "INR",
        "status": "failed",
        "error_code": "BAD_REQUEST_ERROR",
        "error_description": "Payment failed due to network error",
        "error_source": "bank",
        "error_step": "payment_authentication",
        "error_reason": "network_error"
    }

@pytest.fixture
def sample_customer_data() -> Dict[str, Any]:
    """Realistic customer data."""
    return {
        "id": "cust_abc456",
        "email": "test@example.com",
        "contact": "+919876543210",
        "segment": "high_value"
    }

@pytest.fixture
def sample_webhook_payload(sample_payment_data: Dict[str, Any]) -> Dict[str, Any]:
    """Razorpay payment.failed webhook payload."""
    return {
        "entity": "event",
        "account_id": "acc_123",
        "event": "payment.failed",
        "contains": ["payment"],
        "payload": {
            "payment": {
                "entity": sample_payment_data
            }
        },
        "created_at": 1612134000
    }
