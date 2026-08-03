from datetime import datetime

from sqlalchemy import (
    Integer,
    Numeric,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class SubscriptionAdjustment(Base):

    __tablename__ = "subscription_adjustments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    admin_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    discount_amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0,
    )

    credit_amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0,
    )

    reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user = relationship(
        "User",
        foreign_keys=[user_id],
    )

    admin = relationship(
        "User",
        foreign_keys=[admin_user_id],
    )