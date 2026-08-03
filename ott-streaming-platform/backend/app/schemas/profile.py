from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FavoriteResponse(BaseModel):
    id: int
    title: str
    description: str
    content_type: str
    category: str
    thumbnail: str
    duration: int
    plan_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class WatchHistoryResponse(BaseModel):
    id: int
    title: str
    description: str
    content_type: str
    category: str
    thumbnail: str
    duration: int
    plan_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class FavoriteCreateResponse(BaseModel):
    id: int
    user_id: int
    content_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class UsageResponse(BaseModel):

    movies_used: int
    movies_limit: int

    series_used: int
    series_limit: int

    music_used: int
    music_limit: int