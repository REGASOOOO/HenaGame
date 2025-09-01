from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Dict
from sqlalchemy.orm import Session

from ..database.db import get_db
from ..models.userModel import User
from passlib.context import CryptContext
from ..security.jwt import create_access_token, get_username_from_token, TokenError

# Create a router for auth endpoints
router = APIRouter(prefix="/auth", tags=["authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(credentials: UserCredentials, db: Session = Depends(get_db)) -> Dict[str, str]:
    if not credentials.username:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Username required")
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not pwd_context.verify(credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

def _get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        username = get_username_from_token(token)
    except TokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.get("/me", status_code=status.HTTP_200_OK)
async def read_me(current_user: User = Depends(_get_current_user)) -> Dict[str, str]:
    print(current_user)
    return {"username": current_user.username}


@router.delete("/profile/{username}", status_code=status.HTTP_200_OK)
async def delete_profile(username: str, current_user: User = Depends(_get_current_user)) -> Dict[str, str]:
    if current_user.username != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    # TODO: implement delete logic
    return {"message": f"User {username} profile deleted (stub)"}
