from sqlalchemy.orm import Session

from fastapi_app.src.database import models
from fastapi_app.src import schemas

from datetime import datetime


async def get_comment(db: Session, comment_id: int):
    """
    Retrieve a comment from the database by its ID.

    :param db: The database session.
    :type db: Session
    :param comment_id: The ID of the comment to retrieve.
    :type comment_id: int
    :return: The comment with the specified ID, or None if not found.
    :rtype: models.Comment
    """
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

async def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int, photo_id: int):
    """
    Create a new comment and add it to the database.

    :param db: The database session.
    :type db: Session
    :param comment: The comment data to create.
    :type comment: schemas.CommentCreate
    :param user_id: The ID of the user creating the comment.
    :type user_id: int
    :param photo_id: The ID of the photo being commented on.
    :type photo_id: int
    :return: The created comment.
    :rtype: models.Comment
    """
    db_comment = models.Comment(**comment.dict(), user_id=user_id, photo_id=photo_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

async def update_comment(db: Session, comment: schemas.CommentUpdate, comment_id: int):
    """
    Update an existing comment in the database.

    :param db: The database session.
    :type db: Session
    :param comment: The updated comment data.
    :type comment: schemas.CommentUpdate
    :param comment_id: The ID of the comment to update.
    :type comment_id: int
    :return: The updated comment, or None if not found.
    :rtype: models.Comment
    """
    db_comment = await get_comment(db, comment_id)
    if db_comment:
        for key, value in comment.dict().items():
            setattr(db_comment, key, value)
        db_comment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_comment)
    return db_comment

async def delete_comment(db: Session, comment_id: int):
    """
    Delete a comment from the database by its ID.

    :param db: The database session.
    :type db: Session
    :param comment_id: The ID of the comment to delete.
    :type comment_id: int
    :return: The deleted comment, or None if not found.
    :rtype: models.Comment
    """
    db_comment = await get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment
