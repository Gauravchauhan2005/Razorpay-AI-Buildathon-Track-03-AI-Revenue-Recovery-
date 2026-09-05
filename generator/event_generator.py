"""
Event Generator CLI.
"""

import argparse
import json
import random
from datetime import datetime
import os
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generator.customer_generator import CustomerGenerator
from generator.payment_generator import PaymentGenerator

def calculate_recovery_prob(payment: dict, customer: dict, previous_attempts: int, previous_success_rate: float) -> float:
    """Calculate the probability of recovery for a failed payment."""
    if payment['status'] != 'failed':
        return 0.0
        
    reason = payment['failure_reason']
    
    # Base probability by reason
    if reason in ['network_failure', 'timeout']:
        base_prob = 0.80
    elif reason == 'insufficient_funds':
        base_prob = 0.60
    elif reason in ['bank_decline', 'authentication_failure']:
        base_prob = 0.35
    elif reason in ['customer_abandoned', 'limit_exceeded']:
        base_prob = 0.15
    else:
        base_prob = 0.30
        
    # Segment modifiers
    segment = customer['segment']
    if segment == 'high_value':
        base_prob *= 1.2
    elif segment == 'loyal':
        base_prob *= 1.1
    elif segment == 'low_probability':
        base_prob *= 0.5
        
    # Previous success rate modifier
    base_prob *= (0.5 + previous_success_rate)
    
    # Attempt count decay
    if previous_attempts > 0:
        base_prob *= (0.8 ** previous_attempts)
        
    return min(max(base_prob, 0.0), 1.0)

def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Synthetic Event Generator")
    parser.add_argument('--count', type=int, default=1000, help='Number of events to generate')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--output', type=str, default='generator/data/batch_001.jsonl', help='Output path')
    parser.add_argument('--customers', type=int, default=200, help='Number of unique customers')
    
    args = parser.parse_args()
    
    rnd = random.Random(args.seed)
    
    print(f"Generating {args.customers} customers...")
    cust_gen = CustomerGenerator(seed=args.seed)
    customers = cust_gen.generate_batch(args.customers)
    
    pay_gen = PaymentGenerator(seed=args.seed)
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    print(f"Generating {args.count} events to {args.output}...")
    
    total_events = 0
    failed_count = 0
    recovered_count = 0
    
    with open(args.output, 'w') as f:
        for i in range(args.count):
            customer = rnd.choice(customers)
            payment = pay_gen.generate_one(customer)
            
            # Behaviour
            previous_attempts = rnd.randint(0, 5)
            time_since_last_payment = rnd.randint(10, 10000)
            
            tot_tx = customer['total_transactions']
            succ_tx = customer['successful_transactions']
            prev_success_rate = succ_tx / tot_tx if tot_tx > 0 else 0.0
            
            # Context
            dt = datetime.fromisoformat(payment['timestamp'])
            hour = dt.hour
            day_of_week = dt.weekday()
            
            # Recovery
            prev_recovery_attempts = rnd.randint(0, 3)
            prev_recovery_success = rnd.uniform(0, 1)
            
            # Target
            recovered = 0
            if payment['status'] == 'failed':
                failed_count += 1
                prob = calculate_recovery_prob(payment, customer, prev_recovery_attempts, prev_success_rate)
                if rnd.random() < prob:
                    recovered = 1
                    recovered_count += 1
            
            event_id = f"evt_{i+1:06d}"
            
            event_record = {
                'event_id': event_id,
                # Customer fields
                **customer,
                # Payment fields
                **payment,
                # Behaviour
                'previous_attempts': previous_attempts,
                'time_since_last_payment': time_since_last_payment,
                'previous_success_rate': prev_success_rate,
                # Context
                'hour': hour,
                'day_of_week': day_of_week,
                # Recovery info
                'previous_recovery_attempts': prev_recovery_attempts,
                'previous_recovery_success': prev_recovery_success,
                # Target
                'recovered': recovered
            }
            
            f.write(json.dumps(event_record) + "\n")
            total_events += 1
            
    print("\\n--- Summary Statistics ---")
    print(f"Total events: {total_events}")
    print(f"Failed payments: {failed_count}")
    recovery_rate = (recovered_count / failed_count * 100) if failed_count > 0 else 0
    print(f"Recovered count: {recovered_count} ({recovery_rate:.1f}% recovery rate for failed payments)")

if __name__ == '__main__':
    main()
