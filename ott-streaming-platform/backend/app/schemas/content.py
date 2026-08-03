from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ContentResponse(BaseModel):
    id: int
    title: str
    description: str
    content_type: str
    category: str
    file_name: str
    thumbnail: str
    duration: int
    plan_id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)