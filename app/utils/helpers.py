import json
from typing import Any

def format_currency(amount: float, currency: str = 'INR') -> str:
    """Format an amount as currency."""
    if currency.upper() == 'INR':
        return f"₹{amount:,.2f}"
    return f"{currency} {amount:,.2f}"

def minutes_to_human(minutes: int) -> str:
    """Convert minutes to human readable string."""
    if minutes < 60:
        return f"{minutes} minutes"
    elif minutes < 24 * 60:
        hours = minutes // 60
        return f"{hours} hour{'s' if hours > 1 else ''}"
    else:
        days = minutes // (24 * 60)
        return f"{days} day{'s' if days > 1 else ''}"

def safe_json_loads(text: str) -> dict[str, Any]:
    """Safely parse JSON string."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return {}

def generate_payment_link_url(payment_id: str) -> str:
    """Generate a mock payment link URL."""
    return f"https://rzp.io/mock/{payment_id}"

def calculate_recovery_rate(recovered: int, total: int) -> float:
    """Calculate recovery rate as a percentage."""
    if total <= 0:
        return 0.0
    return (recovered / total) * 100

def truncate_message(msg: str, max_len: int = 160) -> str:
    """Truncate message to max length."""
    if len(msg) <= max_len:
        return msg
    return msg[:max_len-3] + "..."
