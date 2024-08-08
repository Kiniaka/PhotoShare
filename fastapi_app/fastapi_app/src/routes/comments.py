from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from fastapi_app.src.database import models
from fastapi_app.src import schemas
from fastapi_app.src.repository import comments as crud
from fastapi_app.src.database.db import get_db
from fastapi_app.src.services.auth import auth_service

router = APIRouter(prefix="/comments", tags=["comments"])
# router = APIRouter()

@router.post("/photos/{photo_id}/comments/", response_model=schemas.Comment, status_code=201)
async def create_comment_for_photo(
    photo_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    """
    Create a new comment for a specific photo.

    :param photo_id: The ID of the photo to comment on.
    :type photo_id: int
    :param comment: The comment data to create.
    :type comment: schemas.CommentCreate
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: models.User
    :return: The created comment.
    :rtype: schemas.Comment
    """
    return await crud.create_comment(db=db, comment=comment, user_id=current_user.id, photo_id=photo_id)

@router.get("/comments/{comment_id}", response_model=schemas.Comment)
async def read_comment(comment_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific comment by its ID.

    :param comment_id: The ID of the comment to retrieve.
    :type comment_id: int
    :param db: The database session.
    :type db: Session
    :return: The retrieved comment.
    :rtype: schemas.Comment
    :raises HTTPException: If the comment is not found.
    """
    db_comment = await crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.put("/comments/{comment_id}", response_model=schemas.Comment)
async def update_comment(
    comment_id: int,
    comment: schemas.CommentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    """
    Update an existing comment.

    :param comment_id: The ID of the comment to update.
    :type comment_id: int
    :param comment: The updated comment data.
    :type comment: schemas.CommentUpdate
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: models.User
    :return: The updated comment.
    :rtype: schemas.Comment
    :raises HTTPException: If the comment is not found or the user is not authorized to update it.
    """
    db_comment = await crud.get_comment(db, comment_id=comment_id)
    if db_comment is None or db_comment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized to update")
    return await crud.update_comment(db=db, comment=comment, comment_id=comment_id)

@router.delete("/comments/{comment_id}", response_model=schemas.Comment)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    """
    Delete a specific comment by its ID.

    :param comment_id: The ID of the comment to delete.
    :type comment_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: models.User
    :return: The deleted comment.
    :rtype: schemas.Comment
    :raises HTTPException: If the comment is not found or the user is not authorized to delete it.
    """
    db_comment = await crud.get_comment(db, comment_id=comment_id)
    if db_comment is None or current_user.role not in ["admin", "moderator"]:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized to delete")
    return await crud.delete_comment(db=db, comment_id=comment_id)