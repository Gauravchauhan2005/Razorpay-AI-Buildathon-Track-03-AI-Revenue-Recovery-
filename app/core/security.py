"""Security and verification module."""
import hmac
import hashlib

def verify_webhook_signature(request_body: bytes, signature: str, secret: str) -> bool:
    """Verifies Razorpay webhook signatures."""
    if not signature or not secret:
        return False
        
    expected_mac = hmac.new(
        key=secret.encode('utf-8'),
        msg=request_body,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_mac, signature)
