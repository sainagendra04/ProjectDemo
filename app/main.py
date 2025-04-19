from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware  # Add this import

from .Schemas import book_schema, author_schema  # Add author_schema import

from . import operations
from .database.database_connection import get_db, engine, Base
from sqlalchemy.orm import Session

from app.database.database_connection import Base, engine

app = FastAPI()

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your React app URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create tables in the database
try:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")
    raise  # Re-raise the exception for visibility

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI regarding the BOOK related operations....!"}

@app.post("/books", response_model=book_schema.Book, status_code=status.HTTP_201_CREATED, tags=["Books"])
def create_book(book: book_schema.BookCreate, db: Session = Depends(get_db)):
    return operations.create_book(db=db, book=book)

@app.get("/books/", response_model=List[book_schema.Book], tags=["Books"])
def get_all_books(db: Session = Depends(get_db)):
    return operations.get_books(db=db, skip=0, limit=10)

@app.get("/book/{book_id}", response_model=book_schema.Book, tags=["Books"])
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    db_book = operations.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with the Id not found")
    return db_book

@app.get("/book/name/{name}", response_model=book_schema.Book, tags=["Books"])
def get_book_by_name(title: str, db: Session = Depends(get_db)):
    db_book = operations.get_book_by_name(db=db, name=title)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with the name not found")
    return db_book

@app.put("/book/{book_id}", response_model=book_schema.Book, tags=["Books"])
def update_book(book_id: int, book: book_schema.BookUpdate, db: Session = Depends(get_db)):
    db_book = operations.update_book(db=db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with the Id not found")
    return db_book

@app.delete("/book/{book_id}", response_model=book_schema.Book, tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = operations.delete_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with the Id not found")
    return db_book

# Author endpoints
@app.post("/authors/", response_model=author_schema.Author, status_code=status.HTTP_201_CREATED, tags=["Authors"])
def create_author(author: author_schema.AuthorCreate, db: Session = Depends(get_db)):
    return operations.create_author(db=db, author=author)

@app.get("/authors/", response_model=List[author_schema.Author], tags=["Authors"])
def get_all_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return operations.get_authors(db=db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=author_schema.Author, tags=["Authors"])
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = operations.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.put("/authors/{author_id}", response_model=author_schema.Author, tags=["Authors"])
def update_author(author_id: int, author: author_schema.AuthorUpdate, db: Session = Depends(get_db)):
    db_author = operations.update_author(db=db, author_id=author_id, author=author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.delete("/authors/{author_id}", response_model=author_schema.Author, tags=["Authors"])
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = operations.delete_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author
