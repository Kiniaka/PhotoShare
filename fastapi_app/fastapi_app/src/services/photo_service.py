from sqlalchemy.orm import Session
from uuid import UUID
from fastapi_app.src.database.models import Photo
from fastapi_app.src.database.db import SessionLocal

    
class PhotoService:
    @staticmethod
    def save(db: Session, photo: Photo) -> Photo:
        """
        Save a new photo to the database.

        :param db: The database session.
        :type db: Session
        :param photo: The photo object to save.
        :type photo: Photo
        :return: The saved photo object.
        :rtype: Photo
        """
        db.add(photo)
        db.commit()
        db.refresh(photo)
        return photo

    @staticmethod
    def update(db: Session, photo_id: int, description: str) -> Photo:
        """
        Update the description of a photo by its ID.

        :param db: The database session.
        :type db: Session
        :param photo_id: The ID of the photo to update.
        :type photo_id: int
        :param description: The new description for the photo.
        :type description: str
        :return: The updated photo object.
        :rtype: Photo
        :raises FileNotFoundError: If the photo is not found.
        """
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if photo:
            photo.description = description
            db.commit()
            db.refresh(photo)
        else:
            raise FileNotFoundError(f"Photo with ID {photo_id} not found")
        return photo

    @staticmethod
    def delete(db: Session, photo_id: int) -> None:
        """
        Delete a photo by its ID.

        :param db: The database session.
        :type db: Session
        :param photo_id: The ID of the photo to delete.
        :type photo_id: int
        :return: None
        :rtype: None
        :raises FileNotFoundError: If the photo is not found.
        """
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if photo:
            db.delete(photo)
            db.commit()
        else:
            raise FileNotFoundError(f"Photo with ID {photo_id} not found")

    @staticmethod
    def get(db: Session, photo_id: int) -> Photo:
        """
        Retrieve a photo by its ID.

        :param db: The database session.
        :type db: Session
        :param photo_id: The ID of the photo to retrieve.
        :type photo_id: int
        :return: The retrieved photo object.
        :rtype: Photo
        :raises FileNotFoundError: If the photo is not found.
        """
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if not photo:
            raise FileNotFoundError(f"Photo with ID {photo_id} not found")
        return photo