from typing import Optional, List
from pydantic import BaseModel
from datetime import date

class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    description: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None

# This class is used when we need author info without books
class AuthorInBook(AuthorBase):
    id: int

    class Config:
        from_attributes = True

# Main Author class for full author details
class Author(AuthorBase):
    id: int
    books: List["BookInAuthor"] = []

    class Config:
        from_attributes = True

# Simplified Book representation for Author responses
class BookInAuthor(BaseModel):
    id: int
    title: str
    isbn: str
    publication_date: Optional[date] = None
    genre: Optional[str] = None

    class Config:
        from_attributes = True

# Update forward references
Author.model_rebuild()