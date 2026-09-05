import logging
from app.core.logging_config import get_logger

logger = get_logger(__name__)

class NotificationService:
    """Mock notification service for sending messages."""
    def send_sms(self, phone: str, message: str) -> dict:
        logger.info(f'MOCK SMS - To: {phone} - Message: {message[:100]}...')
        return {"status": "sent", "channel": "sms", "recipient": phone}

    def send_email(self, email: str, subject: str, message: str) -> dict:
        logger.info(f'MOCK EMAIL - To: {email} - Message: {message[:100]}...')
        return {"status": "sent", "channel": "email", "recipient": email}

    def send_whatsapp(self, phone: str, message: str) -> dict:
        logger.info(f'MOCK WHATSAPP - To: {phone} - Message: {message[:100]}...')
        return {"status": "sent", "channel": "whatsapp", "recipient": phone}

    def send_push(self, customer_id: str, message: str) -> dict:
        logger.info(f'MOCK PUSH - To: {customer_id} - Message: {message[:100]}...')
        return {"status": "sent", "channel": "push", "recipient": customer_id}

    def send(self, channel: str, customer: dict, message: str) -> dict:
        if channel == "sms":
            return self.send_sms(customer.get("phone", ""), message)
        elif channel == "email":
            return self.send_email(customer.get("email", ""), "Payment Recovery", message)
        elif channel == "whatsapp":
            return self.send_whatsapp(customer.get("phone", ""), message)
        elif channel == "push":
            return self.send_push(customer.get("customer_id", ""), message)
        else:
            logger.info(f'MOCK {channel.upper()} - To: {customer} - Message: {message[:100]}...')
            return {"status": "sent", "channel": channel}
