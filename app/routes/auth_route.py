from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schema.auth_schema import LoginRequest, LoginResponse
from app.utils.dependencies import get_current_user
from app.utils.security import (
    create_access_token,
    verify_password
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    if not verify_password(
        data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    token = create_access_token(user)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }


@router.get("/me")
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "company_id": current_user.company_id,
        "department_id": current_user.department_id
    }


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.token_version += 1

    db.commit()

    return {
        "message": "Logged out successfully"
    }