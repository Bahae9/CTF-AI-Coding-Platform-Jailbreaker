"""
validators.py — Input validation helpers for the Learnify platform.
"""
import re
from typing import Any


EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
SLUG_RE  = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def is_valid_email(value: str) -> bool:
    """Return True if value is a plausible email address."""
    return bool(EMAIL_RE.match(value.strip())) if isinstance(value, str) else False


def is_valid_slug(value: str) -> bool:
    """Return True if value is a URL-safe lowercase slug."""
    return bool(SLUG_RE.match(value)) if isinstance(value, str) else False


def clamp(value: int | float, lo: int | float, hi: int | float) -> int | float:
    """Clamp a numeric value to [lo, hi]."""
    return max(lo, min(hi, value))


def sanitize_string(value: Any, max_length: int = 255) -> str:
    """
    Strip leading/trailing whitespace, collapse internal whitespace,
    and truncate to max_length. Returns empty string for non-string input.
    """
    if not isinstance(value, str):
        return ""
    cleaned = " ".join(value.split())
    return cleaned[:max_length]


def validate_price(value: Any) -> float:
    """
    Coerce value to a non-negative float price rounded to 2 decimal places.
    Raises ValueError for values that cannot be converted.
    """
    try:
        price = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid price: {value!r}")
    if price < 0:
        raise ValueError("Price cannot be negative.")
    return round(price, 2)


def validate_rating(value: Any) -> float:
    """Return a valid rating in [0.0, 5.0], raises ValueError otherwise."""
    try:
        rating = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid rating: {value!r}")
    if not (0.0 <= rating <= 5.0):
        raise ValueError("Rating must be between 0.0 and 5.0.")
    return round(rating, 1)