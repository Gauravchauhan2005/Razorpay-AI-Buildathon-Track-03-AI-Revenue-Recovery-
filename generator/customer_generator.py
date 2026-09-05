"""
Customer Generator module.
"""

import random
from faker import Faker

class CustomerGenerator:
    """Generates realistic customer profiles."""

    def __init__(self, seed: int | None = None) -> None:
        """Initialize generator with optional seed."""
        self.random = random.Random(seed)
        self.faker = Faker()
        if seed is not None:
            Faker.seed(seed)
            
    def generate_one(self, customer_id: str | None = None) -> dict:
        """Generate a single customer profile."""
        if customer_id is None:
            customer_id = f"cust_{self.random.randint(1000, 9999)}"
            
        segment = self.random.choices(
            ['high_value', 'loyal', 'at_risk', 'new', 'low_probability'],
            weights=[15, 25, 20, 25, 15],
            k=1
        )[0]
        
        # Age days
        if segment == 'new':
            customer_age_days = self.random.randint(1, 30)
        elif segment == 'loyal':
            customer_age_days = self.random.randint(180, 1000)
        elif segment == 'high_value':
            customer_age_days = self.random.randint(90, 800)
        elif segment == 'at_risk':
            customer_age_days = self.random.randint(30, 200)
        else:
            customer_age_days = self.random.randint(10, 100)
            
        # Transactions
        if segment == 'new':
            total_transactions = self.random.randint(1, 5)
            success_rate = self.random.uniform(0.5, 0.9)
        elif segment == 'loyal':
            total_transactions = self.random.randint(50, 500)
            success_rate = self.random.uniform(0.85, 0.99)
        elif segment == 'high_value':
            total_transactions = self.random.randint(20, 200)
            success_rate = self.random.uniform(0.9, 0.99)
        elif segment == 'at_risk':
            total_transactions = self.random.randint(10, 50)
            success_rate = self.random.uniform(0.4, 0.7)
        else:
            total_transactions = self.random.randint(1, 20)
            success_rate = self.random.uniform(0.2, 0.5)
            
        successful_transactions = int(total_transactions * success_rate)
        failed_transactions = total_transactions - successful_transactions
        
        # Average Transaction Value
        if segment == 'high_value':
            avg_val = self.random.randint(5000, 50000)
        elif segment == 'loyal':
            avg_val = self.random.randint(500, 10000)
        elif segment == 'new':
            avg_val = self.random.randint(100, 5000)
        elif segment == 'at_risk':
            avg_val = self.random.randint(100, 2000)
        else:
            avg_val = self.random.randint(50, 1000)
            
        preferred_channel = self.random.choices(
            ['whatsapp', 'sms', 'email', 'push'],
            weights=[40, 30, 20, 10],
            k=1
        )[0]
        
        return {
            'customer_id': customer_id,
            'email': self.faker.email(),
            'phone': f"+91{self.random.randint(1000000000, 9999999999)}",
            'segment': segment,
            'customer_age_days': customer_age_days,
            'total_transactions': total_transactions,
            'successful_transactions': successful_transactions,
            'failed_transactions': failed_transactions,
            'average_transaction_value': avg_val,
            'preferred_channel': preferred_channel
        }

    def generate_batch(self, count: int) -> list[dict]:
        """Generate a batch of customers."""
        return [self.generate_one() for _ in range(count)]
