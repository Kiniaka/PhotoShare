from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ImageModel, ImageInDB
from src.repository import images as repository_images
from src.routes.auth import auth_service
from src.database.models import User

router = APIRouter(prefix='/contacts', tags=['contacts'])

@router.get('/', response_model=List[ImageInDB], description='No more than 10 requests pre minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_images(skip: int = 0, limit: int = 5, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve images with rate limiting (10 requests per minute).

    :param skip: Number of records to skip.
    :type skip: int
    :param limit: Maximum number of records to retrieve.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :raises HTTPException 404: If images not found.
    :return: List of images.
    :rtype: List[ImageInDB]
    """
    images = await repository_images.get_images(skip, limit, current_user, db)
    return images

@router.get('/{image_id}', response_model=ImageInDB, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_image(image_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a image by ID with rate limiting (10 requests per minute).

    :param image_id: The ID of the contact to retrieve.
    :type image_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :raises HTTPException 404: If image not found.
    :return: Retrieved image.
    :rtype: ImageInDB
    """
    image = await repository_images.get_contact(image_id, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return image


@router.post('/', response_model=ImageInDB, description='No more than 10 requests pre minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ImageModel, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Create a new image with rate limiting (10 requests per minute).

    :param body: The image details to create.
    :type body: ImageModel
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: Created image.
    :rtype: ImageInDB
    """
    return await repository_images.create_image(body, current_user, db)

@router.put('/{image_id}', response_model=ImageInDB, description='No more than 10 requests pre minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_image(body: ImageModel, image_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Update a contact by ID with rate limiting (10 requests per minute).

    :param image_id: The ID of the contact to update.
    :type image_id: int
    :param body: The updated image details.
    :type body: ImageModel
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :raises HTTPException 404: If image not found.
    :return: Updated image.
    :rtype: ImageInDB
    """
    contact = await repository_images.update_contact(image_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return contact


@router.delete('{image_id}', response_model=ImageInDB, description='No more than 10 requests pre minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_image(image_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Delete a contact by ID with rate limiting (10 requests per minute).

    :param image_id: The ID of the contact to delete.
    :type image_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :raises HTTPException 404: If image not found.
    :return: Deleted image.
    :rtype: ImageInDB
    """
    image = await repository_images.remove_image(image_id, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image