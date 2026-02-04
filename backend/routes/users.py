"""User routes for the API."""
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from backend.database import get_db
from backend.schemas import UserCreate, UserResponse, UserLogin, Token, UserUpdate, MessageResponse
from backend.services.user_service import UserService
from backend.utils.auth import decode_access_token
from backend.utils.exceptions import UnauthorizedException

router = APIRouter(prefix="/api/users", tags=["Users"])


def get_current_user_id(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> int:
    """Dependency to get current user ID from JWT token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException("Missing or invalid authorization header")
    
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    
    if not payload:
        raise UnauthorizedException("Invalid or expired token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload")
    
    return int(user_id)


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return UserService.create_user(db, user)


@router.post("/login", response_model=Token)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token."""
    user, access_token = UserService.authenticate_user(db, credentials.username, credentials.password)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def get_current_user(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Get current user profile."""
    return UserService.get_user_by_id(db, user_id)


@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_data: UserUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    return UserService.update_user(db, user_id, user_data)


@router.delete("/me", response_model=MessageResponse)
def delete_current_user(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Delete current user account."""
    UserService.delete_user(db, user_id)
    return MessageResponse(message="User account deleted successfully")
