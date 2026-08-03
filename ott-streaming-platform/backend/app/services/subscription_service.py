from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)


class SubscriptionService:

    # ======================================
    # Get All Subscription Plans
    # ======================================

    @staticmethod
    def get_plans(db: Session):
        return SubscriptionRepository.get_all_plans(db)

    # ======================================
    # Subscribe / Upgrade / Downgrade
    # ======================================

    @staticmethod
    def subscribe(
        db: Session,
        user_id: int,
        plan_id: int,
    ):

        plan = SubscriptionRepository.get_plan_by_id(
            db,
            plan_id,
        )

        if plan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription plan not found.",
            )

        current = SubscriptionRepository.get_user_subscription(
            db,
            user_id,
        )

        start_date = datetime.utcnow()

        end_date = start_date + timedelta(
            days=plan.duration_days
        )

        if current:

            current.plan_id = plan.id
            current.start_date = start_date
            current.end_date = end_date
            current.status = "ACTIVE"

            SubscriptionRepository.update_subscription(db)

            return current

        subscription = Subscription(
            user_id=user_id,
            plan_id=plan.id,
            start_date=start_date,
            end_date=end_date,
            status="ACTIVE",
        )

        return SubscriptionRepository.create_subscription(
            db,
            subscription,
        )

    # ======================================
    # Get Current Subscription
    # ======================================

    @staticmethod
    def get_current_subscription(
        db: Session,
        user_id: int,
    ):

        subscription = SubscriptionRepository.get_active_subscription(
            db,
            user_id,
        )

        if subscription is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active subscription found.",
            )

        return subscription

    # ======================================
    # Cancel Subscription
    # ======================================

    @staticmethod
    def cancel_subscription(
        db: Session,
        user_id: int,
    ):

        subscription = SubscriptionRepository.get_active_subscription(
            db,
            user_id,
        )

        if subscription is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active subscription found.",
            )

        subscription.status = "CANCELLED"

        SubscriptionRepository.cancel_subscription(db)

        return {
            "message": "Subscription cancelled successfully."
        }
    # ======================================
    # Proration Preview
    # ======================================

    @staticmethod
    def proration_preview(
        db: Session,
        user_id: int,
        plan_id: int,
    ):

        subscription = SubscriptionRepository.get_active_subscription(
            db,
            user_id,
        )

        if subscription is None:
            raise HTTPException(
                status_code=404,
                detail="No active subscription found.",
            )

        current_plan = SubscriptionRepository.get_plan_by_id(
            db,
            subscription.plan_id,
        )

        new_plan = SubscriptionRepository.get_plan_by_id(
            db,
            plan_id,
        )

        if new_plan is None:
            raise HTTPException(
                status_code=404,
                detail="Subscription plan not found.",
            )

        remaining_days = max(
            0,
            (subscription.end_date - datetime.utcnow()).days,
        )

        total_days = current_plan.duration_days

        credit_amount = round(
            (
                float(current_plan.price)
                / total_days
            )
            * remaining_days,
            2,
        )

        payable_amount = max(
            0,
            round(
                float(new_plan.price)
                - credit_amount,
                2,
            ),
        )

        return {
            "current_plan": current_plan.plan_name,
            "new_plan": new_plan.plan_name,
            "remaining_days": remaining_days,
            "current_plan_price": float(current_plan.price),
            "new_plan_price": float(new_plan.price),
            "credit_amount": credit_amount,
            "payable_amount": payable_amount,
        }