from pydantic import BaseModel, ConfigDict


class MonthlyRevenueReport(BaseModel):
    month: str
    total_subscriptions: int
    estimated_revenue: float

    model_config = ConfigDict(
        from_attributes=True
    )


class SubscriptionSummaryReport(BaseModel):
    active_subscriptions: int
    cancelled_subscriptions: int

    model_config = ConfigDict(
        from_attributes=True
    )


class PlanDistributionReport(BaseModel):
    plan_name: str
    total_subscriptions: int

    model_config = ConfigDict(
        from_attributes=True
    )