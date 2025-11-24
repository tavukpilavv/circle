from circle.extensions import db
from circle.models.base import BaseModel


class EventSignup(BaseModel):
    __tablename__ = "event_signups"

    event_id = db.Column(db.String(36), db.ForeignKey("events.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    status_id = db.Column(db.String(36), db.ForeignKey("signup_statuses.id"), nullable=False)
    waitlist_position = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.UniqueConstraint("event_id", "email", name="uq_signup_event_email"),
    )


class WaitlistPromotion(BaseModel):
    __tablename__ = "waitlist_promotions"

    signup_id = db.Column(db.String(36), db.ForeignKey("event_signups.id"), nullable=False)
    promoted_at = db.Column(db.DateTime, nullable=False)


class Checkin(BaseModel):
    __tablename__ = "checkins"

    signup_id = db.Column(db.String(36), db.ForeignKey("event_signups.id"), nullable=False)
    checked_in_at = db.Column(db.DateTime, nullable=False)
