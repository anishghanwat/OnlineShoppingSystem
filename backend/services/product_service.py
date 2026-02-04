"""Product service containing business logic for product operations."""
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models.product import Product
from backend.schemas import ProductCreate, ProductUpdate
from backend.utils.exceptions import NotFoundException, BadRequestException
from backend.utils.validators import validate_positive_number, validate_non_negative_integer


class ProductService:
    """Service class for product operations."""
    
    @staticmethod
    def get_all_products(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Product]:
        """Get all products with optional filtering and pagination."""
        query = db.query(Product)
        
        # Filter by category if provided
        if category:
            query = query.filter(Product.category == category)
        
        # Search by name or description if provided
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (Product.name.ilike(search_pattern)) | 
                (Product.description.ilike(search_pattern))
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product:
        """Get a product by ID."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise NotFoundException(f"Product with ID {product_id} not found")
        return product
    
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        """Create a new product."""
        # Validate data
        validate_positive_number(product_data.price, "Price")
        validate_non_negative_integer(product_data.stock_quantity, "Stock quantity")
        
        # Create product
        product = Product(**product_data.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Product:
        """Update an existing product."""
        product = ProductService.get_product_by_id(db, product_id)
        
        # Update only provided fields
        update_data = product_data.model_dump(exclude_unset=True)
        
        # Validate if price is being updated
        if "price" in update_data:
            validate_positive_number(update_data["price"], "Price")
        
        # Validate if stock_quantity is being updated
        if "stock_quantity" in update_data:
            validate_non_negative_integer(update_data["stock_quantity"], "Stock quantity")
        
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> None:
        """Delete a product."""
        product = ProductService.get_product_by_id(db, product_id)
        db.delete(product)
        db.commit()
    
    @staticmethod
    def get_categories(db: Session) -> List[str]:
        """Get all unique product categories."""
        categories = db.query(Product.category).distinct().all()
        return [cat[0] for cat in categories]
    
    @staticmethod
    def check_stock_availability(db: Session, product_id: int, quantity: int) -> bool:
        """Check if sufficient stock is available."""
        product = ProductService.get_product_by_id(db, product_id)
        return product.stock_quantity >= quantity
    
    @staticmethod
    def reduce_stock(db: Session, product_id: int, quantity: int) -> None:
        """Reduce product stock."""
        product = ProductService.get_product_by_id(db, product_id)
        
        if product.stock_quantity < quantity:
            raise BadRequestException(
                f"Insufficient stock for {product.name}. Available: {product.stock_quantity}, Requested: {quantity}"
            )
        
        product.stock_quantity -= quantity
        db.commit()
