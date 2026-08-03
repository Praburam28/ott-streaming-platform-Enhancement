from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.favorite import Favorite
from app.models.watch_history import WatchHistory
from app.models.content import Content


class ProfileRepository:

    @staticmethod
    def save_watch_history(
        db: Session,
        user_id: int,
        content_id: int,
    ):
        history = (
            db.query(WatchHistory)
            .filter(
                WatchHistory.user_id == user_id,
                WatchHistory.content_id == content_id,
            )
            .first()
        )

        if history:
            history.watched_at = datetime.utcnow()
            db.commit()
            db.refresh(history)
            return history

        history = WatchHistory(
            user_id=user_id,
            content_id=content_id,
            progress=0,
        )

        db.add(history)
        db.commit()
        db.refresh(history)

        return history

    @staticmethod
    def get_watch_history(
    db: Session,
    user_id: int,
    ):
        return (
        db.query(Content)
        .join(
            WatchHistory,
            WatchHistory.content_id == Content.id
        )
        .filter(
            WatchHistory.user_id == user_id,
            Content.is_active == True
        )
        .order_by(
            WatchHistory.watched_at.desc()
        )
        .all()
    )

    @staticmethod
    def add_favorite(
        db: Session,
        user_id: int,
        content_id: int,
    ):
        favorite = (
            db.query(Favorite)
            .filter(
                Favorite.user_id == user_id,
                Favorite.content_id == content_id,
            )
            .first()
        )

        if favorite:
            return favorite

        favorite = Favorite(
            user_id=user_id,
            content_id=content_id,
        )

        db.add(favorite)
        db.commit()
        db.refresh(favorite)

        return favorite

    @staticmethod
    def get_favorites(
    db: Session,
    user_id: int,
    ):
        return (
        db.query(Content)
        .join(
            Favorite,
            Favorite.content_id == Content.id
        )
        .filter(
            Favorite.user_id == user_id,
            Content.is_active == True
        )
        .all()
    )

    @staticmethod
    def get_usage_metrics(
        db: Session,
        user_id: int,
    ):

        movie_count = (
            db.query(func.count(WatchHistory.id))
            .join(
                Content,
                WatchHistory.content_id == Content.id,
            )
            .filter(
                WatchHistory.user_id == user_id,
                Content.content_type == "movie",
                Content.is_active == True,
            )
            .scalar()
        )

        series_count = (
            db.query(func.count(WatchHistory.id))
            .join(
                Content,
                WatchHistory.content_id == Content.id,
            )
            .filter(
                WatchHistory.user_id == user_id,
                Content.content_type == "series",
                Content.is_active == True,
            )
            .scalar()
        )

        music_count = (
            db.query(func.count(WatchHistory.id))
            .join(
                Content,
                WatchHistory.content_id == Content.id,
            )
            .filter(
                WatchHistory.user_id == user_id,
                Content.content_type == "music",
                Content.is_active == True,
            )
            .scalar()
        )

        return {
            "movies_used": movie_count or 0,
            "movies_limit": 100,
            "series_used": series_count or 0,
            "series_limit": 50,
            "music_used": music_count or 0,
            "music_limit": 100,
        }