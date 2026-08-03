from sqlalchemy.orm import Session

from app.repositories.profile_repository import ProfileRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.api_key_repository import ApiKeyRepository


class ProfileService:

    @staticmethod
    def get_profile(
        db: Session,
        current_user,
    ):

        subscription = SubscriptionRepository.get_active_subscription(
            db=db,
            user_id=current_user.id,
        )

        api_key = ApiKeyRepository.get_by_user(
            db=db,
            user_id=current_user.id,
        )

        return {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "role": current_user.role,
            "is_active": current_user.is_active,
            "subscription": (
                subscription.plan.plan_name
                if subscription
                else "Free"
            ),
            "api_key": (
                api_key.api_key
                if api_key
                else ""
            ),
        }

    @staticmethod
    def get_watch_history(
        db: Session,
        user_id: int,
    ):
        return ProfileRepository.get_watch_history(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def add_favorite(
        db: Session,
        user_id: int,
        content_id: int,
    ):
        return ProfileRepository.add_favorite(
            db=db,
            user_id=user_id,
            content_id=content_id,
        )

    @staticmethod
    def get_favorites(
        db: Session,
        user_id: int,
    ):
        return ProfileRepository.get_favorites(
            db=db,
            user_id=user_id,
        )
        
    # ======================================
    # Usage Metrics
    # ======================================

    @staticmethod
    def get_usage_metrics(
        db: Session,
        user_id: int,
    ):

        return ProfileRepository.get_usage_metrics(
            db=db,
            user_id=user_id,
        )