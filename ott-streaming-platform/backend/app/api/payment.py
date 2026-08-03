from fastapi import APIRouter

from app.schemas.payment import (
    PaymentRequest,
)

from app.services.payment_service import (
    PaymentService,
)

router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
)


@router.post("/process")
def process_payment(
    request: PaymentRequest,
):

    return PaymentService.process_payment()