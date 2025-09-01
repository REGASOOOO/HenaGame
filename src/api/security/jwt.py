import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import jwt, JWTError

# Basic settings (override via environment variables in production)
SECRET_KEY = os.getenv("JWT_SECRET", "CHANGE_ME_IN_PROD")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


class TokenError(Exception):
    pass


def get_username_from_token(token: str) -> str:
    try:
        payload = decode_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise TokenError("Token missing subject")
        return username
    except JWTError as e:
        raise TokenError(str(e)) from e
