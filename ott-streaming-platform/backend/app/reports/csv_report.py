import csv
import os
from datetime import datetime


class CSVReportGenerator:

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
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            # -------------------------
            # Monthly Revenue
            # -------------------------

            writer.writerow(["MONTHLY REVENUE REPORT"])
            writer.writerow(
                [
                    "Month",
                    "Subscriptions",
                    "Estimated Revenue",
                ]
            )

            writer.writerow(
                [
                    monthly_revenue["month"],
                    monthly_revenue["total_subscriptions"],
                    monthly_revenue["estimated_revenue"],
                ]
            )

            writer.writerow([])

            # -------------------------
            # Subscription Summary
            # -------------------------

            writer.writerow(
                ["ACTIVE VS CANCELLED"]
            )

            writer.writerow(
                [
                    "Active",
                    "Cancelled",
                ]
            )

            writer.writerow(
                [
                    subscription_summary["active_subscriptions"],
                    subscription_summary["cancelled_subscriptions"],
                ]
            )

            writer.writerow([])

            # -------------------------
            # Plan Distribution
            # -------------------------

            writer.writerow(
                ["PLAN DISTRIBUTION"]
            )

            writer.writerow(
                [
                    "Plan",
                    "Subscriptions",
                ]
            )

            for plan in plan_distribution:

                writer.writerow(
                    [
                        plan["plan_name"],
                        plan["total_subscriptions"],
                    ]
                )

        return filename