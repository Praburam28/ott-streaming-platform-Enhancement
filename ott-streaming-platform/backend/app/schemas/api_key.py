from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApiKeyResponse(BaseModel):
    api_key: str
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)