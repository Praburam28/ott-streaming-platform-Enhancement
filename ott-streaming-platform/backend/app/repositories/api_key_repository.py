from sqlalchemy.orm import Session

from app.models.api_key import ApiKey


class ApiKeyRepository:

    @staticmethod
    def get_by_user(db: Session, user_id: int):

        return (
            db.query(ApiKey)
            .filter(ApiKey.user_id == user_id)
            .first()
        )

    @staticmethod
    def get_by_key(db: Session, api_key: str):

        return (
            db.query(ApiKey)
            .filter(ApiKey.api_key == api_key)
            .first()
        )

    @staticmethod
    def create(db: Session, api_key: ApiKey):

        db.add(api_key)

        db.commit()

        db.refresh(api_key)

        return api_key

    @staticmethod
    def update(db: Session):

        db.commit()

@staticmethod
def validate(
    db: Session,
    api_key: str,
):

    print("=" * 60)
    print("Received API Key:", api_key)

    key = ApiKeyRepository.get_by_key(
        db,
        api_key,
    )

    print("Database Result:", key)
    print("=" * 60)

    if key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key.",
        )

    if not key.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is inactive.",
        )

    if key.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key expired.",
        )

    return key