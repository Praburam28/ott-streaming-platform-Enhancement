from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
)


# ==========================================
# Change Subscription Plan
# ==========================================

class ChangePlanRequest(BaseModel):

    user_id: int = Field(
        ...,
        gt=0,
    )

    plan_id: int = Field(
        ...,
        gt=0,
    )


# ==========================================
# Manual Discount / Credit
# ==========================================

class AdjustmentRequest(BaseModel):

    user_id: int = Field(
        ...,
        gt=0,
    )

    discount_amount: float = Field(
        default=0,
        ge=0,
    )

    credit_amount: float = Field(
        default=0,
        ge=0,
    )

    reason: str = Field(
        ...,
        min_length=3,
        max_length=255,
    )

    @field_validator("reason")
    @classmethod
    def validate_reason(cls, value: str):

        value = value.strip()

        if not value:

            raise ValueError(
                "Reason cannot be empty."
            )

        return value

    @field_validator("credit_amount")
    @classmethod
    def validate_amounts(
        cls,
        value,
        info,
    ):

        discount = info.data.get(
            "discount_amount",
            0,
        )

        if discount == 0 and value == 0:

            raise ValueError(
                "Either discount_amount or credit_amount must be greater than zero."
            )

        return value


# ==========================================
# Audit Log Response
# ==========================================

class AuditLogResponse(BaseModel):

    id: int

    admin_user_id: int

    affected_user_id: int

    action: str

    details: str

    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )