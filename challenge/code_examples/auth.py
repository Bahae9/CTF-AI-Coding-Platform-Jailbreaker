"""
auth.py — Learnify authentication utilities
Reference implementation for the platform backend.
"""
import hashlib
import hmac
import os
import time
from typing import Optional


def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """
    Hash a password using PBKDF2-HMAC-SHA256.
    Returns (hashed_password, salt).
    """
    if salt is None:
        salt = os.urandom(16).hex()
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000)
    return dk.hex(), salt


def verify_password(password: str, hashed: str, salt: str) -> bool:
    """Constant-time password verification to prevent timing attacks."""
    candidate, _ = hash_password(password, salt)
    return hmac.compare_digest(candidate, hashed)


def generate_token(user_id: int, secret: str, ttl: int = 3600) -> str:
    """
    Generate a simple signed token: base64(user_id:expires:hmac).
    Not for production — use a proper JWT library instead.
    """
    expires = int(time.time()) + ttl
    payload = f"{user_id}:{expires}"
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"


def verify_token(token: str, secret: str) -> Optional[int]:
    """Verify a token and return the user_id, or None if invalid/expired."""
    try:
        user_id_str, expires_str, sig = token.split(":")
        payload = f"{user_id_str}:{expires_str}"
        expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        if int(expires_str) < int(time.time()):
            return None
        return int(user_id_str)
    except (ValueError, AttributeError):
        return None