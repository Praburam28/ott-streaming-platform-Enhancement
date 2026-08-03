from fastapi import Header
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.services.streaming_service import StreamingService

router = APIRouter(
    prefix="/stream",
    tags=["Streaming"],
)


@router.get("/video/{content_id}")
def stream_video(
    content_id: int,
    x_api_key: str = Header(...),
    range: str | None = Header(None),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return StreamingService.stream_content(
        db=db,
        user_id=current_user.id,
        content_id=content_id,
        api_key=x_api_key,
        range_header=range,
    )


@router.get("/music/{content_id}")
def stream_music(
    content_id: int,
    x_api_key: str = Header(...),
    range: str | None = Header(None),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return StreamingService.stream_content(
        db=db,
        user_id=current_user.id,
        content_id=content_id,
        api_key=x_api_key,
        range_header=range,
    )