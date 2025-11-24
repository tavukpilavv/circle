from circle.extensions import db
from circle.models.base import BaseModel


class Media(BaseModel):
    __tablename__ = "media"

    event_id = db.Column(db.String(36), db.ForeignKey("events.id"), nullable=True)
    url = db.Column(db.String(512), nullable=False)
    media_type = db.Column(db.String(64), nullable=False)


class EmailLog(BaseModel):
    __tablename__ = "email_logs"

    university_id = db.Column(
        db.String(36), db.ForeignKey("universities.id"), nullable=False, index=True
    )
    to_email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)


class AuditEvent(BaseModel):
    __tablename__ = "audit_events"

    university_id = db.Column(
        db.String(36), db.ForeignKey("universities.id"), nullable=False, index=True
    )
    actor_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    payload = db.Column(db.JSON, nullable=True)
