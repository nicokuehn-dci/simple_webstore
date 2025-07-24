"""
Simple Password Hash Utility
"""
import hashlib


def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(password) == hashed


# Demo passwords for testing
DEMO_PASSWORDS = {
    'admin': hash_password('admin123'),
    'customer': hash_password('customer123')
}
