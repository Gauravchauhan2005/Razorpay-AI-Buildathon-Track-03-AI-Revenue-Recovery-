import razorpay
from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

class RazorpayService:
    """Razorpay API integration service."""
    def __init__(self):
        if settings.razorpay_key_id and settings.razorpay_key_secret:
            self.client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))
        else:
            self.client = None

    @property
    def is_configured(self) -> bool:
        return self.client is not None

    def fetch_payment(self, payment_id: str) -> dict | None:
        if not self.is_configured:
            return None
        try:
            return self.client.payment.fetch(payment_id)
        except Exception as e:
            logger.error(f"Error fetching payment {payment_id}: {e}")
            return None

    def create_payment_link(self, amount: int, currency: str, customer_info: dict, description: str) -> dict | None:
        if not self.is_configured:
            return {"short_url": "https://rzp.io/mock/link"}
        try:
            return self.client.payment_link.create({
                "amount": amount,
                "currency": currency,
                "customer": customer_info,
                "description": description
            })
        except Exception as e:
            logger.error(f"Error creating payment link: {e}")
            return None

    def verify_payment_signature(self, params: dict) -> bool:
        if not self.is_configured:
            return False
        try:
            return self.client.utility.verify_payment_signature(params)
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            return False
