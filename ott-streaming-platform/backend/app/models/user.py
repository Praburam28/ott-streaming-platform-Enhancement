from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(120), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    role = Column(String(20), default="user")

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    
    subscriptions = relationship(
    "Subscription",
    back_populates="user"
    ) 
    
    api_keys = relationship(
    "ApiKey",
    back_populates="user"
    )
    
    watch_history = relationship(
    "WatchHistory",
    back_populates="user",
    )
    
    favorites = relationship(
    "Favorite",
    back_populates="user",
    )
    
    