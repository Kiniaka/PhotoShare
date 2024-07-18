from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ImageModel, ImageInDB
from src.repository import images as repository_images
from src.routes.auth import auth_service
from src.database.models import User

router = APIRouter(prefix='/images', tags=['images'])


@router.get('/', response_model=List[ImageInDB], summary='Retrieve images with rate limiting',
            description='No more than 10 requests per minute',
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
    images = await repository_images.get_images(skip, limit, db)
    filtered_images = [
        image for image in images if image.user_id == current_user.id]

    if not filtered_images:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No images found')

    return filtered_images


@router.get('/{image_id}', response_model=ImageInDB, summary='Retrieve a single image with rate limiting',
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_image(image_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve an image by ID with rate limiting (10 requests per minute).

    :param image_id: The ID of the image to retrieve.
    :type image_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :raises HTTPException 404: If image not found or if the image does not belong to the current user.
    :return: Retrieved image.
    :rtype: ImageInDB
    """
    image = await repository_images.get_image(image_id, db)
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')

    # Check if the retrieved image belongs to the current user
    if image.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You do not have permission to access this image')

    return image


@router.post('/', response_model=ImageInDB, summary='Create a new image with rate limiting',
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_image(body: ImageModel, db: Session = Depends(get_db),
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


@router.put('/{image_id}', response_model=ImageInDB, summary='Update an image with rate limiting',
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_image(image_id: int, body: ImageModel, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Update an image by ID with rate limiting (10 requests per minute).

    :param image_id: The ID of the image to update.
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
    image = await repository_images.update_image(image_id, body, current_user, db)
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')
    return image


@router.delete('/{image_id}', response_model=ImageInDB, summary='Delete an image with rate limiting',
               description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def delete_image(image_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Delete an image by ID with rate limiting (10 requests per minute).

    :param image_id: The ID of the image to delete.
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')
    return image
