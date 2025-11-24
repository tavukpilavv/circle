from circle.extensions import db
from circle.models.base import BaseModel


class Event(BaseModel):
    __tablename__ = "events"

    university_id = db.Column(
        db.String(36),
        db.ForeignKey("universities.id"),
        nullable=False,
        index=True,
    )
    club_id = db.Column(
        db.String(36), db.ForeignKey("clubs.id"), nullable=False
    )
    venue_id = db.Column(
        db.String(36), db.ForeignKey("venues.id"), nullable=True
    )
    status_id = db.Column(
        db.String(36), db.ForeignKey("event_statuses.id"), nullable=False
    )
    visibility_type_id = db.Column(
        db.String(36), db.ForeignKey("visibility_types.id"), nullable=True
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=True)
    banner_url = db.Column(db.String(512), nullable=True)

    club = db.relationship("Club", backref="events", lazy=True)
    venue = db.relationship("Venue", backref="events", lazy=True)
    tags = db.relationship("EventTag", backref="event", lazy=True)
    signups = db.relationship("EventSignup", backref="event", lazy=True)
    media_items = db.relationship("Media", backref="event", lazy=True)

    __table_args__ = (
        db.CheckConstraint("end_at > start_at", name="ck_event_time"),
    )


class EventTag(BaseModel):
    __tablename__ = "event_tags"

    event_id = db.Column(
        db.String(36),
        db.ForeignKey("events.id"),
        nullable=False,
    )
    tag_id = db.Column(
        db.String(36),
        db.ForeignKey("tags.id"),
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "event_id",
            "tag_id",
            name="uq_event_tag",
        ),
    )
