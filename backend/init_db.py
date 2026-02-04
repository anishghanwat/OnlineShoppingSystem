"""Database initialization and seeding script."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.database import engine, Base, SessionLocal
from backend.models.product import Product
from backend.models.user import User
from backend.models.cart import Cart
from backend.models.order import Order, OrderItem
from backend.utils.auth import hash_password


def init_database():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def seed_sample_data():
    """Seed the database with sample data."""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_products = db.query(Product).count()
        if existing_products > 0:
            print("Database already contains data. Skipping seeding.")
            return
        
        print("Seeding sample data...")
        
        # Create sample products
        products = [
            Product(
                name="Laptop - Dell XPS 15",
                description="High-performance laptop with Intel i7 processor, 16GB RAM, 512GB SSD",
                price=1299.99,
                category="Electronics",
                stock_quantity=15,
                image_url="https://loremflickr.com/300/300/laptop"
            ),
            Product(
                name="Wireless Mouse",
                description="Ergonomic wireless mouse with 2.4GHz connectivity",
                price=29.99,
                category="Electronics",
                stock_quantity=50,
                image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=300&q=80"
            ),
            Product(
                name="Mechanical Keyboard",
                description="RGB mechanical keyboard with blue switches",
                price=89.99,
                category="Electronics",
                stock_quantity=30,
                image_url="https://loremflickr.com/300/300/keyboard"
            ),
            Product(
                name="Running Shoes",
                description="Comfortable running shoes with cushioned sole",
                price=79.99,
                category="Sports",
                stock_quantity=40,
                image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=300&q=80"
            ),
            Product(
                name="Yoga Mat",
                description="Non-slip yoga mat with carrying strap",
                price=24.99,
                category="Sports",
                stock_quantity=60,
                image_url="https://loremflickr.com/300/300/yoga"
            ),
            Product(
                name="Coffee Maker",
                description="Programmable coffee maker with 12-cup capacity",
                price=49.99,
                category="Home",
                stock_quantity=25,
                image_url="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=300&q=80"
            ),
            Product(
                name="Blender",
                description="High-speed blender for smoothies and shakes",
                price=59.99,
                category="Home",
                stock_quantity=20,
                image_url="https://loremflickr.com/300/300/blender"
            ),
            Product(
                name="Fiction Book - The Great Novel",
                description="Bestselling fiction novel",
                price=14.99,
                category="Books",
                stock_quantity=100,
                image_url="https://images.unsplash.com/photo-1543002588-bfa74002ed7e?auto=format&fit=crop&w=300&q=80"
            ),
            Product(
                name="Headphones - Sony WH-1000XM4",
                description="Noise-cancelling wireless headphones",
                price=349.99,
                category="Electronics",
                stock_quantity=20,
                image_url="https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?auto=format&fit=crop&w=300&q=80"
            ),
            Product(
                name="Water Bottle",
                description="Insulated stainless steel water bottle, 32oz",
                price=19.99,
                category="Sports",
                stock_quantity=75,
                image_url="https://loremflickr.com/300/300/waterbottle"
            ),
        ]
        
        db.add_all(products)
        
        # Create a test user
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=hash_password("password123"),
            full_name="Test User",
            phone="1234567890",
            address="123 Test Street, Test City, TC 12345",
            is_active=True,
            is_admin=False
        )
        db.add(test_user)
        
        # Create an admin user
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            full_name="Admin User",
            is_active=True,
            is_admin=True
        )
        db.add(admin_user)
        
        db.commit()
        print("Sample data seeded successfully!")
        print("\nTest User Credentials:")
        print("  Username: testuser")
        print("  Password: password123")
        print("\nAdmin User Credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    seed_sample_data()
