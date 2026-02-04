"""Cart service containing business logic for shopping cart operations."""
from sqlalchemy.orm import Session
from typing import List
from backend.models.cart import Cart
from backend.models.product import Product
from backend.schemas import CartItemCreate, CartItemUpdate
from backend.utils.exceptions import NotFoundException, BadRequestException
from backend.services.product_service import ProductService


class CartService:
    """Service class for cart operations."""
    
    @staticmethod
    def get_user_cart(db: Session, user_id: int) -> List[Cart]:
        """Get all items in user's cart."""
        return db.query(Cart).filter(Cart.user_id == user_id).all()
    
    @staticmethod
    def add_to_cart(db: Session, user_id: int, cart_item: CartItemCreate) -> Cart:
        """Add an item to the cart or update quantity if already exists."""
        # Verify product exists and has sufficient stock
        product = ProductService.get_product_by_id(db, cart_item.product_id)
        
        if product.stock_quantity < cart_item.quantity:
            raise BadRequestException(
                f"Insufficient stock for {product.name}. Available: {product.stock_quantity}"
            )
        
        # Check if item already in cart
        existing_item = db.query(Cart).filter(
            Cart.user_id == user_id,
            Cart.product_id == cart_item.product_id
        ).first()
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + cart_item.quantity
            
            if product.stock_quantity < new_quantity:
                raise BadRequestException(
                    f"Insufficient stock for {product.name}. Available: {product.stock_quantity}"
                )
            
            existing_item.quantity = new_quantity
            db.commit()
            db.refresh(existing_item)
            return existing_item
        else:
            # Create new cart item
            new_cart_item = Cart(
                user_id=user_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity
            )
            db.add(new_cart_item)
            db.commit()
            db.refresh(new_cart_item)
            return new_cart_item
    
    @staticmethod
    def update_cart_item(db: Session, user_id: int, item_id: int, update_data: CartItemUpdate) -> Cart:
        """Update cart item quantity."""
        cart_item = db.query(Cart).filter(
            Cart.id == item_id,
            Cart.user_id == user_id
        ).first()
        
        if not cart_item:
            raise NotFoundException("Cart item not found")
        
        # Verify stock availability
        product = ProductService.get_product_by_id(db, cart_item.product_id)
        
        if product.stock_quantity < update_data.quantity:
            raise BadRequestException(
                f"Insufficient stock for {product.name}. Available: {product.stock_quantity}"
            )
        
        cart_item.quantity = update_data.quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item
    
    @staticmethod
    def remove_from_cart(db: Session, user_id: int, item_id: int) -> None:
        """Remove an item from the cart."""
        cart_item = db.query(Cart).filter(
            Cart.id == item_id,
            Cart.user_id == user_id
        ).first()
        
        if not cart_item:
            raise NotFoundException("Cart item not found")
        
        db.delete(cart_item)
        db.commit()
    
    @staticmethod
    def clear_cart(db: Session, user_id: int) -> None:
        """Clear all items from user's cart."""
        db.query(Cart).filter(Cart.user_id == user_id).delete()
        db.commit()
    
    @staticmethod
    def get_cart_total(db: Session, user_id: int) -> dict:
        """Calculate cart total price and item count."""
        cart_items = CartService.get_user_cart(db, user_id)
        
        total_price = 0.0
        total_items = 0
        
        for item in cart_items:
            if item.product:
                total_price += item.product.price * item.quantity
                total_items += item.quantity
        
        return {
            "total_price": round(total_price, 2),
            "total_items": total_items
        }
