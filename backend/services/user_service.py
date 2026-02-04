"""User service containing business logic for user operations."""
from sqlalchemy.orm import Session
from typing import Optional
from backend.models.user import User
from backend.schemas import UserCreate, UserUpdate
from backend.utils.exceptions import NotFoundException, BadRequestException, UnauthorizedException
from backend.utils.auth import hash_password, verify_password, create_access_token
from backend.utils.validators import validate_email


class UserService:
    """Service class for user operations."""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user (registration)."""
        # Validate email
        validate_email(user_data.email)
        
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise BadRequestException(f"Username '{user_data.username}' already exists")
        
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise BadRequestException(f"Email '{user_data.email}' already registered")
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create user
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            address=user_data.address
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> tuple[User, str]:
        """Authenticate user and return user object with access token."""
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            raise UnauthorizedException("Invalid username or password")
        
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException("Invalid username or password")
        
        if not user.is_active:
            raise UnauthorizedException("User account is inactive")
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
        
        return user, access_token
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        """Update user profile."""
        user = UserService.get_user_by_id(db, user_id)
        
        # Update only provided fields
        update_data = user_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        """Delete user account."""
        user = UserService.get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
