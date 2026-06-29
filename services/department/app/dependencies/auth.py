import os

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from jwt.exceptions import InvalidTokenError


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing")


security = HTTPBearer()


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        admin_id = payload.get("sub")
        company_id = payload.get("company_id")
        role = payload.get("role")

        if not admin_id:
            raise HTTPException(
                status_code=401,
                detail="Admin ID missing in token"
            )

        if not company_id:
            raise HTTPException(
                status_code=401,
                detail="Company ID missing in token"
            )

        if role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Only admin can manage departments"
            )

        return {
            "admin_id": admin_id,
            "company_id": company_id,
            "role": role
        }

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )