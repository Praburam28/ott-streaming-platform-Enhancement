from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.schemas.user import UserSignup
from app.schemas.auth import Token

from app.repositories.user_repository import UserRepository

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:
    """
    Business logic for authentication.
    """

    @staticmethod
    def signup(
        db: Session,
        user_data: UserSignup,
    ):

        existing_user = UserRepository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password=hash_password(user_data.password),
            role="user",
            is_active=True,
        )

        created_user = UserRepository.create(
            db,
            new_user,
        )

        return created_user

    @staticmethod
    def login(
        db: Session,
        form_data: OAuth2PasswordRequestForm,
    ) -> Token:

        user = UserRepository.get_by_email(
            db,
            form_data.username,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not verify_password(
            form_data.password,
            user.password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )