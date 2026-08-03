from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.services.reporting.reporting_service import ReportingService

from app.repositories.admin.admin_repository import AdminRepository

from app.reports.email_report import EmailReportService


scheduler = BackgroundScheduler()


def generate_reports():

    db: Session = SessionLocal()

    try:

        # Generate reports
        csv_file = ReportingService.export_csv(db)

        pdf_file = ReportingService.export_pdf(db)

        # Get all admin users
        admins = AdminRepository.get_admin_users(db)

        # Send reports to each admin
        for admin in admins:

            EmailReportService.send_reports(
                recipient=admin.email,
                csv_file=csv_file,
                pdf_file=pdf_file,
            )

        print("Monthly reports generated and emailed successfully.")

    except Exception as e:

        print(f"Report generation failed: {e}")

    finally:

        db.close()


def start_scheduler():

    if not scheduler.running:

        scheduler.add_job(
            generate_reports,
            trigger="cron",
            day=1,
            hour=0,
            minute=0,
            id="monthly_reports",
            replace_existing=True,
        )

        scheduler.start()