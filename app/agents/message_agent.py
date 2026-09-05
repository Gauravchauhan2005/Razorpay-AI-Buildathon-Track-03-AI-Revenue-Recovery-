"""Message Agent for personalized payment recovery communication.
Supports English, Hinglish, and Hindi with strict financial guardrails.
"""
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class MessageAgent:
    """Generates context-aware, empathetic, and compliant recovery messages."""

    def __init__(self):
        self.use_llm = bool(settings.openai_api_key and settings.openai_api_key.strip())
        
        # English Templates
        self.templates_en = {
            ("RETRY_NOW", "NETWORK_FAILURE"): "Hi {customer_name}, your payment of {currency} {amount:,.0f} encountered a temporary network glitch. Click here to instantly complete it: {payment_link}",
            ("RETRY_LATER", "INSUFFICIENT_FUNDS"): "Hi {customer_name}, your payment of {currency} {amount:,.0f} could not be processed due to a temporary balance issue. You can safely complete it anytime here: {payment_link}",
            ("SEND_PAYMENT_LINK", "DEFAULT"): "Hi {customer_name}, we noticed your payment of {currency} {amount:,.0f} was interrupted. Tap here to quickly resume your order: {payment_link}",
            ("SEND_REMINDER", "DEFAULT"): "Hi {customer_name}, friendly reminder: your payment of {currency} {amount:,.0f} is pending. Tap to finish securely: {payment_link}",
            ("ESCALATE_TO_HUMAN", "DEFAULT"): "Hello {customer_name}, thank you for your patience. Your dedicated Razorpay account specialist is reviewing your transaction of {currency} {amount:,.0f} and will assist you directly.",
            ("RETRY_LATER", "DEFAULT"): "Hi {customer_name}, your payment of {currency} {amount:,.0f} was temporarily paused. Retry securely here: {payment_link}",
            ("NO_ACTION", "DEFAULT"): "Hi {customer_name}, your payment of {currency} {amount:,.0f} could not be completed. Please reach out to support if you need assistance.",
        }

        # Hinglish Templates (India FinTech / D2C conversion booster)
        self.templates_hinglish = {
            ("RETRY_NOW", "NETWORK_FAILURE"): "Namaste {customer_name}! Aapka {currency} {amount:,.0f} ka payment bank network issue ki wajah se atak gaya tha. Abhi dubara try karne ke liye yahan tap karein: {payment_link}",
            ("RETRY_LATER", "INSUFFICIENT_FUNDS"): "Hi {customer_name}, aapke {currency} {amount:,.0f} payment mein balance issue aaya tha. Account check karke aap yahan se aasaani se pay kar sakte hain: {payment_link}",
            ("SEND_PAYMENT_LINK", "DEFAULT"): "Hi {customer_name}, aapka {currency} {amount:,.0f} ka payment adhura reh gaya tha. Order complete karne ke liye is link par tap karein: {payment_link}",
            ("SEND_REMINDER", "DEFAULT"): "Namaste {customer_name}, aapka {currency} {amount:,.0f} ka payment pending hai. Yahan click karke payment poora karein: {payment_link}",
            ("ESCALATE_TO_HUMAN", "DEFAULT"): "Namaste {customer_name}, aapki {currency} {amount:,.0f} transaction ke liye hamare relationship manager aapse jald hi sampark karenge.",
            ("RETRY_LATER", "DEFAULT"): "Hi {customer_name}, thodi der baad aapka payment retry kar sakte hain yahan se: {payment_link}",
            ("NO_ACTION", "DEFAULT"): "Namaste {customer_name}, aapka payment complete nahi ho paya. Kisi bhi sahayata ke liye support team se contact karein.",
        }

        # Hindi Templates
        self.templates_hi = {
            ("RETRY_NOW", "NETWORK_FAILURE"): "नमस्ते {customer_name}, नेटवर्क समस्या के कारण आपका {currency} {amount:,.0f} का भुगतान अधूरा रह गया था। पुनः प्रयास करने के लिए लिंक पर क्लिक करें: {payment_link}",
            ("RETRY_LATER", "INSUFFICIENT_FUNDS"): "नमस्ते {customer_name}, आपके {currency} {amount:,.0f} के भुगतान में शेष राशि की समस्या आई थी। कृपया खाता जांचें और यहाँ भुगतान करें: {payment_link}",
            ("SEND_PAYMENT_LINK", "DEFAULT"): "नमस्ते {customer_name}, अपने {currency} {amount:,.0f} के भुगतान को पूरा करने के लिए यहाँ क्लिक करें: {payment_link}",
            ("SEND_REMINDER", "DEFAULT"): "नमस्ते {customer_name}, आपका {currency} {amount:,.0f} का भुगतान अभी लंबित है। पूरा करने के लिए लिंक पर क्लिक करें: {payment_link}",
            ("ESCALATE_TO_HUMAN", "DEFAULT"): "नमस्ते {customer_name}, हमारे प्रतिनिधि आपके {currency} {amount:,.0f} के भुगतान में सहायता के लिए शीघ्र संपर्क करेंगे।",
            ("RETRY_LATER", "DEFAULT"): "नमस्ते {customer_name}, आप कुछ समय बाद यहाँ से पुनः भुगतान कर सकते हैं: {payment_link}",
            ("NO_ACTION", "DEFAULT"): "नमस्ते {customer_name}, आपका भुगतान पूरा नहीं हो सका। सहायता के लिए सपोर्ट से संपर्क करें।",
        }

    def _get_safe_failure_reason(self, failure_reason: str) -> str:
        """Converts internal technical error codes to user-safe explanations."""
        mapping = {
            "INSUFFICIENT_FUNDS": "a temporary balance verification issue",
            "BANK_DECLINE": "a temporary bank authorization response",
            "NETWORK_FAILURE": "a momentary payment gateway network timeout",
            "TIMEOUT": "a payment session timeout",
            "AUTHENTICATION_FAILURE": "an OTP / authentication timeout",
            "UPI_FAILURE": "a temporary UPI server response delay",
        }
        return mapping.get(failure_reason, "a temporary processing delay")

    def generate_message(
        self,
        customer_name: str,
        amount: float,
        currency: str,
        failure_reason_display: str,
        recommended_action: str,
        payment_link: Optional[str] = None,
        language: str = "english",
        customer_segment: str = "new"
    ) -> str:
        """Generates a professional, guardrailed payment recovery message."""
        link_str = payment_link if payment_link else "https://razorpay.me/pay"
        safe_reason = self._get_safe_failure_reason(failure_reason_display)
        
        # High value VIP greeting override
        if customer_segment == "high_value" and recommended_action == "ESCALATE_TO_HUMAN":
            return (
                f"Hello {customer_name}, thank you for choosing us. We noticed your transaction of {currency} {amount:,.0f} "
                f"faced {safe_reason}. Your priority account concierge has been notified and will assist you immediately."
            )

        # Optional LLM Generation with strict guardrails
        if self.use_llm:
            try:
                import openai
                client = openai.OpenAI(api_key=settings.openai_api_key)
                lang_instruction = "in Hinglish (Hindi written in English script)" if language == "hinglish" else f"in {language}"
                
                prompt = (
                    f"Draft a warm, reassuring customer payment recovery message {lang_instruction}.\n"
                    f"Customer: {customer_name}\n"
                    f"Amount: {currency} {amount:,.0f}\n"
                    f"Reason: {safe_reason}\n"
                    f"Action: {recommended_action}\n"
                    f"Link: {link_str}\n"
                    f"Constraints: Under 160 characters. Do NOT ask for OTP/PIN/password. Do NOT promise fake discounts."
                )

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are Razorpay's intelligent payment recovery assistant. "
                                "Rules: Never ask for card PIN, OTP, CVV, or passwords. "
                                "Never invent unauthorized discounts. Keep tone empathetic and professional."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=100,
                    temperature=0.3
                )
                content = response.choices[0].message.content
                if content:
                    return content.strip()
            except Exception as e:
                logger.warning(f"LLM generation failed ({e}). Falling back to certified template.")

        # Template Selection
        if language == "hinglish":
            templates = self.templates_hinglish
        elif language == "hindi":
            templates = self.templates_hi
        else:
            templates = self.templates_en

        key = (recommended_action, failure_reason_display)
        if key not in templates:
            key = (recommended_action, "DEFAULT")
        if key not in templates:
            key = ("SEND_PAYMENT_LINK", "DEFAULT")

        template = templates.get(
            key,
            "Hi {customer_name}, your payment of {currency} {amount:,.0f} was interrupted. Please retry here: {payment_link}"
        )

        return template.format(
            customer_name=customer_name,
            amount=amount,
            currency=currency,
            payment_link=link_str
        ).strip()
