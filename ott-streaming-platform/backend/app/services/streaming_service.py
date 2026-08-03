import mimetypes
import os

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.repositories.content_repository import ContentRepository
from app.repositories.profile_repository import ProfileRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.api_key_service import ApiKeyService


class StreamingService:

    VIDEO_FOLDER = "app/uploads/videos"
    MUSIC_FOLDER = "app/uploads/music"

    CHUNK_SIZE = 1024 * 1024  # 1 MB

    @staticmethod
    def stream_content(
        db: Session,
        user_id: int,
        content_id: int,
        api_key: str,
        range_header: str | None,
    ):
        """
        Stream video/music after validating:
        - JWT
        - API Key
        - Subscription
        - Content
        - User Plan

        Also records watch history.
        """

        # ----------------------------------------------------
        # Validate API Key
        # ----------------------------------------------------
        ApiKeyService.validate(
            db=db,
            api_key=api_key,
        )

        # ----------------------------------------------------
        # Validate Subscription
        # ----------------------------------------------------
        subscription = SubscriptionRepository.get_user_subscription(
            db,
            user_id,
        )

        if subscription is None:
            raise HTTPException(
                status_code=403,
                detail="No active subscription.",
            )

        # ----------------------------------------------------
        # Get Content
        # ----------------------------------------------------
        content = ContentRepository.get_by_id(
            db,
            content_id,
        )

        if content is None:
            raise HTTPException(
                status_code=404,
                detail="Content not found.",
            )

        # ----------------------------------------------------
        # Content Status
        # ----------------------------------------------------
        if not content.is_active:
            raise HTTPException(
                status_code=403,
                detail="Content is disabled.",
            )

        # ----------------------------------------------------
        # Subscription Plan Validation
        # ----------------------------------------------------
        if subscription.plan_id < content.plan_id:
            raise HTTPException(
                status_code=403,
                detail="Upgrade your subscription plan.",
            )

        # ----------------------------------------------------
        # Determine File Location
        # ----------------------------------------------------
        if content.content_type.upper() == "MUSIC":
            folder = StreamingService.MUSIC_FOLDER
        else:
            folder = StreamingService.VIDEO_FOLDER

        file_path = os.path.join(
            folder,
            content.file_name,
        )

        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="Media file not found.",
            )

        # ----------------------------------------------------
        # Save Watch History
        # ----------------------------------------------------
        ProfileRepository.save_watch_history(
            db=db,
            user_id=user_id,
            content_id=content_id,
        )

        # ----------------------------------------------------
        # Range Streaming
        # ----------------------------------------------------
        file_size = os.path.getsize(file_path)

        start = 0
        end = file_size - 1

        if range_header:

            range_header = range_header.replace(
                "bytes=",
                "",
            )

            start_end = range_header.split("-")

            if start_end[0]:
                start = int(start_end[0])

            if len(start_end) > 1 and start_end[1]:
                end = int(start_end[1])

        length = end - start + 1

        def file_iterator():

            with open(file_path, "rb") as media:

                media.seek(start)

                remaining = length

                while remaining > 0:

                    read_size = min(
                        StreamingService.CHUNK_SIZE,
                        remaining,
                    )

                    data = media.read(read_size)

                    if not data:
                        break

                    remaining -= len(data)

                    yield data

        media_type = (
            mimetypes.guess_type(file_path)[0]
            or "application/octet-stream"
        )

        headers = {
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Content-Length": str(length),
        }

        return StreamingResponse(
            file_iterator(),
            status_code=206,
            media_type=media_type,
            headers=headers,
        )