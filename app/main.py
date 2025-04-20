from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.database_connection import engine, Base

from app.database.database_connection import Base, engine
from app.controller import user_controller, author_controller, book_controller

app = FastAPI()

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your React app URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(user_controller.router, tags=["Users"], prefix="/user")
app.include_router(author_controller.router, tags=["Authors"], prefix="/author")
app.include_router(book_controller.router, tags=["Books"], prefix="/book")

# Create tables in the database
try:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")
    raise  # Re-raise the exception for visibility

# User related operations
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI regarding the BOOK related operations....!"}
