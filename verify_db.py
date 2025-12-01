from app import create_app, db
from app.models import Event

app = create_app()
with app.app_context():
    events = Event.query.all()
    print(f"Total Events: {len(events)}")
    for e in events:
        print(f"- {e.title} (ID: {e.id})")
