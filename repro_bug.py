from app import create_app, db
from app.models import User
import json

app = create_app()

def test_login():
    with app.app_context():
        user = User.query.filter_by(email="ali@ogrenci.com").first()
        if not user:
            print("User NOT existing")
            return

        print(f"User found: {user.email}")
        print(f"Hash in DB: {user.password_hash}")
        
        # Check manually
        chk = user.check_password("")
        print(f"Manual check_password(''): {chk}")

        client = app.test_client()

        print("--- T1: Correct ---")
        print(f"S:{resp.status_code} D:{resp.get_json()}")

        print("--- T2: Wrong pass ---")
        resp = client.post('/api/auth/login', json={'email': 'ali@ogrenci.com', 'password': 'WRONG'})
        print(f"S:{resp.status_code} D:{resp.get_json()}")
        
        print("--- T3: Username correct pass ---")
        print(f"S:{resp.status_code} D:{resp.get_json()}")

if __name__ == "__main__":
    test_login()
