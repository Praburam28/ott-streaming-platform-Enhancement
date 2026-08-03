from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class WatchHistory(Base):
    __tablename__ = "watch_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    content_id: Mapped[int] = mapped_column(
        ForeignKey("contents.id"),
        nullable=False,
    )

    watched_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    progress: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    user = relationship(
        "User",
        back_populates="watch_history",
    )

    content = relationship(
        "Content",
    )