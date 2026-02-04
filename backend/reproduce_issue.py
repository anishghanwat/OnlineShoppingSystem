from backend.utils.auth import hash_password

try:
    pwd = "password123"
    print(f"Password: '{pwd}', Type: {type(pwd)}, Length: {len(pwd)}")
    from passlib.context import CryptContext
    ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    print(f"Schemes: {ctx.schemes()}")
    hashed = hash_password(pwd)
    print(f"Success: {hashed}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
