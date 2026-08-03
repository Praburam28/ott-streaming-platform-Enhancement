from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.admin.admin_audit_log import AdminAuditLog
from app.models.admin.subscription_adjustment import SubscriptionAdjustment

from app.repositories.admin.admin_repository import AdminRepository


class AdminService:

    # ===============================
    # Upgrade / Downgrade Subscription
    # ===============================

    @staticmethod
    def change_subscription_plan(
        db: Session,
        admin_user_id: int,
        user_id: int,
        plan_id: int,
    ):

        subscription = AdminRepository.get_subscription(
            db,
            user_id,
        )

        if subscription is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found.",
            )

        subscription.plan_id = plan_id

        AdminRepository.update(db)

        audit = AdminAuditLog(
            admin_user_id=admin_user_id,
            affected_user_id=user_id,
            action="CHANGE_PLAN",
            details=f"Changed subscription to Plan {plan_id}",
        )

        AdminRepository.create_audit_log(
            db,
            audit,
        )

        return subscription

    # ===============================
    # Pause Subscription
    # ===============================

    @staticmethod
    def pause_subscription(
        db: Session,
        admin_user_id: int,
        user_id: int,
    ):

        subscription = AdminRepository.get_subscription(
            db,
            user_id,
        )

        if subscription is None:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found.",
            )

        subscription.status = "PAUSED"

        AdminRepository.update(db)

        audit = AdminAuditLog(
            admin_user_id=admin_user_id,
            affected_user_id=user_id,
            action="PAUSE_SUBSCRIPTION",
            details="Subscription paused",
        )

        AdminRepository.create_audit_log(
            db,
            audit,
        )

        return subscription

    # ===============================
    # Resume Subscription
    # ===============================

    @staticmethod
    def resume_subscription(
        db: Session,
        admin_user_id: int,
        user_id: int,
    ):

        subscription = AdminRepository.get_subscription(
            db,
            user_id,
        )

        if subscription is None:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found.",
            )

        subscription.status = "ACTIVE"

        AdminRepository.update(db)

        audit = AdminAuditLog(
            admin_user_id=admin_user_id,
            affected_user_id=user_id,
            action="RESUME_SUBSCRIPTION",
            details="Subscription resumed",
        )

        AdminRepository.create_audit_log(
            db,
            audit,
        )

        return subscription

    # ===============================
    # Manual Discount / Credit
    # ===============================

    @staticmethod
    def apply_adjustment(
        db: Session,
        admin_user_id: int,
        user_id: int,
        discount_amount: float,
        credit_amount: float,
        reason: str,
    ):

        adjustment = SubscriptionAdjustment(
            user_id=user_id,
            admin_user_id=admin_user_id,
            discount_amount=discount_amount,
            credit_amount=credit_amount,
            reason=reason,
        )

        AdminRepository.create_adjustment(
            db,
            adjustment,
        )

        audit = AdminAuditLog(
            admin_user_id=admin_user_id,
            affected_user_id=user_id,
            action="ADJUSTMENT",
            details=reason,
        )

        AdminRepository.create_audit_log(
            db,
            audit,
        )

        return adjustment

    # ===============================
    # Audit Logs
    # ===============================

    @staticmethod
    def get_logs(
        db: Session,
    ):
        return AdminRepository.get_all_logs(
            db,
        )