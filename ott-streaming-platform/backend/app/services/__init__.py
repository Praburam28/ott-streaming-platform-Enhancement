from datetime import datetime
from sqlalchemy.orm import Session

from app.repositories.reporting.reporting_repository import (
    ReportingRepository,
)


class ReportingService:

    # ==========================================
    # Monthly Revenue Report
    # ==========================================

    @staticmethod
    def monthly_revenue(
        db: Session,
    ):

        today = datetime.now()

        report = ReportingRepository.get_monthly_revenue(
            db=db,
            year=today.year,
            month=today.month,
        )

        return {
            "month": today.strftime("%B %Y"),
            "total_subscriptions": report.total_subscriptions or 0,
            "estimated_revenue": float(
                report.estimated_revenue or 0
            ),
        }

    # ==========================================
    # Active vs Cancelled
    # ==========================================

    @staticmethod
    def subscription_summary(
        db: Session,
    ):

        return ReportingRepository.get_subscription_summary(
            db,
        )

    # ==========================================
    # Plan Distribution
    # ==========================================

    @staticmethod
    def plan_distribution(
        db: Session,
    ):

        plans = ReportingRepository.get_plan_distribution(
            db,
        )

        return [
            {
                "plan_name": plan.plan_name,
                "total_subscriptions": plan.total_subscriptions,
            }
            for plan in plans
        ]