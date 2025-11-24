from circle.extensions import db
from circle.models.base import BaseModel


class Club(BaseModel):
    __tablename__ = "clubs"

    university_id = db.Column(
        db.String(36),
        db.ForeignKey("universities.id"),
        nullable=False,
        index=True,
    )
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)

    memberships = db.relationship("ClubMembership", backref="club", lazy=True)

    __table_args__ = (
        db.UniqueConstraint(
            "university_id", "slug", name="uq_clubs_uni_slug"
        ),
    )


class ClubMembership(BaseModel):
    __tablename__ = "club_memberships"

    club_id = db.Column(
        db.String(36), db.ForeignKey("clubs.id"), nullable=False
    )
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False
    )
    role = db.Column(db.String(64), nullable=True)

    __table_args__ = (
        db.UniqueConstraint("club_id", "user_id", name="uq_club_user"),
    )
