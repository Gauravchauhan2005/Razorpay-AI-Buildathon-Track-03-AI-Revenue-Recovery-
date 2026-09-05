"""
Payment Generator module.
"""

import random
from datetime import datetime, timedelta

class PaymentGenerator:
    """Generates realistic payment records for given customers."""
    
    FAILURE_REASONS = [
        'insufficient_funds', 'bank_decline', 'network_failure', 
        'authentication_failure', 'invalid_details', 'upi_failure', 
        'timeout', 'customer_abandoned', 'limit_exceeded'
    ]
    PAYMENT_METHODS = ['upi', 'card', 'netbanking', 'wallet']
    
    def __init__(self, seed: int | None = None) -> None:
        """Initialize generator with optional seed."""
        self.random = random.Random(seed)
        
    def generate_one(self, customer: dict, payment_id: str | None = None) -> dict:
        """Generate a payment for a specific customer."""
        if payment_id is None:
            payment_id = f"pay_{self.random.randint(100000, 999999)}"
            
        order_id = f"order_{self.random.randint(100000, 999999)}"
        customer_id = customer['customer_id']
        
        amount_base = customer['average_transaction_value']
        # add some variation
        amount = int(amount_base * self.random.uniform(0.5, 2.0))
        
        payment_method = self.random.choices(
            self.PAYMENT_METHODS, 
            weights=[40, 30, 20, 10], 
            k=1
        )[0]
        
        status = self.random.choices(
            ['captured', 'failed'],
            weights=[82, 18],
            k=1
        )[0]
        
        failure_reason = None
        if status == 'failed':
            failure_reason = self.random.choices(
                self.FAILURE_REASONS,
                weights=[25, 15, 20, 10, 5, 12, 8, 3, 2],
                k=1
            )[0]
            
        # timestamp within last 30 days
        days_ago = self.random.uniform(0, 30)
        timestamp = datetime.now() - timedelta(days=days_ago)
        
        device_type = self.random.choices(
            ['mobile', 'desktop', 'tablet'],
            weights=[60, 30, 10],
            k=1
        )[0]
        
        return {
            'payment_id': payment_id,
            'order_id': order_id,
            'customer_id': customer_id,
            'amount': amount,
            'currency': 'INR',
            'payment_method': payment_method,
            'status': status,
            'failure_reason': failure_reason,
            'timestamp': timestamp.isoformat(),
            'device_type': device_type
        }
