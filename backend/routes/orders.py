"""Order routes for the API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import OrderCreate, OrderResponse, OrderStatusUpdate, MessageResponse
from backend.services.order_service import OrderService
from backend.routes.users import get_current_user_id

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/checkout", response_model=OrderResponse, status_code=201)
def checkout(
    order_data: OrderCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create an order from cart (checkout)."""
    return OrderService.create_order_from_cart(db, user_id, order_data)


@router.get("/", response_model=List[OrderResponse])
def get_user_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's order history."""
    return OrderService.get_user_orders(db, user_id, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get a specific order by ID."""
    return OrderService.get_order_by_id(db, order_id, user_id=user_id)


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    """Update order status (admin only - authentication to be added)."""
    return OrderService.update_order_status(db, order_id, status_update)
