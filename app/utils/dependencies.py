from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.utils.security import decode_access_token


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    authentication_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token"
    )

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")
        token_version = payload.get("token_version")

        if user_id is None:
            raise authentication_error

        user_id = int(user_id)

    except (InvalidTokenError, TypeError, ValueError):
        raise authentication_error

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise authentication_error

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    if user.token_version != token_version:
        raise authentication_error

    return user


def require_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user


def require_agent(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "agent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agent access required"
        )

    return current_user