# Online Shopping System

A full-stack e-commerce platform built with FastAPI backend, modern HTML/CSS/JavaScript frontend, and MySQL database.

## Features

- 🛍️ **Product Browsing**: Browse products with search and category filtering
- 🛒 **Shopping Cart**: Add, update, and remove items from cart
- 💳 **Checkout**: Complete orders with shipping information
- 📦 **Order History**: Track past orders and their status
- 🔐 **User Authentication**: Register and login functionality
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **MySQL**: Relational database
- **Pydantic**: Data validation
- **JWT**: Authentication tokens

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS variables
- **JavaScript**: Vanilla JS for API integration
- **Responsive Design**: Mobile-first approach

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Web server and reverse proxy

## Local Development Setup

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- Node.js (optional, for serving frontend)

### Step 1: Clone and Setup

```bash
cd OnlineShoppingSystem
python -m venv venv
```

### Step 2: Activate Virtual Environment

**Windows:**
```bash
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Copy `.env.example` to `.env` and update with your MySQL credentials:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=online_shopping
SECRET_KEY=your-secret-key
```

### Step 5: Initialize Database

```bash
python backend/init_db.py
```

This will create all tables and seed sample data.

### Step 6: Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Step 7: Run Frontend

Open `frontend/index.html` in a browser, or use a local server:

```bash
# Using Python
cd frontend
python -m http.server 5500
```

Frontend will be available at: `http://localhost:5500`

## Test Credentials

After running `init_db.py`, use these credentials:

**Regular User:**
- Username: `testuser`
- Password: `password123`

**Admin User:**
- Username: `admin`
- Password: `admin123`

## API Endpoints

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}` - Get product details
- `POST /api/products/` - Create product (admin)
- `PUT /api/products/{id}` - Update product (admin)
- `DELETE /api/products/{id}` - Delete product (admin)

### Cart
- `GET /api/cart/` - Get user's cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update/{item_id}` - Update cart item
- `DELETE /api/cart/remove/{item_id}` - Remove from cart
- `DELETE /api/cart/clear` - Clear cart

### Orders
- `POST /api/orders/checkout` - Create order from cart
- `GET /api/orders/` - Get user's orders
- `GET /api/orders/{id}` - Get order details

### Users
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - Login user
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update user profile

## Docker Deployment

### Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will start:
- MySQL database on port 3306
- FastAPI backend on port 8000
- Nginx frontend on port 80

Access the application at: `http://localhost`

### Stop Containers

```bash
docker-compose down
```

### Remove Volumes (Reset Database)

```bash
docker-compose down -v
```

## VM Deployment

### Prerequisites
- Linux VM (Ubuntu 20.04+ recommended)
- Docker and Docker Compose installed
- Cloud MySQL database (AWS RDS, Google Cloud SQL, etc.)

### Steps

1. **Clone repository on VM:**
```bash
git clone <your-repo-url>
cd OnlineShoppingSystem
```

2. **Update .env with cloud database credentials:**
```env
DB_HOST=your-cloud-db-host.com
DB_PORT=3306
DB_USER=cloud_user
DB_PASSWORD=cloud_password
DB_NAME=online_shopping
```

3. **Run with Docker Compose:**
```bash
docker-compose up -d
```

4. **Initialize database (first time only):**
```bash
docker exec -it shopping_backend python backend/init_db.py
```

## Project Structure

```
OnlineShoppingSystem/
├── backend/
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   ├── utils/           # Utilities (auth, validators, exceptions)
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   ├── main.py          # FastAPI app
│   ├── schemas.py       # Pydantic schemas
│   └── init_db.py       # Database initialization
├── frontend/
│   ├── styles/
│   │   └── main.css     # Styles
│   ├── scripts/
│   │   └── app.js       # JavaScript
│   ├── index.html       # Home page
│   ├── cart.html        # Cart page
│   ├── checkout.html    # Checkout page
│   └── orders.html      # Orders page
├── tests/               # Test files
├── .env                 # Environment variables
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Multi-container setup
├── nginx.conf           # Nginx configuration
└── README.md            # This file
```

## Troubleshooting

### Database Connection Error
- Ensure MySQL is running
- Check credentials in `.env`
- Verify database exists

### CORS Error
- Update `ALLOWED_ORIGINS` in `.env`
- Restart backend server

### Port Already in Use
- Change port in `uvicorn` command or `docker-compose.yml`

## License

This project is for educational purposes.
