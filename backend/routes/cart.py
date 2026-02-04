"""Cart routes for the API."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import CartItemCreate, CartItemUpdate, CartItemResponse, CartResponse, MessageResponse
from backend.services.cart_service import CartService
from backend.routes.users import get_current_user_id

router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.get("/", response_model=CartResponse)
def get_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Get current user's cart."""
    cart_items = CartService.get_user_cart(db, user_id)
    cart_total = CartService.get_cart_total(db, user_id)
    
    return CartResponse(
        items=[CartItemResponse.model_validate(item) for item in cart_items],
        total_items=cart_total["total_items"],
        total_price=cart_total["total_price"]
    )


@router.post("/add", response_model=CartItemResponse, status_code=201)
def add_to_cart(
    cart_item: CartItemCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Add an item to the cart."""
    return CartService.add_to_cart(db, user_id, cart_item)


@router.put("/update/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    update_data: CartItemUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update cart item quantity."""
    return CartService.update_cart_item(db, user_id, item_id, update_data)


@router.delete("/remove/{item_id}", response_model=MessageResponse)
def remove_from_cart(
    item_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Remove an item from the cart."""
    CartService.remove_from_cart(db, user_id, item_id)
    return MessageResponse(message="Item removed from cart")


@router.delete("/clear", response_model=MessageResponse)
def clear_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Clear all items from the cart."""
    CartService.clear_cart(db, user_id)
    return MessageResponse(message="Cart cleared successfully")
