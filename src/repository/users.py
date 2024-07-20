from src.services.auth import auth_service as auth
from typing import Optional, List
from sqlalchemy.orm import Session
from src.database.models import User
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

path = 'src/database/.env'

load_dotenv(path)


async def create_user(email: str, username: str, password: str, db: Session) -> User:
    """
    Creates a new user record in the database.
    :param email: User's email address.
    :param username: User's username.
    :param password: Hashed password of the user.
    :param db: Database session dependency.
    :return: Created user object.
    """
    if not db.query(User).first():
        role = "admin"
    else:
        role = "user"

    new_user = User(email=email, username=username,
                    password=password, role=role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(email: str, db: Session) -> Optional[User]:
    """
    Retrieves a user record from the database based on email address.
    :param email: Email address of the user.
    :param db: Database session dependency.
    :return: User object if found, None if not found.
    """
    return db.query(User).filter(User.email == email).first()


async def update_user(user_id: int, username: str, email: str, password: str, db: Session) -> Optional[User]:
    """
    Updates an existing user record in the database.
    :param user_id: ID of the user to be updated.
    :param username: Updated username.
    :param email: Updated email address.
    :param password: Updated hashed password.
    :param db: Database session dependency.
    :return: Updated user object if found, None if not found.
    """
    user_to_update = await db.query(User).filter(User.id == user_id).first()
    if not user_to_update:
        return None

    user_to_update.username = username
    user_to_update.email = email
    user_to_update.password = password

    await db.commit()
    await db.refresh(user_to_update)

    return user_to_update


async def delete_user(user_id: int, db: Session):
    """
    Deletes an existing user record from the database.
    :param user_id: ID of the user to be deleted.
    :param db: Database session dependency.
    """
    user_to_delete = await db.query(User).filter(User.id == user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        await db.commit()


async def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    """
    Authenticates a user by checking the provided email and password.
    :param email: Email of the user.
    :param password: Password of the user.
    :param db: Database session dependency.
    :return: User object if authentication succeeds, None otherwise.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not auth.verify_password(password, user.password):
        return None
    return user

async def confirm_user_email(email: str, db: Session) -> None:
    """
    Confirms the user's email (assuming some logic for email confirmation).
    :param email: Email of the user to confirm.
    :param db: Database session dependency.
    :return: None
    """
    user = await db.query(User).filter(User.email == email).first()

    if user:
        user.email_confirmed = True

        await db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


async def promote_to_moderator(user_id: int, db: Session) -> Optional[User]:
    """
    Promotes an existing user to the role of moderator.
    :param user_id: ID of the user to promote.
    :param db: Database session dependency.
    :return: Updated user object if found, None if not found.
    """
    user_to_promote = await db.query(User).filter(User.id == user_id).first()
    if not user_to_promote:
        return None

    user_to_promote.role = "moderator"

    await db.commit()
    await db.refresh(user_to_promote)

    return user_to_promote


async def demote_to_user(user_id: int, db: Session) -> Optional[User]:
    """
    Demotes an existing moderator to the role of user.
    :param user_id: ID of the user to demote.
    :param db: Database session dependency.
    :return: Updated user object if found, None if not found.
    """
    user_to_demote = await db.query(User).filter(User.id == user_id).first()
    if not user_to_demote:
        return None

    user_to_demote.role = "user"

    await db.commit()
    await db.refresh(user_to_demote)

    return user_to_demote


async def promote_to_admin(user_id: int, db: Session) -> Optional[User]:
    """
    Promotes an existing user to the role of admin.
    :param user_id: ID of the user to promote.
    :param db: Database session dependency.
    :return: Updated user object if found, None if not found.
    """
    user_to_promote = await db.query(User).filter(User.id == user_id).first()
    if not user_to_promote:
        return None

    user_to_promote.role = "admin"

    await db.commit()
    await db.refresh(user_to_promote)

    return user_to_promote

# ______________________PIERWOTNA FUNCKJA KTÓRA CYKLUJE IMPORTY_______________________________________________________________


def get_current_active_user(current_user: User = Depends(auth.get_current_user)):
    """
    Retrieves the current active user.
    :param current_user: Current authenticated user.
    :return: Current active user object.
    """
    if current_user.role not in ["admin", "moderator", "user"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Insufficient permissions")
    return current_user

def get_all_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    """
    Retrieves all user records from the database.
    :param db: Database session dependency.
    :param skip: Number of records to skip for pagination.
    :param limit: Maximum number of records to retrieve.
    :return: List of user objects.
    """
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Retrieves a user record from the database based on user ID.
    :param db: Database session dependency.
    :param user_id: ID of the user to retrieve.
    :return: User object if found, None if not found.
    """
    return db.query(User).filter(User.id == user_id).first()
