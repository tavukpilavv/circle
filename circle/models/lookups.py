from circle.extensions import db
from circle.models.base import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    key = db.Column(db.String(64), unique=True, nullable=False)
    label = db.Column(db.String(128), nullable=False)


class VisibilityType(BaseModel):
    __tablename__ = "visibility_types"

    key = db.Column(db.String(64), unique=True, nullable=False)
    label = db.Column(db.String(128), nullable=False)


class EventStatus(BaseModel):
    __tablename__ = "event_statuses"

    key = db.Column(db.String(32), unique=True, nullable=False)
    label = db.Column(db.String(128), nullable=False)


class SignupStatus(BaseModel):
    __tablename__ = "signup_statuses"

    key = db.Column(db.String(32), unique=True, nullable=False)
    label = db.Column(db.String(128), nullable=False)


class VenueType(BaseModel):
    __tablename__ = "venue_types"

    key = db.Column(db.String(64), unique=True, nullable=False)
    label = db.Column(db.String(128), nullable=False)


class Tag(BaseModel):
    __tablename__ = "tags"

    university_id = db.Column(
        db.String(36),
        db.ForeignKey("universities.id"),
        nullable=False,
        index=True,
    )
    key = db.Column(db.String(64), nullable=False)
    label = db.Column(db.String(128), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("university_id", "key", name="uq_tag_uni_key"),
    )
