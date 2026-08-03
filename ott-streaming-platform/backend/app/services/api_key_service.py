import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.api_key import ApiKey
from app.repositories.api_key_repository import ApiKeyRepository


class ApiKeyService:

    EXPIRY_DAYS = 365

    @staticmethod
    def generate(
        db: Session,
        user_id: int,
    ):

        existing = ApiKeyRepository.get_by_user(
            db,
            user_id,
        )

        api_key = secrets.token_hex(32)

        expires_at = datetime.utcnow() + timedelta(
            days=ApiKeyService.EXPIRY_DAYS
        )

        if existing:

            existing.api_key = api_key
            existing.expires_at = expires_at
            existing.is_active = True

            ApiKeyRepository.update(db)

            return existing

        new_key = ApiKey(
            user_id=user_id,
            api_key=api_key,
            expires_at=expires_at,
            is_active=True,
        )

        return ApiKeyRepository.create(
            db,
            new_key,
        )

    @staticmethod
    def get_user_api_key(
        db: Session,
        user_id: int,
    ):

        key = ApiKeyRepository.get_by_user(
            db,
            user_id,
        )

        if key is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API Key not found.",
            )

        return key

    @staticmethod
    def validate(
        db: Session,
        api_key: str,
    ):

        print("=" * 60)
        print("Received API Key:", api_key)

        key = ApiKeyRepository.get_by_key(
            db,
            api_key,
        )

        print("Database Result:", key)

        if key:
            print("DB Key:", key.api_key)
            print("Active:", key.is_active)
            print("Expires:", key.expires_at)

        print("=" * 60)

        if key is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key.",
            )

        if not key.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key is inactive.",
            )

        if key.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key expired.",
            )

        return key