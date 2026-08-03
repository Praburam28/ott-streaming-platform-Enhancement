from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.schemas.user import UserSignup, UserLogin, UserResponse
from app.schemas.auth import Token
from app.services.auth_service import AuthService
from app.core.security import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=201
)
def signup(
    user: UserSignup,
    db: Session = Depends(get_db)
):
    return AuthService.signup(db, user)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return AuthService.login(
        db=db,
        form_data=form_data,
    )

@router.get(
    "/me",
    response_model=UserResponse
)
def get_profile(
    current_user=Depends(get_current_user)
):
    return current_user