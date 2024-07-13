from sqlalchemy.orm import Session
from typing import List


from src.database.db import get_db
from src.database.models import Tag

async def create_tags(tags: list, db: Session) -> List[Tag]:
    final = []
    for tag in tags:
        existing = db.query(Tag).filter(Tag.tag_name == tag).first()
        if existing:
            final.append(existing)
        else:
            new_tag = Tag(tag_name=tag)
            db.add(new_tag)
            db.commit()
            db.refresh(new_tag)
            final.append(new_tag)
    return final
