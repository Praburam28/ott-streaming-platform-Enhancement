import os
import shutil

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.content import Content
from app.repositories.content_repository import ContentRepository


class ContentService:

    VIDEO_FOLDER = "app/uploads/videos"
    MUSIC_FOLDER = "app/uploads/music"
    THUMBNAIL_FOLDER = "app/uploads/thumbnails"

    @staticmethod
    def upload_content(
        db: Session,
        title: str,
        description: str,
        content_type: str,
        category: str,
        duration: int,
        plan_id: int,
        media_file: UploadFile,
        thumbnail: UploadFile,
    ):

        folder = (
            ContentService.MUSIC_FOLDER
            if content_type.upper() == "MUSIC"
            else ContentService.VIDEO_FOLDER
        )

        os.makedirs(folder, exist_ok=True)
        os.makedirs(
            ContentService.THUMBNAIL_FOLDER,
            exist_ok=True,
        )

        media_path = os.path.join(
            folder,
            media_file.filename,
        )

        with open(media_path, "wb") as buffer:
            shutil.copyfileobj(
                media_file.file,
                buffer,
            )

        thumbnail_path = os.path.join(
            ContentService.THUMBNAIL_FOLDER,
            thumbnail.filename,
        )

        with open(thumbnail_path, "wb") as buffer:
            shutil.copyfileobj(
                thumbnail.file,
                buffer,
            )

        content = Content(
            title=title,
            description=description,
            content_type=content_type.upper(),
            category=category,
            duration=duration,
            plan_id=plan_id,
            file_name=media_file.filename,
            thumbnail=thumbnail.filename,
            is_active=True,
        )

        return ContentRepository.create(
            db,
            content,
        )

    @staticmethod
    def list_content(
        db: Session,
    ):
        return ContentRepository.get_all(db)

    @staticmethod
    def get_content(
        db: Session,
        content_id: int,
    ):

        content = ContentRepository.get_by_id(
            db,
            content_id,
        )

        if content is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found.",
            )

        if not content.is_active:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content is disabled.",
            )

        return content

    @staticmethod
    def disable_content(
        db: Session,
        content_id: int,
    ):

        content = ContentRepository.get_by_id(
            db,
            content_id,
        )

        if content is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found.",
            )

        content.is_active = False

        ContentRepository.update(db)

        return content