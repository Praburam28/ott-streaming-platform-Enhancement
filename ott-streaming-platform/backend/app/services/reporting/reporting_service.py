from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.reporting.reporting_repository import (
    ReportingRepository,
)
from app.reports.csv_report import CSVReportGenerator
from app.reports.pdf_report import PDFReportGenerator


class ReportingService:

    # ==========================================
    # Monthly Revenue
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
    # Subscription Summary
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

    # ==========================================
    # Export CSV
    # ==========================================

    @staticmethod
    def export_csv(
        db: Session,
    ):

        monthly = ReportingService.monthly_revenue(db)

        summary = ReportingService.subscription_summary(db)

        distribution = ReportingService.plan_distribution(db)

        return CSVReportGenerator.generate_report(
            monthly,
            summary,
            distribution,
        )

    # ==========================================
    # Export PDF
    # ==========================================

    @staticmethod
    def export_pdf(
        db: Session,
    ):

        monthly = ReportingService.monthly_revenue(db)

        summary = ReportingService.subscription_summary(db)

        distribution = ReportingService.plan_distribution(db)

        return PDFReportGenerator.generate_report(
            monthly,
            summary,
            distribution,
        )