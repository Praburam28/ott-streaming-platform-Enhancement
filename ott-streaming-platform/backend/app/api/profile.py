from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db

from app.schemas.user import UserResponse
from app.schemas.profile import (
    WatchHistoryResponse,
    FavoriteResponse,
    FavoriteCreateResponse,
    UsageResponse,
)

from app.services.profile_service import ProfileService

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


@router.get(
    "",
    response_model=UserResponse,
)

def get_profile(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ProfileService.get_profile(
        db=db,
        current_user=current_user,
    )


@router.get(
    "/history",
    response_model=list[WatchHistoryResponse],
)
def watch_history(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ProfileService.get_watch_history(
        db=db,
        user_id=current_user.id,
    )


@router.post(
    "/favorites/{content_id}",
    response_model=FavoriteCreateResponse,
)
def add_favorite(
    content_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ProfileService.add_favorite(
        db=db,
        user_id=current_user.id,
        content_id=content_id,
    )


@router.get(
    "/favorites",
    response_model=list[FavoriteResponse],
)
def get_favorites(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ProfileService.get_favorites(
        db=db,
        user_id=current_user.id,
    )
# ======================================
# Usage Metrics
# ======================================

@router.get(
    "/usage",
    response_model=UsageResponse,
)
def get_usage_metrics(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ProfileService.get_usage_metrics(
        db=db,
        user_id=current_user.id,
    )