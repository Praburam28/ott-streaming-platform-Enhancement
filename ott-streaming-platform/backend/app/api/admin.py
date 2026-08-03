from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.admin import require_admin

from app.services.admin.admin_service import AdminService

from app.schemas.admin.admin import (
    ChangePlanRequest,
    AdjustmentRequest,
    AuditLogResponse,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

# ---------------------------------------
# Force Upgrade / Downgrade
# ---------------------------------------

@router.patch("/subscription/change-plan")
def change_plan(
    request: ChangePlanRequest,
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return AdminService.change_subscription_plan(
        db=db,
        admin_user_id=current_admin.id,
        user_id=request.user_id,
        plan_id=request.plan_id,
    )


# ---------------------------------------
# Pause Subscription
# ---------------------------------------

@router.patch("/subscription/{user_id}/pause")
def pause_subscription(
    user_id: int,
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return AdminService.pause_subscription(
        db=db,
        admin_user_id=current_admin.id,
        user_id=user_id,
    )


# ---------------------------------------
# Resume Subscription
# ---------------------------------------

@router.patch("/subscription/{user_id}/resume")
def resume_subscription(
    user_id: int,
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return AdminService.resume_subscription(
        db=db,
        admin_user_id=current_admin.id,
        user_id=user_id,
    )


# ---------------------------------------
# Discount / Credit
# ---------------------------------------

@router.post("/subscription/adjustment")
def adjustment(
    request: AdjustmentRequest,
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return AdminService.apply_adjustment(
        db=db,
        admin_user_id=current_admin.id,
        user_id=request.user_id,
        discount_amount=request.discount_amount,
        credit_amount=request.credit_amount,
        reason=request.reason,
    )


# ---------------------------------------
# Audit Logs
# ---------------------------------------

@router.get(
    "/audit-logs",
    response_model=list[AuditLogResponse],
)
def audit_logs(
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return AdminService.get_logs(db)