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
        chk = user.check_password("123456")
        print(f"Manual check_password('123456'): {chk}")

        client = app.test_client()

        print("--- T1: Correct ---")
        resp = client.post('/api/auth/login', json={'email': 'ali@ogrenci.com', 'password': '123456'})
        print(f"S:{resp.status_code} D:{resp.get_json()}")

        print("--- T2: Wrong pass ---")
        resp = client.post('/api/auth/login', json={'email': 'ali@ogrenci.com', 'password': 'WRONG'})
        print(f"S:{resp.status_code} D:{resp.get_json()}")
        
        print("--- T3: Username correct pass ---")
        resp = client.post('/api/auth/login', json={'username': 'aliy', 'password': '123456'})
        print(f"S:{resp.status_code} D:{resp.get_json()}")

if __name__ == "__main__":
    test_login()
