from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import User
from src.services.auth import auth_service
from fastapi import HTTPException, status


def create_user(email: str, username: str, password: str, db: Session) -> Optional[User]:
    """
    Creates a new user record in the database.
    """
    # Determine user role based on existing users
    if not db.query(User).first():
        role = "admin"
    else:
        role = "user"

    hashed_password = auth_service.get_password_hash(password)
    new_user = User(email=email, username=username,
                    password=hashed_password, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_user(user_id: int, username: str, email: str, password: str, db: Session) -> Optional[User]:
    """
    Updates an existing user record in the database.
    """
    user_to_update = await db.query(User).filter(User.id == user_id).first()
    if not user_to_update:
        return None

    user_to_update.username = username
    user_to_update.email = email
    user_to_update.password = auth_service.get_password_hash(password)

    await db.commit()
    await db.refresh(user_to_update)

    return user_to_update


def delete_user(user_id: int, db: Session):
    """
    Deletes an existing user record from the database.
    """
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    """
    Authenticates a user by checking the provided email and password.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not auth_service.verify_password(password, user.password):
        return None
    return user


def confirm_user_email(email: str, db: Session) -> None:
    """
    Confirms the user's email.
    """
    user = db.query(User).filter(User.email == email).first()

    if user:
        user.email_confirmed = True

        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


def get_user_by_email(email: str, db: Session) -> Optional[User]:
    """
    Retrieves a user record from the database based on email address.
    """
    return db.query(User).filter(User.email == email).first()
