from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from core.config.settings import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token with an expiration time.
    """
    to_encode = data.copy()
    expire = datetime.now(tz=UTC) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decode a JWT access token. Return payload dict or None if invalid.
    """
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None
