from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict
from sqlalchemy.orm import Session

from ..database.db import get_db
from ..models.userModel import User
from passlib.context import CryptContext

# Create a router for auth endpoints
router = APIRouter(prefix="/auth", tags=["authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models for request validation
class UserCredentials(BaseModel):
    username: str | None
    password: str 



# Routes
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(credentials: UserCredentials, db: Session = Depends(get_db)) -> Dict[str, str]:
    # Vérifie si l'utilisateur existe
    existing = db.query(User).filter(User.username == credentials.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    # Hash du mot de passe
    password_hash = pwd_context.hash(credentials.password)
    # Adapter selon les champs de ton modèle User
    user = User(username=credentials.username, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": f"Utilisateur {user.username} créé"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(credentials: UserCredentials) -> Dict[str, str]:
    """Login a user"""
    return {"message": f"User {credentials.username} logged in successfully"}

@router.delete("/profile/{username}", status_code=status.HTTP_200_OK)
async def delete_profile(username: str) -> Dict[str, str]:
    """Delete a user profile"""
    return {"message": f"User {username} profile deleted successfully"}
