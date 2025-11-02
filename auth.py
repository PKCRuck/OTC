import hashlib
import json
import os

AUTH_FILE = "data/auth.json"

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def ensure_auth_file():
    """Ensure the auth file exists with a default password."""
    if not os.path.exists(AUTH_FILE):
        os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)
        # Default password is "admin123"
        default_config = {
            "password_hash": hash_password("admin123")
        }
        with open(AUTH_FILE, 'w') as f:
            json.dump(default_config, f, indent=2)

def verify_password(password: str) -> bool:
    """Verify a password against the stored hash."""
    ensure_auth_file()
    with open(AUTH_FILE, 'r') as f:
        config = json.load(f)

    return hash_password(password) == config['password_hash']

def change_password(old_password: str, new_password: str) -> bool:
    """Change the admin password."""
    if not verify_password(old_password):
        return False

    ensure_auth_file()
    with open(AUTH_FILE, 'r') as f:
        config = json.load(f)

    config['password_hash'] = hash_password(new_password)

    with open(AUTH_FILE, 'w') as f:
        json.dump(config, f, indent=2)

    return True

def get_default_password_info() -> str:
    """Return info about the default password if it's still in use."""
    ensure_auth_file()
    if verify_password("admin123"):
        return "⚠️ You are using the default password: **admin123**. Please change it immediately!"
    return ""
