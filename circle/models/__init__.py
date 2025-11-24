from circle import extensions
from circle.models import base  # noqa: F401
from circle.models import (  # noqa: F401
    club,
    event,
    lookups,
    media,
    signup,
    university,
    user,
    venue,
)


def register_models():
    # Importing ensures model registration with SQLAlchemy metadata
    _ = (
        base,
        lookups,
        university,
        user,
        club,
        venue,
        event,
        signup,
        media,
    )
    return extensions.db


__all__ = ["register_models"]
