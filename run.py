from app import create_app, db
from app.models import User, Community, Event

app = create_app()

# For flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Community': Community, 'Event': Event}

# Favicon handler (to prevent 404 spam)
@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
