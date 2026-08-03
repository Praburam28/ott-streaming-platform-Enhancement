import random


class PaymentService:

    @staticmethod
    def process_payment():

        success = random.choice([True, False])

        if success:

            return {
                "success": True,
                "message": "Payment Successful"
            }

        return {
            "success": False,
            "message": "Payment Failed"
        }