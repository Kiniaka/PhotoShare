import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from src.schemas import TokenModel
from src.services.auth import auth_service
from src.services.user_service import create_user, get_user_by_email, confirm_user_email
from src.database.db import get_db

router = APIRouter()


@router.post("/login", response_model=TokenModel)
async def login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Endpoint to authenticate a user and generate access and refresh tokens.

    Args:
    - email (str): User's email address.
    - password (str): User's password.
    - db (Session, optional): SQLAlchemy database session (dependency).

    Returns:
    - dict: Dictionary containing access_token, refresh_token, and token_type.

    Raises:
    - HTTPException: If authentication fails (status_code 401).
    """
    user = await auth_service.authenticate_user(email, password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)))
    refresh_token_expires = timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30)))

    access_token = await auth_service.create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires.total_seconds()
    )
    refresh_token_param = await auth_service.create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires.total_seconds()
    )

    return {"access_token": access_token, "refresh_token": refresh_token_param, "token_type": "bearer"}


@router.post("/refresh", response_model=TokenModel)
async def refresh_token(refresh_token_param: str = Depends(auth_service.oauth2_scheme), db: Session = Depends(get_db)):
    """
    Endpoint to refresh an access token using a refresh token.

    Args:
    - refresh_token_param (str, optional): Refresh token from request header (dependency).
    - db (Session, optional): SQLAlchemy database session (dependency).

    Returns:
    - dict: Dictionary containing new access_token, refresh_token, and token_type.

    Raises:
    - HTTPException: If token decoding fails (status_code 401) or user not found (status_code 404).
    """
    try:
        email = await auth_service.decode_refresh_token(refresh_token_param)
        user = await get_user_by_email(email, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)))
        access_token = await auth_service.create_access_token(
            data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires.total_seconds()
        )

        return {"access_token": access_token, "refresh_token": refresh_token_param, "token_type": "bearer"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from e


@router.post("/register", response_model=TokenModel)
async def register(email: str, username: str, password: str, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user and generate access and refresh tokens.

    Args:
    - email (str): User's email address.
    - username (str): User's username.
    - password (str): User's password.
    - db (Session, optional): SQLAlchemy database session (dependency).

    Returns:
    - dict: Dictionary containing access_token, refresh_token, and token_type.

    Raises:
    - HTTPException: If user already registered (status_code 400).
    """
    user = await create_user(email, username, password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)))
    refresh_token_expires = timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30)))

    access_token = await auth_service.create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires.total_seconds()
    )
    refresh_token_param = await auth_service.create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires.total_seconds()
    )

    return {"access_token": access_token, "refresh_token": refresh_token_param, "token_type": "bearer"}


@router.post("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Endpoint to verify user's email using a verification token.

    Args:
    - token (str): Email verification token.
    - db (Session, optional): SQLAlchemy database session (dependency).

    Returns:
    - dict: Dictionary with detail message on successful email verification.

    Raises:
    - HTTPException: If user not found (status_code 404) or invalid token (status_code 422).
    """
    email = await auth_service.get_email_from_token(token)
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await confirm_user_email(email, db)
    return {"detail": "Email verified"}
