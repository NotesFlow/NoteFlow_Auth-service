from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest):
    db: Session = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter((User.username == payload.username) | (User.email == payload.email))
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists",
            )

        user = User(
            username=payload.username,
            email=payload.email,
            password_hash=get_password_hash(payload.password),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return RegisterResponse(
            id=user.id,
            username=user.username,
            email=user.email,
        )
    finally:
        db.close()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(User.username == payload.username).first()

        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        access_token = create_access_token(subject=user.username)

        return TokenResponse(access_token=access_token)
    finally:
        db.close()