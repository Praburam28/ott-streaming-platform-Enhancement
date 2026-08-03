from pydantic import BaseModel


class PaymentRequest(BaseModel):
    plan_id: int


class PaymentResponse(BaseModel):
    success: bool
    message: str