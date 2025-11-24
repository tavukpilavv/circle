import uuid
from datetime import datetime

from circle.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
