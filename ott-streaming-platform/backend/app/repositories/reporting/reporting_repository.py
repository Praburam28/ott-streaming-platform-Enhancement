from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.models.subscription_plan import SubscriptionPlan


class ReportingRepository:

    # ==========================================
    # Monthly Revenue
    # ==========================================

    @staticmethod
    def get_monthly_revenue(
        db: Session,
        year: int,
        month: int,
    ):

        return (
            db.query(
                func.count(Subscription.id).label(
                    "total_subscriptions"
                ),
                func.coalesce(
                    func.sum(SubscriptionPlan.price),
                    0,
                ).label(
                    "estimated_revenue"
                ),
            )
            .join(
                SubscriptionPlan,
                Subscription.plan_id
                == SubscriptionPlan.id,
            )
            .filter(
                func.extract(
                    "year",
                    Subscription.start_date,
                )
                == year,
                func.extract(
                    "month",
                    Subscription.start_date,
                )
                == month,
            )
            .first()
        )

    # ==========================================
    # Active vs Cancelled
    # ==========================================

    @staticmethod
    def get_subscription_summary(
        db: Session,
    ):

        active = (
            db.query(Subscription)
            .filter(
                Subscription.status == "ACTIVE"
            )
            .count()
        )

        cancelled = (
            db.query(Subscription)
            .filter(
                Subscription.status == "CANCELLED"
            )
            .count()
        )

        return {
            "active_subscriptions": active,
            "cancelled_subscriptions": cancelled,
        }

    # ==========================================
    # Plan Distribution
    # ==========================================

    @staticmethod
    def get_plan_distribution(
        db: Session,
    ):

        return (
            db.query(
                SubscriptionPlan.plan_name,
                func.count(
                    Subscription.id
                ).label(
                    "total_subscriptions"
                ),
            )
            .join(
                Subscription,
                Subscription.plan_id
                == SubscriptionPlan.id,
            )
            .group_by(
                SubscriptionPlan.plan_name
            )
            .all()
        )