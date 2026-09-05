from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.payment_service import PaymentService
from app.utils.validators import PaymentResponse

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("", response_model=list[PaymentResponse])
@router.get("/", response_model=list[PaymentResponse], include_in_schema=False)
def get_payments(skip: int = 0, limit: int = 100, status: str | None = None, db: Session = Depends(get_db)):
    service = PaymentService(db)
    return service.get_payments(skip=skip, limit=limit, status=status)

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    service = PaymentService(db)
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
