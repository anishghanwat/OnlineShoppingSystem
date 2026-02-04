"""Simple database test script."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

try:
    print("Step 1: Importing database...")
    from backend.database import engine, Base
    print("✓ Database imported")
    
    print("\nStep 2: Importing models...")
    from backend.models.product import Product
    from backend.models.user import User
    from backend.models.cart import Cart
    from backend.models.order import Order, OrderItem
    print("✓ Models imported")
    
    print("\nStep 3: Testing database connection...")
    with engine.connect() as conn:
        print("✓ Database connection successful")
    
    print("\nStep 4: Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully!")
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}")
    print(f"Message: {str(e)}")
    import traceback
    traceback.print_exc()
