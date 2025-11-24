from circle.extensions import db
from circle.models.base import BaseModel


class University(BaseModel):
    __tablename__ = "universities"

    slug = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    campuses = db.relationship("Campus", backref="university", lazy=True)


class Campus(BaseModel):
    __tablename__ = "campuses"

    university_id = db.Column(
        db.String(36),
        db.ForeignKey("universities.id"),
        nullable=False,
        index=True,
    )
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        db.UniqueConstraint(
            "university_id", "name", name="uq_campus_name_uni"
        ),
    )
