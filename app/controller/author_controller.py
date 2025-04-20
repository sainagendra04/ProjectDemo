from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app
from app.Schemas import author_schema
from app.database.database_connection import get_db
from app.services import author_service


router = APIRouter()

@router.post("/authors/", response_model=author_schema.Author, status_code=status.HTTP_201_CREATED, tags=["Authors"])
def create_author(author: author_schema.AuthorCreate, db: Session = Depends(get_db)):
    return author_service.create_author(db=db, author=author)

@router.get("/authors/", response_model=List[author_schema.Author], tags=["Authors"])
def get_all_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return author_service.get_authors(db=db, skip=skip, limit=limit)

@router.get("/authors/{author_id}", response_model=author_schema.Author, tags=["Authors"])
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = author_service.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.put("/authors/{author_id}", response_model=author_schema.Author, tags=["Authors"])
def update_author(author_id: int, author: author_schema.AuthorUpdate, db: Session = Depends(get_db)):
    db_author = author_service.update_author(db=db, author_id=author_id, author=author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.delete("/authors/{author_id}", response_model=author_schema.Author, tags=["Authors"])
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = author_service.delete_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author