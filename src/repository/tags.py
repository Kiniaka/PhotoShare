from sqlalchemy.orm import Session
from typing import List
from src.schemas import TagModel


async def create_tags(tags: List[str], db: Session) -> List[TagModel]:
    final_tags = []
    for tag_name in tags:
        existing_tag = db.query(TagModel).filter_by(tag_name=tag_name).first()
        if existing_tag is not None:
            final_tags.append(existing_tag)
        else:
            new_tag = TagModel(tag_name=tag_name)
            db.add(new_tag)
            await db.commit()
            await db.refresh(new_tag)
            final_tags.append(new_tag)
    return final_tags
