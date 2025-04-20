from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.database_connection import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define the User class first
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)  
    last_name = Column(String(50), nullable=True)  
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)

    def set_password(self, password: str):
        self.password = pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)

# Define the Book class first
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    publication_date = Column(Date)
    genre = Column(String)
    price = Column(Integer, nullable=True)
    description = Column(String, nullable=True)

    authors = relationship("Author", secondary="book_authors", back_populates="books", lazy="joined")

# Define the Author class
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    books = relationship("Book", secondary="book_authors", back_populates="authors", lazy="joined")

# Define the association table last
book_author = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE")),
    Column("author_id", Integer, ForeignKey("authors.id", ondelete="CASCADE")),
)

__all__ = ['Book', 'Author', 'book_author', 'User']