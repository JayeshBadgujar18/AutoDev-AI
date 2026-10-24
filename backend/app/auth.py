from datetime import datetime, timedelta, timezone
from jose import jwt
from .config import get_settings


def create_access_token(subject: str, role: str = "developer") -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": subject, "role": role, "iat": now, "exp": now + timedelta(hours=8)}
    return jwt.encode(payload, get_settings().jwt_secret, algorithm=get_settings().jwt_algorithm)
