import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


class PDFReportGenerator:

    REPORT_FOLDER = "reports_output"

    @classmethod
    def create_directory(cls):
        if not os.path.exists(cls.REPORT_FOLDER):
            os.makedirs(cls.REPORT_FOLDER)

    @classmethod
    def generate_report(
        cls,
        monthly_revenue,
        subscription_summary,
        plan_distribution,
    ):

        cls.create_directory()

        filename = (
            f"{cls.REPORT_FOLDER}/reports_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        document = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        elements = []

        # ======================================
        # Title
        # ======================================

        elements.append(
            Paragraph(
                "OTT Streaming Platform Report",
                styles["Heading1"],
            )
        )

        elements.append(Spacer(1, 20))

        # ======================================
        # Monthly Revenue
        # ======================================

        elements.append(
            Paragraph(
                "Monthly Revenue Report",
                styles["Heading2"],
            )
        )

        revenue_table = Table(
            [
                [
                    "Month",
                    "Subscriptions",
                    "Estimated Revenue",
                ],
                [
                    monthly_revenue["month"],
                    str(monthly_revenue["total_subscriptions"]),
                    f"₹ {monthly_revenue['estimated_revenue']:.2f}",
                ],
            ]
        )

        revenue_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )

        elements.append(revenue_table)

        elements.append(Spacer(1, 20))

        # ======================================
        # Subscription Summary
        # ======================================

        elements.append(
            Paragraph(
                "Active vs Cancelled Subscriptions",
                styles["Heading2"],
            )
        )

        summary_table = Table(
            [
                [
                    "Active",
                    "Cancelled",
                ],
                [
                    str(subscription_summary["active_subscriptions"]),
                    str(subscription_summary["cancelled_subscriptions"]),
                ],
            ]
        )

        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )

        elements.append(summary_table)

        elements.append(Spacer(1, 20))

        # ======================================
        # Plan Distribution
        # ======================================

        elements.append(
            Paragraph(
                "Plan-wise Subscription Distribution",
                styles["Heading2"],
            )
        )

        data = [
            [
                "Plan",
                "Subscriptions",
            ]
        ]

        for plan in plan_distribution:

            data.append(
                [
                    plan["plan_name"],
                    str(plan["total_subscriptions"]),
                ]
            )

        plan_table = Table(data)

        plan_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )

        elements.append(plan_table)

        document.build(elements)

        return filename