import os
import sys
import socket
from urllib.parse import urlparse
import psycopg2

def verify_connection():
    database_url = os.environ.get('DATABASE_URL')
    
    print("--- Database Connection Verification ---")
    
    if not database_url:
        print("❌ Error: DATABASE_URL environment variable is not set.")
        return

    # Mask password for printing
    try:
        parsed = urlparse(database_url)
        safe_url = f"{parsed.scheme}://{parsed.username}:****@{parsed.hostname}:{parsed.port}{parsed.path}"
        print(f"Checking connection to: {safe_url}")
        
        hostname = parsed.hostname
        port = parsed.port or 5432
        
        print(f"\n1. Resolving hostname: {hostname}")
        try:
            ip_address = socket.gethostbyname(hostname)
            print(f"   ✅ Hostname resolved to: {ip_address}")
        except socket.gaierror as e:
            print(f"   ❌ DNS Resolution Failed: {e}")
            print("   -> This usually means the hostname is incorrect or the service is not accessible from this environment.")
            return

        print(f"\n2. Attempting TCP connection to {hostname}:{port}...")
        try:
            sock = socket.create_connection((hostname, port), timeout=5)
            print("   ✅ TCP Connection successful")
            sock.close()
        except Exception as e:
            print(f"   ❌ TCP Connection Failed: {e}")
            return

        print(f"\n3. Attempting PostgreSQL authentication...")
        try:
            conn = psycopg2.connect(database_url)
            print("   ✅ Database authentication successful!")
            conn.close()
        except psycopg2.OperationalError as e:
            print(f"   ❌ Authentication/Operational Error: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected Error: {e}")

    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")

if __name__ == "__main__":
    verify_connection()
