from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.api_key import ApiKeyResponse
from app.services.api_key_service import ApiKeyService

router = APIRouter(
    prefix="/api-key",
    tags=["API Key"],
)


@router.post(
    "/generate",
    response_model=ApiKeyResponse,
)
def generate_api_key(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ApiKeyService.generate(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/me",
    response_model=ApiKeyResponse,
)
def get_my_api_key(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    api_key = ApiKeyService.get_user_api_key(
        db=db,
        user_id=current_user.id,
    )

    return api_key


@router.post(
    "/regenerate",
    response_model=ApiKeyResponse,
)
def regenerate_api_key(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ApiKeyService.generate(
        db=db,
        user_id=current_user.id,
    )