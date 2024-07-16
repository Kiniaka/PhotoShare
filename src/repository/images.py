from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Image, User
from src.schemas import ImageModel
from src.repository.tags import create_tags


async def get_images(skip: int, limit: int, db: Session) -> Optional[List[Image]]:
    """Returns a list of images from the database.

    :param skip: Number of images to skip
    :type skip: int
    :param limit: Maximum number of images to return
    :type limit: int
    :param db: Database session
    :type db: Session
    :return: List of images or None if no images are found
    :rtype: Optional[List[Image]]
    """
    images = db.query(Image).offset(skip).limit(limit).all()
    return images if images else None


async def get_image(image_id: int, db: Session) -> Optional[Image]:
    """Retrieves an image by its ID.

    :param image_id: ID of the image to retrieve
    :type image_id: int
    :param db: Database session
    :type db: Session
    :return: Image object or None if not found
    :rtype: Optional[Image]
    """
    return db.query(Image).filter(Image.id == image_id).first()


async def create_image(body: ImageModel, user: User, db: Session) -> Image:
    """Creates a new image in the database.

    :param body: Data for the new image
    :type body: ImageModel
    :param user: User who is creating the image
    :type user: User
    :param db: Database session
    :type db: Session
    :return: Created image
    :rtype: Image
    """
    tags = await create_tags(body.tags) if body.tags else []
    image = Image(**body.dict(), tags=tags, user_id=user.id)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


async def update_image(image_id: int, body: ImageModel, user: User, db: Session) -> Optional[Image]:
    """Updates an existing image in the database.

    :param image_id: ID of the image to update
    :type image_id: int
    :param body: Updated data for the image
    :type body: ImageModel
    :param user: User who is updating the image
    :type user: User
    :param db: Database session
    :type db: Session
    :return: Updated image or None if not found
    :rtype: Optional[Image]
    """
    image = db.query(Image).filter(
        and_(Image.id == image_id, Image.user_id == user.id)).first()
    if image:
        image.image_name = body.image_name
        image.image_link = body.image_link
        tags = await create_tags(body.tags) if body.tags else []
        image.tags = tags
        db.commit()
        db.refresh(image)
    return image


async def remove_image(image_id: int, user: User, db: Session) -> Optional[Image]:
    """Deletes an image from the database.

    :param image_id: ID of the image to delete
    :type image_id: int
    :param user: User who is deleting the image
    :type user: User
    :param db: Database session
    :type db: Session
    :return: Deleted image or None if not found
    :rtype: Optional[Image]
    """
    image = db.query(Image).filter(
        and_(Image.user_id == user.id, Image.id == image_id)).first()
    if image:
        db.delete(image)
        db.commit()
    return image
