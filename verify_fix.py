from app import create_app, db
from app.models import User
import sys

app = create_app()

def run_test():
    with app.app_context():
        # Ensure user exists
        user = User.query.filter_by(email="ali@ogrenci.com").first()
        if not user:
            print("User ali@ogrenci.com not found. Seed required.")
            sys.exit(1)

        client = app.test_client()
        success = True

        # 1. Login with proper email + pass
        resp = client.post('/api/auth/login', json={'email': 'ali@ogrenci.com', 'password': '123456'})
        if resp.status_code == 200:
            print("PASS: Email login success")
        else:
            print(f"FAIL: Email login returned {resp.status_code}")
            success = False

        # 2. Login with correct username + pass
        resp = client.post('/api/auth/login', json={'username': 'aliy', 'password': '123456'})
        if resp.status_code == 200:
            print("PASS: Username login success")
        else:
            print(f"FAIL: Username login returned {resp.status_code}")
            success = False

        # 3. Login with correct email + WRONG pass
        resp = client.post('/api/auth/login', json={'email': 'ali@ogrenci.com', 'password': 'WRONG'})
        if resp.status_code == 401:
            print("PASS: Wrong password rejected")
        else:
            print(f"FAIL: Wrong password returned {resp.status_code} (Should be 401)")
            success = False

        # 4. Login with non-existing user
        resp = client.post('/api/auth/login', json={'email': 'ghost@user.com', 'password': '123'})
        if resp.status_code == 401:
            print("PASS: Ghost user rejected")
        else:
            print(f"FAIL: Ghost user returned {resp.status_code}")
            success = False
            
        # 5. Login without password
        resp = client.post('/api/auth/login', json={'email': 'ali@ogrenci.com'})
        if resp.status_code == 400:
            print("PASS: Missing password rejected")
        else:
            print(f"FAIL: Missing password returned {resp.status_code} (Should be 400 or 401)")
            success = False

        if success:
            print("\nALL CHECKS PASSED")
            sys.exit(0)
        else:
            print("\nSOME CHECKS FAILED")
            sys.exit(1)

if __name__ == "__main__":
    run_test()
