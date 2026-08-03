from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.content import ContentResponse
from app.services.content_service import ContentService
from app.dependencies.admin import require_admin

router = APIRouter(
    prefix="/content",
    tags=["Content"],
)


# Upload Content (Admin Only)
@router.post(
    "/upload",
    response_model=ContentResponse,
)
def upload_content(
    title: str = Form(...),
    description: str = Form(...),
    content_type: str = Form(...),
    category: str = Form(...),
    duration: int = Form(...),
    plan_id: int = Form(...),
    media_file: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    current_user=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ContentService.upload_content(
        db=db,
        title=title,
        description=description,
        content_type=content_type,
        category=category,
        duration=duration,
        plan_id=plan_id,
        media_file=media_file,
        thumbnail=thumbnail,
    )


# Get All Content
@router.get(
    "/",
    response_model=list[ContentResponse],
)
def list_content(
    db: Session = Depends(get_db),
):
    return ContentService.list_content(db)


# Get Single Content
@router.get(
    "/{content_id}",
    response_model=ContentResponse,
)
def get_content(
    content_id: int,
    db: Session = Depends(get_db),
):
    return ContentService.get_content(
        db,
        content_id,
    )


# Disable Content (Admin Only)
@router.patch(
    "/disable/{content_id}",
    response_model=ContentResponse,
)
def disable_content(
    content_id: int,
    current_user=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ContentService.disable_content(
        db,
        content_id,
    )