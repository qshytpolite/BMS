from typing import Generator
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User
from .schemas import TokenData
from .utils import verify_token

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Dependency: Provide a scoped database session


def get_db() -> Generator:
    """Yield a database session and ensure it closes after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency: Get the current user based on token


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Retrieve the current user from the token."""
    try:
        token_data = verify_token(token)  # Validate and decode the token
        user = db.query(User).filter(User.id == token_data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e

# Dependency: Check if the user is an admin


def require_admin(user: User = Depends(get_current_user)) -> None:
    """Raise an exception if the user is not an admin."""
    if not user.is_admin:
        raise HTTPException(
            status_code=403, detail="Admin privileges required")
