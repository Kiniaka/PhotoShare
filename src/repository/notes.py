from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from src.database.models import Note
from src.schemas import NoteCreate, NoteUpdate


def get_notes(db: Session) -> List[Note]:
    """Fetch all notes from the database.

    Args:
        db (Session): Database session instance.

    Returns:
        List[Note]: List of all notes in the database.
    """
    return db.query(Note).all()


def get_note_by_id(note_id: int, db: Session) -> Optional[Note]:
    """Fetch a note by its ID from the database.

    Args:
        note_id (int): ID of the note to fetch.
        db (Session): Database session instance.

    Returns:
        Optional[Note]: Note object if found, otherwise None.
    """
    return db.query(Note).filter(Note.id == note_id).first()


def create_note(note: NoteCreate, db: Session) -> Note:
    """Create a new note and store it in the database.

    Args:
        note (NoteCreate): Data for creating the new note.
        db (Session): Database session instance.

    Returns:
        Note: Created note object.
    """
    db_note = Note(
        note_description=note.note_description,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_note(note_id: int, note_update: NoteUpdate, db: Session) -> Optional[Note]:
    """Update an existing note in the database.

    Args:
        note_id (int): ID of the note to update.
        note_update (NoteUpdate): Data for updating the note.
        db (Session): Database session instance.

    Returns:
        Optional[Note]: Updated note object if found, otherwise None.
    """
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db_note.note_description = note_update.note_description
        db_note.updated_at = datetime.now()
        db.commit()
        db.refresh(db_note)
        return db_note
    return None


def delete_note(note_id: int, db: Session) -> Optional[Note]:
    """Delete a note from the database.

    Args:
        note_id (int): ID of the note to delete.
        db (Session): Database session instance.

    Returns:
        Optional[Note]: Deleted note object if found, otherwise None.
    """
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return db_note
    return None
