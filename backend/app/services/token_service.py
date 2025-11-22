import jwt
from datetime import datetime, timedelta
import secrets
from fastapi import HTTPException
from typing import Dict, Any
from app.repositories.token_repo import (
    add_token, remove_token, remove_user_tokens, get_token, remove_expired_tokens
)

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
REGULAR_TOKEN_EXPIRY_HOURS = 24
REMEMBER_ME_TOKEN_EXPIRY_DAYS = 30
UNAUTHORIZED = 401


def _expiry_delta(remember_me: bool) -> timedelta:
    return (
        timedelta(days=REMEMBER_ME_TOKEN_EXPIRY_DAYS)
        if remember_me
        else timedelta(hours=REGULAR_TOKEN_EXPIRY_HOURS)
    )


def generate_token(
    user_id: str,
    username: str,
    email: str,
    remember_me: bool = False,
    is_admin: bool = False
) -> Dict[str, Any]:
    now = datetime.utcnow()
    expires_delta = _expiry_delta(remember_me)

    expires_at = now + expires_delta
    expires_in_seconds = int(expires_delta.total_seconds())

    payload = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "exp": expires_at,
        "iat": now,
        "remember_me": remember_me,
        "is_admin": is_admin
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    token_data = {
        "token": token,
        "user_id": user_id,
        "expires_at": expires_at.isoformat(),
        "remember_me": remember_me,
        "created_at": now.isoformat()
    }
    add_token(token_data)
    remove_expired_tokens()

    return {
        "token": token,
        "expires_at": expires_at.isoformat(),
        "expires_in": expires_in_seconds
    }


def _expire_and_raise(token: str, msg: str) -> None:
    remove_token(token)
    raise HTTPException(status_code=UNAUTHORIZED, detail=msg)


def verify_token(token: str) -> Dict[str, Any]:
    stored_token = get_token(token)
    if not stored_token:
        raise HTTPException(status_code=UNAUTHORIZED, detail="Token not found or invalid.")

    expires_at = datetime.fromisoformat(stored_token["expires_at"])
    if datetime.utcnow() > expires_at:
        _expire_and_raise(token, "Token has expired.")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        _expire_and_raise(token, "Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=UNAUTHORIZED, detail="Invalid token.")
    except Exception as e:
        raise HTTPException(
            status_code=UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}"
        )


def invalidate_token(token: str) -> None:
    remove_token(token)

def invalidate_user_tokens(user_id: str) -> None:
    remove_user_tokens(user_id)
    