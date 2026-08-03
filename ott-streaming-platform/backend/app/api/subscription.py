from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.subscription import (
    SubscribeRequest,
    SubscriptionPlanResponse,
    SubscriptionResponse,
    ProrationPreviewRequest,
    ProrationPreviewResponse,
)
from app.services.subscription_service import SubscriptionService

router = APIRouter(
    prefix="/subscription",
    tags=["Subscription"],
)


@router.get(
    "/plans",
    response_model=list[SubscriptionPlanResponse],
)
def get_plans(
    db: Session = Depends(get_db),
):
    return SubscriptionService.get_plans(db)


@router.post(
    "/subscribe",
    response_model=SubscriptionResponse,
)
def subscribe(
    request: SubscribeRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return SubscriptionService.subscribe(
        db=db,
        user_id=current_user.id,
        plan_id=request.plan_id,
    )
    
@router.get(
    "/current",
    response_model=SubscriptionResponse,
)
def get_current_subscription(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return SubscriptionService.get_current_subscription(
        db=db,
        user_id=current_user.id,
    )


@router.delete("/cancel")
def cancel_subscription(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return SubscriptionService.cancel_subscription(
        db=db,
        user_id=current_user.id,
    )

@router.post(
    "/proration-preview",
    response_model=ProrationPreviewResponse,
)
def proration_preview(
    request: ProrationPreviewRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return SubscriptionService.proration_preview(
        db=db,
        user_id=current_user.id,
        plan_id=request.plan_id,
    )