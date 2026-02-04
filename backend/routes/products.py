"""Product routes for the API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.schemas import ProductResponse, ProductCreate, ProductUpdate, MessageResponse
from backend.services.product_service import ProductService

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all products with optional filtering and pagination."""
    products = ProductService.get_all_products(db, skip=skip, limit=limit, category=category, search=search)
    return products


@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    """Get all product categories."""
    return ProductService.get_categories(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID."""
    return ProductService.get_product_by_id(db, product_id)


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product (admin only - authentication to be added)."""
    return ProductService.create_product(db, product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """Update a product (admin only - authentication to be added)."""
    return ProductService.update_product(db, product_id, product)


@router.delete("/{product_id}", response_model=MessageResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product (admin only - authentication to be added)."""
    ProductService.delete_product(db, product_id)
    return MessageResponse(message=f"Product {product_id} deleted successfully")
