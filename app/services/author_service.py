from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.Schemas import author_schema
import app.Models.models as models


def get_author(db: Session, author_id: int):
    return db.query(models.Author).order_by(models.Author.id).filter(models.Author.id == author_id).first()

def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Author).order_by(models.Author.id).offset(skip).limit(limit).all()

def create_author(db: Session, author: author_schema.AuthorCreate):
    db_author = models.Author(
        first_name=author.first_name,
        last_name=author.last_name,
        description=author.description
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def update_author(db: Session, author_id: int, author: author_schema.AuthorUpdate):
    db_author = get_author(db, author_id)
    if not db_author:
        return None
    
    update_data = author.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_author, key, value)

    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if not db_author:
        return None
    db.delete(db_author)
    db.commit()
    return db_author