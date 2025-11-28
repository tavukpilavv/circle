from app import create_app, db
from app.models import User, Community, Event

app = create_app()

# Otomatik importlar (flask shell için)
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Community': Community, 'Event': Event}

if __name__ == '__main__':
    app.run(debug=True, port=5000)