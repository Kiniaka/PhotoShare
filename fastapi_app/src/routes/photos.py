from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from uuid import uuid4
from fastapi_app.src.database.models import Photo, User
from fastapi_app.src.services.photo_service import PhotoService
from fastapi_app.src.services.auth import auth_service
from fastapi_app.src.database.db import get_db
from fastapi_app.src.repository.tags import create_tags
import aiofiles
import os
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(prefix="/photos", tags=["photos"])


UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_photo(file: UploadFile) -> str:
    """
    Save an uploaded photo to the file system.

    :param file: The photo file to upload.
    :type file: UploadFile
    :return: The file path where the photo is saved.
    :rtype: str
    :raises IOError: If there is an error saving the file.
    """
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    async with aiofiles.open(file_path, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    
    return file_path

@router.post("/photos/", status_code=201)
async def create_photo(description: str, tags: Optional[str] = None, file: UploadFile = File(...), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Create a new photo.

    :param description: Description of the photo.
    :type description: str
    :param tags: Space-separated tags for the photo.
    :type tags: Optional[str]
    :param file: The photo file to upload.
    :type file: UploadFile
    :param current_user: The current authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: Session
    :return: The saved photo object.
    :rtype: Photo
    :raises HTTPException: If there is an error saving the photo, raises an appropriate HTTP error.
    """
    file_path = await save_photo(file)
    tag_list = [tag for tag in tags.split(' ')]
    tags = await create_tags(tag_list, db)
    photo = Photo(description=description, url=file_path, tags=tags, user_id=current_user.id)
    saved_photo = PhotoService.save(db, photo)
    return saved_photo

@router.put("/photos/{photo_id}")
async def update_photo(photo_id: int, description: str, db: Session = Depends(get_db)):
    """
    Update the description of a photo by its ID.

    :param photo_id: The ID of the photo to update.
    :type photo_id: int
    :param description: The new description for the photo.
    :type description: str
    :param db: The database session.
    :type db: Session
    :return: The updated photo data.
    :rtype: dict
    :raises HTTPException: If the photo is not found, raises a 404 error with the detail message.
    """
    try:
        updated_photo = PhotoService.update(db, photo_id, description)
        return updated_photo
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/photos/{photo_id}")
async def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    """
    Delete a photo by its ID.

    :param photo_id: The ID of the photo to delete.
    :type photo_id: int
    :param db: The database session.
    :type db: Session
    :return: A confirmation message indicating the photo was deleted.
    :rtype: dict
    :raises HTTPException: If the photo is not found, raises a 404 error with the detail message.
    """
    try:
        PhotoService.delete(db,photo_id)
        return {"detail": "Photo deleted"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/photos/{photo_id}")
async def read_photo(photo_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a photo by its ID.

    :param photo_id: The ID of the photo to retrieve.
    :type photo_id: int
    :param db: The database session.
    :type db: Session
    :return: The photo data.
    :rtype: dict
    :raises HTTPException: If the photo is not found, raises a 404 error with the detail message.
    """
    try:
        photo = PhotoService.get(db, photo_id)
        return photo
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))