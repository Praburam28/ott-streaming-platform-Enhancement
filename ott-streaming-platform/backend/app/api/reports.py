from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.admin import require_admin

from app.schemas.reporting.report import (
    MonthlyRevenueReport,
    SubscriptionSummaryReport,
    PlanDistributionReport,
)
from app.services.reporting.reporting_service import ReportingService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


# ==========================================
# Monthly Revenue Report
# ==========================================

@router.get(
    "/monthly-revenue",
    response_model=MonthlyRevenueReport,
)
def monthly_revenue(
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ReportingService.monthly_revenue(db)


# ==========================================
# Subscription Summary Report
# ==========================================

@router.get(
    "/subscription-summary",
    response_model=SubscriptionSummaryReport,
)
def subscription_summary(
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ReportingService.subscription_summary(db)


# ==========================================
# Plan Distribution Report
# ==========================================

@router.get(
    "/plan-distribution",
    response_model=list[PlanDistributionReport],
)
def plan_distribution(
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ReportingService.plan_distribution(db)


# ==========================================
# Export Monthly Revenue CSV
# ==========================================

@router.get("/export/csv")
def export_csv(
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):

    file_path = ReportingService.export_csv(
        db
    )

    return FileResponse(
        path=file_path,
        filename="reports.csv",
        media_type="text/csv",
    )
    
     
@router.get("/export/pdf")
def export_pdf(
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):

    file_path = ReportingService.export_pdf(
        db
    )

    return FileResponse(
        path=file_path,
        filename="reports.pdf",
        media_type="application/pdf",
    )