"""Order service containing business logic for order operations."""
from sqlalchemy.orm import Session
from typing import List
from backend.models.order import Order, OrderItem, OrderStatus
from backend.models.cart import Cart
from backend.schemas import OrderCreate, OrderStatusUpdate
from backend.utils.exceptions import NotFoundException, BadRequestException
from backend.services.cart_service import CartService
from backend.services.product_service import ProductService


class OrderService:
    """Service class for order operations."""
    
    @staticmethod
    def create_order_from_cart(db: Session, user_id: int, order_data: OrderCreate) -> Order:
        """Create an order from user's cart (checkout)."""
        # Get cart items
        cart_items = CartService.get_user_cart(db, user_id)
        
        if not cart_items:
            raise BadRequestException("Cart is empty. Cannot create order.")
        
        # Calculate total and verify stock availability
        total_amount = 0.0
        order_items_data = []
        
        for cart_item in cart_items:
            product = cart_item.product
            
            if not product:
                raise NotFoundException(f"Product with ID {cart_item.product_id} not found")
            
            # Check stock availability
            if not ProductService.check_stock_availability(db, product.id, cart_item.quantity):
                raise BadRequestException(
                    f"Insufficient stock for {product.name}. Available: {product.stock_quantity}"
                )
            
            # Calculate item total
            item_total = product.price * cart_item.quantity
            total_amount += item_total
            
            # Prepare order item data
            order_items_data.append({
                "product_id": product.id,
                "quantity": cart_item.quantity,
                "price_at_purchase": product.price
            })
        
        # Create order
        order = Order(
            user_id=user_id,
            total_amount=round(total_amount, 2),
            status=OrderStatus.PENDING,
            shipping_address=order_data.shipping_address,
            payment_method=order_data.payment_method
        )
        db.add(order)
        db.flush()  # Get order ID without committing
        
        # Create order items and reduce stock
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                **item_data
            )
            db.add(order_item)
            
            # Reduce product stock
            ProductService.reduce_stock(db, item_data["product_id"], item_data["quantity"])
        
        # Clear cart after successful order
        CartService.clear_cart(db, user_id)
        
        db.commit()
        db.refresh(order)
        return order
    
    @staticmethod
    def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders for a user."""
        return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_order_by_id(db: Session, order_id: int, user_id: int = None) -> Order:
        """Get an order by ID."""
        query = db.query(Order).filter(Order.id == order_id)
        
        # If user_id is provided, ensure order belongs to user
        if user_id is not None:
            query = query.filter(Order.user_id == user_id)
        
        order = query.first()
        
        if not order:
            raise NotFoundException(f"Order with ID {order_id} not found")
        
        return order
    
    @staticmethod
    def update_order_status(db: Session, order_id: int, status_update: OrderStatusUpdate) -> Order:
        """Update order status (admin only)."""
        order = OrderService.get_order_by_id(db, order_id)
        
        order.status = status_update.status
        db.commit()
        db.refresh(order)
        return order
    
    @staticmethod
    def get_all_orders(db: Session, skip: int = 0, limit: int = 100, status: OrderStatus = None) -> List[Order]:
        """Get all orders (admin only) with optional status filter."""
        query = db.query(Order).order_by(Order.created_at.desc())
        
        if status:
            query = query.filter(Order.status == status)
        
        return query.offset(skip).limit(limit).all()
