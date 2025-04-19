from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.database_connection import Base

book_author = Table(
    "book_authors",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE")),
    Column("author_id", Integer, ForeignKey("authors.id", ondelete="CASCADE")),
)