"""Load generated event data into the database."""
import json
import sys
sys.path.insert(0, ".")

from app.database.database import SessionLocal, create_tables
from app.models.customer import Customer
from app.models.payment import Payment
from app.models.event import Event
from datetime import datetime


def load_data(filepath: str = "generator/data/batch_001.jsonl"):
    """Load JSONL events into the database."""
    create_tables()
    db = SessionLocal()

    # Track unique customers
    seen_customers: set[str] = set()
    total = 0
    failed = 0

    with open(filepath, "r") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            total += 1

            cid = data["customer_id"]
            if cid not in seen_customers:
                existing = db.query(Customer).filter(Customer.customer_id == cid).first()
                if not existing:
                    customer = Customer(
                        customer_id=cid,
                        email=data.get("email"),
                        phone=data.get("phone"),
                        segment=data.get("segment", "new"),
                        preferred_channel=data.get("preferred_channel", "sms"),
                        total_transactions=data.get("total_transactions", 0),
                        successful_transactions=data.get("successful_transactions", 0),
                        failed_transactions=data.get("failed_transactions", 0),
                        average_transaction_value=data.get("average_transaction_value", 0.0),
                    )
                    db.add(customer)
                seen_customers.add(cid)

            # Create payment
            pid = data["payment_id"]
            existing_payment = db.query(Payment).filter(Payment.payment_id == pid).first()
            if not existing_payment:
                status = data.get("status", "failed")
                if status == "failed":
                    failed += 1
                payment = Payment(
                    payment_id=pid,
                    order_id=data.get("order_id"),
                    customer_id=cid,
                    amount=data.get("amount", 0),
                    currency=data.get("currency", "INR"),
                    method=data.get("payment_method", data.get("method", "upi")),
                    status=status,
                    failure_reason=data.get("failure_reason"),
                    device_type=data.get("device_type"),
                    recovery_status="eligible" if status == "failed" else None,
                    created_at=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow(),
                )
                db.add(payment)

            # Create event
            eid = data.get("event_id", f"evt_{total:06d}")
            existing_event = db.query(Event).filter(Event.event_id == eid).first()
            if not existing_event:
                event = Event(
                    event_id=eid,
                    event_type="payment.failed" if data.get("status") == "failed" else "payment.captured",
                    payment_id=pid,
                    payload=json.dumps(data),
                    received_at=datetime.utcnow(),
                    processing_status="processed",
                )
                db.add(event)

    db.commit()
    db.close()
    print(f"Loaded {total} events ({failed} failed) with {len(seen_customers)} unique customers.")


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "generator/data/batch_001.jsonl"
    load_data(filepath)
