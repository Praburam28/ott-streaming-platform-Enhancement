import os
import smtplib

from email.message import EmailMessage


class EmailReportService:

    SMTP_SERVER = "smtp.gmail.com"

    SMTP_PORT = 587

    EMAIL = "YOUR_EMAIL@gmail.com"

    PASSWORD = "YOUR_APP_PASSWORD"

    @classmethod
    def send_reports(
        cls,
        recipient: str,
        csv_file: str,
        pdf_file: str,
    ):

        message = EmailMessage()

        message["Subject"] = (
            "OTT Streaming Platform Monthly Reports"
        )

        message["From"] = cls.EMAIL

        message["To"] = recipient

        message.set_content(
            "Monthly reports are attached."
        )

        for file_path in [csv_file, pdf_file]:

            with open(file_path, "rb") as file:

                message.add_attachment(
                    file.read(),
                    maintype="application",
                    subtype="octet-stream",
                    filename=os.path.basename(file_path),
                )

        with smtplib.SMTP(
            cls.SMTP_SERVER,
            cls.SMTP_PORT,
        ) as smtp:

            smtp.starttls()

            smtp.login(
                cls.EMAIL,
                cls.PASSWORD,
            )

            smtp.send_message(message)