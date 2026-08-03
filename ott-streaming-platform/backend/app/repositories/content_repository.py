from sqlalchemy.orm import Session

from app.models.content import Content


class ContentRepository:

    @staticmethod
    def create(
        db: Session,
        content: Content,
    ):
        db.add(content)
        db.commit()
        db.refresh(content)
        return content

    @staticmethod
    def get_all(
        db: Session,
    ):
        return (
            db.query(Content)
            .filter(Content.is_active == True)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        content_id: int,
    ):
        return (
            db.query(Content)
            .filter(Content.id == content_id)
            .first()
        )

    @staticmethod
    def update(db: Session):
        db.commit()

    @staticmethod
    def disable(
        db: Session,
        content_id: int,
    ):
        content = (
            db.query(Content)
            .filter(Content.id == content_id)
            .first()
        )

        if content is None:
            return None

        content.is_active = False

        db.commit()
        db.refresh(content)

        return content