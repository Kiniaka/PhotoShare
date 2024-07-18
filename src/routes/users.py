from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserModel, UserDB
# from src.schemas import UserModel, UserUpdate, UserDB
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.database.models import User

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=List[UserDB], summary='Get all users')
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve all users from the database.

    Args:
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to retrieve.
        db (Session): Database session.
        current_user (User): The current authenticated user.

    Raises:
        HTTPException: If the current user does not have admin permissions.

    Returns:
        List[UserDB]: List of users.
    """
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You do not have permission to access this resource')

    users = repository_users.get_all_users(db, skip=skip, limit=limit)
    return users


@router.get('/{user_id}', response_model=UserDB, summary='Get user by ID')
async def get_user_by_id(user_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): Database session.
        current_user (User): The current authenticated user.

    Raises:
        HTTPException: If the current user does not have admin permissions and is not the requested user.
        HTTPException: If the user with the specified ID is not found.

    Returns:
        UserDB: The retrieved user.
    """
    if current_user.role != 'admin' and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You do not have permission to access this resource')

    user = repository_users.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {user_id} not found')

    return user


@router.post('/', response_model=UserDB, summary='Create a new user')
async def create_user(user_data: UserModel, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    Args:
        user_data (UserModel): The data for the user to create.
        db (Session): Database session.

    Raises:
        HTTPException: If a user with the specified email already exists.

    Returns:
        UserDB: The created user.
    """
    existing_user = repository_users.get_user_by_email(user_data.email, db)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User with email {user_data.email} already exists')

    hashed_password = auth_service.hash_password(user_data.password)
    user = await repository_users.create_user(user_data.email, user_data.username, hashed_password, db)
    return user


# @router.put('/{user_id}', response_model=UserDB, summary='Update user by ID')
# async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db),
#                       current_user: User = Depends(auth_service.get_current_user)):
#     """
#     Update a user by ID.

#     Args:
#         user_id (int): The ID of the user to update.
#         user_data (UserUpdate): The updated user data.
#         db (Session): Database session.
#         current_user (User): The current authenticated user.

#     Raises:
#         HTTPException: If the current user does not have admin permissions and is not the requested user.
#         HTTPException: If the user with the specified ID is not found.

#     Returns:
#         UserInDB: The updated user.
#     """
#     if current_user.role != 'admin' and current_user.id != user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail='You do not have permission to access this resource')

#     hashed_password = auth_service.hash_password(
#         user_data.password) if user_data.password else None
#     user = await repository_users.update_user(user_id, user_data.username, user_data.email, hashed_password, db)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'User with id {user_id} not found')

#     return user


@router.delete('/{user_id}', response_model=UserDB, summary='Delete user by ID')
async def delete_user(user_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    Delete a user by ID.

    Args:
        user_id (int): The ID of the user to delete.
        db (Session): Database session.
        current_user (User): The current authenticated user.

    Raises:
        HTTPException: If the current user does not have admin permissions and is not the requested user.
        HTTPException: If the user with the specified ID is not found.

    Returns:
        UserDB: The deleted user.
    """
    if current_user.role != 'admin' and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You do not have permission to access this resource')

    user = await repository_users.delete_user(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {user_id} not found')

    return user
