from sqlalchemy import create_engine

from app.core.config import settings

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)