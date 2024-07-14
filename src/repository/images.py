from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import extract, and_

from src.database.models import Image, User, Tag
from src.schemas import ImageModel
from tags import create_tags


async def get_images(skip: int, limit: int, db: Session) -> List[Image] | None:
    """returns every image saved in the database

    :param skip: how many images will be skipped
    :type skip: int
    :param limit: max number of images displayed on one page
    :type limit: int
    :param user: current user
    :type user: User
    :param db: database session
    :type db: Session
    :return: images saved in db
    :rtype: List[Image]
    """
    return db.query(Image).filter().offset(skip).limit(limit).all()


async def get_image(image_id: int, db: Session) -> Image | None:
    """Searches for an image by it's index

    :param image_id: searched index
    :type image_id: int
    :param db: database session
    :type db: Session
    :return: image with given index
    :rtype: Image
    """
    return db.query(Image).filter(Image.id == image_id).first()


async def create_image(body: ImageModel, user: User, db: Session) -> Image:
    """Creates and saves image in database

    :param body: Image instance with all the needed parameters
    :type body: ImageModel
    :param user: current user
    :type user: User
    :param db: database session
    :type db: Session
    :return: Image that is being saved
    :rtype: Image
    """
    tags = await create_tags([tag for tag in body.tags.split(' ')])
    image = Image(**body.dict(), tags=tags, user_id=user.id)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


async def update_image(image_id: int, body: ImageModel, user: User, db: Session) -> Image | None:
    """Updates an existing image in database

    :param image_id: index of already existing image
    :type image_id: int
    :param body: new instance of image to save
    :type body: ImageModel
    :param user: current user
    :type user: User
    :param db: database session
    :type db: Session
    :return: newly saved image
    :rtype: Image | None
    """
    image = db.query(Image).filter(
        and_(Image.id == image_id, Image.user_id == user.id)).first()
    if image:
        image.image_name = body.image_name
        image.image_link = body.image_link
        tags = await create_tags([tag for tag in body.tags.split(', ')])
        image.tags = tags
        db.commit()
    return image


async def remove_image(image_id: int, user: User, db: Session) -> Image | None:
    """Removes an image from database

    :param image_id: index of image to remove
    :type image_id: int
    :param user: current user
    :type user: User
    :param db: database session
    :type db: Session
    :return: image that is being removed
    :rtype: Image | None
    """
    image = db.query(Image).filter(
        and_(Image.user_id == user.id, Image.id == image_id)).first()
    if image:
        db.delete(image)
        db.commit()
    return image
