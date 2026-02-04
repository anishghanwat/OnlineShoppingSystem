"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from backend.models.order import OrderStatus


# ============= Product Schemas =============

class ProductBase(BaseModel):
    """Base product schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    stock_quantity: int = Field(..., ge=0)
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    stock_quantity: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None


class ProductResponse(ProductBase):
    """Schema for product response."""
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ============= User Schemas =============

class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    is_admin: bool
    created_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"


# ============= Cart Schemas =============

class CartItemCreate(BaseModel):
    """Schema for adding item to cart."""
    product_id: int = Field(..., gt=0)
    quantity: int = Field(default=1, gt=0)


class CartItemUpdate(BaseModel):
    """Schema for updating cart item."""
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    """Schema for cart item response."""
    id: int
    product_id: int
    quantity: int
    added_at: Optional[datetime]
    product: Optional[ProductResponse]
    
    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Schema for cart response."""
    items: List[CartItemResponse]
    total_items: int
    total_price: float


# ============= Order Schemas =============

class OrderItemResponse(BaseModel):
    """Schema for order item response."""
    id: int
    product_id: int
    quantity: int
    price_at_purchase: float
    product: Optional[ProductResponse]
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Schema for creating an order (checkout)."""
    shipping_address: str = Field(..., min_length=10, max_length=500)
    payment_method: Optional[str] = Field(default="cash_on_delivery", max_length=50)


class OrderResponse(BaseModel):
    """Schema for order response."""
    id: int
    user_id: int
    total_amount: float
    status: str
    shipping_address: str
    payment_method: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status."""
    status: OrderStatus


# ============= Generic Response Schemas =============

class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    detail: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: Optional[str] = None
