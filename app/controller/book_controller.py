import app
from app.Schemas import book_schema
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.services import book_service

from app.database.database_connection import get_db

router = APIRouter()

@router.post("/books", response_model=book_schema.Book, status_code=status.HTTP_201_CREATED, tags=["Books"])
def create_book(book: book_schema.BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(db=db, book=book)

@router.get("/books/", response_model=List[book_schema.Book], tags=["Books"])
def get_all_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return book_service.get_books(db=db, skip=skip, limit=limit)

@router.get("/book/{book_id}", response_model=book_schema.Book, tags=["Books"])
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    db_book = book_service.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with the Id not found")
    return db_book

@router.get("/book/name/{name}", response_model=book_schema.Book, tags=["Books"])
def get_book_by_name(title: str, db: Session = Depends(get_db)):
    db_book = book_service.get_book_by_name(db=db, name=title)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with the name not found")
    return db_book

@router.put("/book/{book_id}", response_model=book_schema.Book, tags=["Books"])
def update_book(book_id: int, book: book_schema.BookUpdate, db: Session = Depends(get_db)):
    db_book = book_service.update_book(db=db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with the Id not found")
    return db_book

@router.delete("/book/{book_id}", response_model=book_schema.Book, tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = book_service.delete_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with the Id not found")
    return db_book