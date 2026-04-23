from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.services.user import get_user_by_email, create_user
from app.deps import get_db

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user.email, user.password)
