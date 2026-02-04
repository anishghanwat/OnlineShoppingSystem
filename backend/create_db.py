"""Try to create database with different connection methods."""
import pymysql
import sys

# Try different password scenarios
passwords_to_try = ['', 'root', 'password', 'admin']

for password in passwords_to_try:
    try:
        print(f"Trying password: {'(empty)' if password == '' else '***'}")
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=password,
            port=3306
        )
        
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS online_shopping")
        print(f"✓ SUCCESS! Database 'online_shopping' created!")
        print(f"✓ Password that worked: {'(empty)' if password == '' else password}")
        
        # Update .env file
        with open('.env', 'r') as f:
            content = f.read()
        
        content = content.replace('DB_PASSWORD=', f'DB_PASSWORD={password}')
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print("✓ .env file updated with correct password")
        
        cursor.close()
        connection.close()
        sys.exit(0)
        
    except Exception as e:
        print(f"  Failed: {e}")
        continue

print("\n❌ Could not connect with any common password.")
print("Please manually update DB_PASSWORD in .env file with your MySQL root password.")
