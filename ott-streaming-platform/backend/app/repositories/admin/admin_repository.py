from sqlalchemy.orm import Session

from app.models.admin.admin_audit_log import AdminAuditLog
from app.models.admin.subscription_adjustment import SubscriptionAdjustment
from app.models.subscription import Subscription
from app.models.user import User


class AdminRepository:

    # ===========================
    # USER
    # ===========================

    @staticmethod
    def get_user(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    # ===========================
    # SUBSCRIPTION
    # ===========================

    @staticmethod
    def get_subscription(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def update(db: Session):
        db.commit()

    # ===========================
    # AUDIT LOG
    # ===========================

    @staticmethod
    def create_audit_log(
        db: Session,
        audit: AdminAuditLog,
    ):

        db.add(audit)

        db.commit()

        db.refresh(audit)

        return audit

    @staticmethod
    def get_all_logs(
        db: Session,
    ):
        return (
            db.query(AdminAuditLog)
            .order_by(
                AdminAuditLog.timestamp.desc()
            )
            .all()
        )

    # ===========================
    # ADJUSTMENTS
    # ===========================

    @staticmethod
    def create_adjustment(
        db: Session,
        adjustment: SubscriptionAdjustment,
    ):

        db.add(adjustment)

        db.commit()

        db.refresh(adjustment)

        return adjustment

    @staticmethod
    def get_adjustments(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(SubscriptionAdjustment)
            .filter(
                SubscriptionAdjustment.user_id == user_id
            )
            .all()
        )
        
    @staticmethod
    def get_admin_users(db: Session):

        return (
            db.query(User)
            .filter(User.role == "ADMIN")
            .all()
        )
    
    # ===========================
    # ADMIN USERS
    # ===========================

    @staticmethod
    def get_admin_users(
        db: Session,
    ):

        return (
            db.query(User)
            .filter(
                User.role == "admin"
            )
            .all()
        )