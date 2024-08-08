from sqlalchemy.orm import Session
from typing import List

from fastapi_app.src.database.models import Tag
from fastapi_app.src.database.db import get_db

async def create_tags(names: list[str], db: Session):
    """
    Retrieves a tags by name.

    :param names: The names of tags.
    :type names: list[str]
    :param db: The database session.
    :type db: Session
    :return: List of tags (both existing and newly added) if found, otherwise None.
    :rtype: Tag
    """
    if names == None:
        return None

    final = []
    for name in names:
        existing = db.query(Tag).filter(Tag.name == name).first()
        if existing:
            final.append(existing)
        else:
            new_tag = Tag(name=name)
            db.add(new_tag)
            db.commit()
            final.append(new_tag)

    return final