import uuid
from flask import abort, request
from slugify import slugify
import bleach

from circle.extensions import db
from circle.models.university import University


def resolve_university():
    slug = request.headers.get("X-University")
    if not slug:
        abort(400, description="Missing X-University header")
    university = University.query.filter_by(slug=slug).first()
    if not university:
        abort(404, description="University not found")
    return university


def filter_by_university(query, university_id):
    return query.filter_by(university_id=university_id)


def refresh_public_events_view():
    try:
        db.session.execute(
            "REFRESH MATERIALIZED VIEW CONCURRENTLY mv_public_events"
        )
    except Exception:
        # Fallback if concurrently unsupported
        db.session.execute("REFRESH MATERIALIZED VIEW mv_public_events")
    db.session.commit()


def sanitize_html(value: str | None) -> str | None:
    if value is None:
        return None
    return bleach.clean(
        value,
        tags=["b", "i", "strong", "em", "u", "p", "br", "ul", "li"],
        strip=True,
    )


def generate_slug(value: str) -> str:
    base = slugify(value, lowercase=True)
    return base or str(uuid.uuid4())
