import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

if not SECRET_KEY:
    raise ValueError("SECRET_KEY .env file me nahi mila")


password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(
        plain_password,
        hashed_password
    )


def create_access_token(user):
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user.id),
        "role": user.role,
        "company_id": user.company_id,
        "department_id": user.department_id,
        "token_version": user.token_version,
        "exp": expires_at
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )