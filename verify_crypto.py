from app import create_app
from werkzeug.security import check_password_hash

app = create_app()

def verify():
    print(f"Check None hash: {check_password_hash(None, 'anything')}")
    print(f"Check Empty hash: {check_password_hash('', 'anything')}")

if __name__ == "__main__":
    verify()
