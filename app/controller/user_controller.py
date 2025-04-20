from fastapi import APIRouter, Depends, HTTPException, status
import app
from app.Schemas import user_schema
from app.database.database_connection import get_db
from sqlalchemy.orm import Session
from app.services import user_service

router = APIRouter()

@router.get("/user", response_model=user_schema.User, tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/register", response_model=user_schema.User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def register_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_service.post_user(db=db, user=user)

@router.put("/update_user/{user_id}", response_model=user_schema.User, tags=["Users"])
def update_user(user_id: int, user: user_schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = user_service.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/delete_user/{user_id}", response_model=user_schema.User, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/user_by_name/{username}", response_model=user_schema.User, tags=["Users"])
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user