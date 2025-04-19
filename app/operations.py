from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from .Schemas import book_schema
from .Schemas import author_schema
import app.Models.models as models

def get_book(db: Session, book_id: int):
    return db.query(models.Book)\
        .filter(models.Book.id == book_id)\
        .options(joinedload(models.Book.authors))\
        .first()

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book)\
        .order_by(models.Book.id)\
        .options(joinedload(models.Book.authors))\
        .offset(skip)\
        .limit(limit).all()
    
def get_book_by_name(db: Session, name: str):
    return db.query(models.Book).filter(models.Book.title == name).first()

def create_book(db: Session, book: book_schema.BookCreate):
    # Create new book instance with basic fields
    db_book = models.Book(
        title=book.title,
        isbn=book.isbn,
        publication_date=book.publication_date,
        genre=book.genre
    )
    
    # Handle authors if provided
    if hasattr(book, 'author_ids') and book.author_ids:
        authors = db.query(models.Author).filter(
            models.Author.id.in_(book.author_ids)
        ).all()
        
        # Verify if all authors were found
        if len(authors) != len(book.author_ids):
            raise ValueError("One or more author IDs are invalid")
            
        db_book.authors = authors

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: book_schema.BookUpdate):
    db_book = get_book(db, book_id)
    if not db_book:
        return None

    update_data = book.dict(exclude_unset=True)
    
    # Handle authors separately
    author_ids = update_data.pop('author_ids', None)
    if author_ids is not None:
        authors = db.query(models.Author).filter(
            models.Author.id.in_(author_ids)
        ).all()
        db_book.authors = authors

    # Update other fields
    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book

# Author operations
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
