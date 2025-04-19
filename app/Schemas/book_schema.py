from datetime import date
from typing import Optional, List
from pydantic import BaseModel

from .author_schema import AuthorInBook


class BookBase(BaseModel):
    title: str
    isbn: str
    publication_date: Optional[date] = None
    genre: Optional[str] = None

class BookCreate(BookBase):
    author_ids: Optional[List[int]] = []

class BookUpdate(BookBase):
    title: Optional[str] = None
    isbn: Optional[str] = None
    author_ids: Optional[List[int]] = []

class Book(BookBase):
    id: int
    authors: List[AuthorInBook] = []

    class Config:
        from_attributes = True