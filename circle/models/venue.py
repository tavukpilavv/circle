from circle.extensions import db
from circle.models.base import BaseModel


class Venue(BaseModel):
    __tablename__ = "venues"

    university_id = db.Column(
        db.String(36), db.ForeignKey("universities.id"), nullable=False, index=True
    )
    campus_id = db.Column(db.String(36), db.ForeignKey("campuses.id"), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)
    venue_type_id = db.Column(db.String(36), db.ForeignKey("venue_types.id"), nullable=True)

    blocks = db.relationship("VenueBlock", backref="venue", lazy=True)

    __table_args__ = (
        db.UniqueConstraint("university_id", "name", name="uq_venue_uni_name"),
    )


class VenueBlock(BaseModel):
    __tablename__ = "venue_blocks"

    venue_id = db.Column(db.String(36), db.ForeignKey("venues.id"), nullable=False)
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        db.CheckConstraint("end_at > start_at", name="ck_block_time"),
    )
