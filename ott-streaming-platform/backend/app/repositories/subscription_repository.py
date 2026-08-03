from datetime import datetime

from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.models.subscription_plan import SubscriptionPlan


class SubscriptionRepository:

    @staticmethod
    def get_all_plans(db: Session):
        return db.query(SubscriptionPlan).all()

    @staticmethod
    def get_plan_by_id(db: Session, plan_id: int):
        return (
            db.query(SubscriptionPlan)
            .filter(SubscriptionPlan.id == plan_id)
            .first()
        )

    @staticmethod
    def get_user_subscription(db: Session, user_id: int):
        return (
            db.query(Subscription)
            .filter(Subscription.user_id == user_id)
            .first()
        )

    @staticmethod
    def get_active_subscription(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "ACTIVE",
                Subscription.end_date >= datetime.utcnow(),
            )
            .first()
        )

    @staticmethod
    def create_subscription(
        db: Session,
        subscription: Subscription,
    ):
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        return subscription

    @staticmethod
    def update_subscription(db: Session):
        db.commit()

    @staticmethod
    def cancel_subscription(db: Session):
        db.commit()
        
    @staticmethod
    def get_subscription_plan(
        db: Session,
        plan_id: int,
    ):
        return (
            db.query(SubscriptionPlan)
            .filter(
                SubscriptionPlan.id == plan_id
            )
            .first()
        )