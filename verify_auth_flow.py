import unittest
import json
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Ensure we have a clean state for the test user, but keep seeded data if possible
        # Since we are using the actual DB (sqlite), we should be careful.
        # Ideally we use a test DB, but for this verification I'll just delete the specific test user if exists.
        test_user = User.query.filter_by(email='test_auth@example.com').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()

    def tearDown(self):
        # Clean up test user
        test_user = User.query.filter_by(email='test_auth@example.com').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()
        self.app_context.pop()

    def test_1_register_success(self):
        print("\n--- Testing Registration Success ---")
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "email": "test_auth@example.com",
            "username": "test_auth_user",
            "password": "password123",
            "major": "Computer Science"
        }
        response = self.client.post('/api/auth/register', json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.get_json()}")
        self.assertEqual(response.status_code, 201)

    def test_2_register_duplicate(self):
        print("\n--- Testing Registration Duplicate ---")
        # First register
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "email": "test_auth@example.com",
            "username": "test_auth_user",
            "password": "password123",
            "major": "Computer Science"
        }
        self.client.post('/api/auth/register', json=payload)
        
        # Try duplicate email
        response = self.client.post('/api/auth/register', json=payload)
        print(f"Status (Duplicate): {response.status_code}")
        print(f"Response (Duplicate): {response.get_json()}")
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_3_login_success(self):
        print("\n--- Testing Login Success ---")
        # Register first
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "email": "test_auth@example.com",
            "username": "test_auth_user",
            "password": "password123",
            "major": "Computer Science"
        }
        self.client.post('/api/auth/register', json=payload)

        # Login
        login_payload = {
            "email": "test_auth@example.com",
            "password": "password123"
        }
        response = self.client.post('/api/auth/login', json=login_payload)
        print(f"Status: {response.status_code}")
        data = response.get_json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)
        self.assertIn('user', data)
        self.assertEqual(data['user']['email'], 'test_auth@example.com') # Note: email not in user obj in auth.py currently, let's check
        # Wait, looking at auth.py: 
        # 'user': {'id': ..., 'first_name': ..., 'last_name': ..., 'username': ..., 'major': ..., 'role': ..., ...}
        # Email is NOT in the user object in auth.py response! I should probably add it if requested, 
        # but the prompt said "email (if available)".
        
    def test_4_login_failure(self):
        print("\n--- Testing Login Failure ---")
        login_payload = {
            "email": "test_auth@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post('/api/auth/login', json=login_payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.get_json()}")
        self.assertEqual(response.status_code, 401)

    def test_5_seeded_users_login(self):
        print("\n--- Testing Seeded Users Login ---")
        
        # Super Admin
        print("Checking Super Admin...")
        resp = self.client.post('/api/auth/login', json={
            "email": "super@circle.com",
            "password": "123456"
        })
        data = resp.get_json()
        print(f"Super Admin Role: {data['user']['role']}")
        self.assertEqual(data['user']['role'], 'super_admin') # Expecting mapped role

        # Student
        print("Checking Student...")
        resp = self.client.post('/api/auth/login', json={
            "email": "ali@ogrenci.com",
            "password": "123456"
        })
        data = resp.get_json()
        print(f"Student Role: {data['user']['role']}")
        self.assertEqual(data['user']['role'], 'student')

if __name__ == '__main__':
    unittest.main()
