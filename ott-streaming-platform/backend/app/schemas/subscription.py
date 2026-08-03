from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubscriptionPlanResponse(BaseModel):
    id: int
    plan_name: str
    price: float
    duration_days: int
    description: str

    model_config = ConfigDict(from_attributes=True)


class SubscribeRequest(BaseModel):
    plan_id: int


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    start_date: datetime
    end_date: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)
    
class ProrationPreviewRequest(BaseModel):
    plan_id: int


class ProrationPreviewResponse(BaseModel):
    current_plan: str
    new_plan: str
    remaining_days: int
    current_plan_price: float
    new_plan_price: float
    credit_amount: float
    payable_amount: float