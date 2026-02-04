// API Configuration
const API_BASE_URL = '';

// ============= Utility Functions =============

function getAuthToken() {
    return localStorage.getItem('authToken');
}

function setAuthToken(token) {
    localStorage.setItem('authToken', token);
}

function removeAuthToken() {
    localStorage.removeItem('authToken');
}

function getCurrentUser() {
    const userStr = localStorage.getItem('currentUser');
    return userStr ? JSON.parse(userStr) : null;
}

function setCurrentUser(user) {
    localStorage.setItem('currentUser', JSON.stringify(user));
}

function removeCurrentUser() {
    localStorage.removeItem('currentUser');
}

function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) return;

    const alertClass = type === 'success' ? 'alert-success' : type === 'error' ? 'alert-error' : 'alert-info';
    const alert = document.createElement('div');
    alert.className = `alert ${alertClass}`;
    alert.textContent = message;

    alertContainer.innerHTML = '';
    alertContainer.appendChild(alert);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

function showLoading(show = true) {
    const loadingState = document.getElementById('loadingState');
    if (loadingState) {
        loadingState.classList.toggle('hidden', !show);
    }
}

// ============= API Functions =============

async function apiRequest(endpoint, options = {}) {
    const token = getAuthToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || error.detail || 'Request failed');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ============= Authentication Functions =============

function checkAuth() {
    const token = getAuthToken();
    const user = getCurrentUser();
    const authLink = document.getElementById('authLink');

    if (authLink) {
        if (token && user) {
            authLink.textContent = `Hi, ${user.username}`;
            authLink.onclick = logout;
        } else {
            authLink.textContent = 'Login';
            authLink.onclick = showLoginModal;
        }
    }
}

function showLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.style.display = 'flex';
        document.getElementById('loginForm').classList.remove('hidden');
        document.getElementById('registerForm').classList.add('hidden');
    }
}

function closeLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function showRegisterForm() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
}

function showLoginForm() {
    document.getElementById('registerForm').classList.add('hidden');
    document.getElementById('loginForm').classList.remove('hidden');
}

async function handleLogin() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    if (!username || !password) {
        showAlert('Please enter username and password', 'error');
        return;
    }

    try {
        const response = await apiRequest('/api/users/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });

        setAuthToken(response.access_token);

        // Fetch user profile
        const user = await apiRequest('/api/users/me');
        setCurrentUser(user);

        showAlert('Login successful!', 'success');
        closeLoginModal();
        checkAuth();

        // Reload page data
        location.reload();
    } catch (error) {
        showAlert(error.message || 'Login failed', 'error');
    }
}

async function handleRegister() {
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const fullName = document.getElementById('regFullName').value;

    if (!username || !email || !password) {
        showAlert('Please fill in all required fields', 'error');
        return;
    }

    try {
        await apiRequest('/api/users/register', {
            method: 'POST',
            body: JSON.stringify({
                username,
                email,
                password,
                full_name: fullName || null
            })
        });

        showAlert('Registration successful! Please login.', 'success');
        showLoginForm();
    } catch (error) {
        showAlert(error.message || 'Registration failed', 'error');
    }
}

function logout() {
    removeAuthToken();
    removeCurrentUser();
    showAlert('Logged out successfully', 'success');
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1000);
}

// ============= Product Functions =============

async function loadCategories() {
    try {
        const categories = await apiRequest('/api/products/categories');
        const categoryFilter = document.getElementById('categoryFilter');

        if (categoryFilter) {
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categoryFilter.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

async function loadProducts() {
    showLoading(true);

    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');

    const search = searchInput ? searchInput.value : '';
    const category = categoryFilter ? categoryFilter.value : '';

    let endpoint = '/api/products/?limit=100';
    if (search) endpoint += `&search=${encodeURIComponent(search)}`;
    if (category) endpoint += `&category=${encodeURIComponent(category)}`;

    try {
        const products = await apiRequest(endpoint);
        displayProducts(products);
    } catch (error) {
        showAlert('Error loading products', 'error');
    } finally {
        showLoading(false);
    }
}

function displayProducts(products) {
    const productGrid = document.getElementById('productGrid');
    const emptyState = document.getElementById('emptyState');

    if (!productGrid) return;

    if (products.length === 0) {
        productGrid.innerHTML = '';
        if (emptyState) emptyState.classList.remove('hidden');
        return;
    }

    if (emptyState) emptyState.classList.add('hidden');

    productGrid.innerHTML = products.map(product => `
        <div class="card product-card">
            <img src="${product.image_url || 'https://via.placeholder.com/300x200?text=Product'}" 
                 alt="${product.name}" 
                 class="card-img">
            <div class="card-body">
                <span class="product-category">${product.category}</span>
                <h3 class="card-title">${product.name}</h3>
                <p class="card-text">${product.description || 'No description available'}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                    <span class="product-price">$${product.price.toFixed(2)}</span>
                    <span class="product-stock ${product.stock_quantity === 0 ? 'stock-out' : product.stock_quantity < 10 ? 'stock-low' : ''}">
                        ${product.stock_quantity === 0 ? 'Out of Stock' : `${product.stock_quantity} in stock`}
                    </span>
                </div>
            </div>
            <div class="card-footer">
                <button class="btn btn-primary btn-sm" 
                        onclick="addToCart(${product.id})" 
                        ${product.stock_quantity === 0 ? 'disabled' : ''}>
                    Add to Cart
                </button>
            </div>
        </div>
    `).join('');
}

function applyFilters() {
    loadProducts();
}

function clearFilters() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');

    if (searchInput) searchInput.value = '';
    if (categoryFilter) categoryFilter.value = '';

    loadProducts();
}

// ============= Cart Functions =============

async function addToCart(productId, quantity = 1) {
    const token = getAuthToken();
    if (!token) {
        showAlert('Please login to add items to cart', 'error');
        showLoginModal();
        return;
    }

    try {
        await apiRequest('/api/cart/add', {
            method: 'POST',
            body: JSON.stringify({ product_id: productId, quantity })
        });

        showAlert('Item added to cart!', 'success');
        updateCartBadge();
    } catch (error) {
        showAlert(error.message || 'Failed to add item to cart', 'error');
    }
}

async function updateCartBadge() {
    const token = getAuthToken();
    const cartBadge = document.getElementById('cartCount');

    if (!cartBadge) return;

    if (!token) {
        cartBadge.textContent = '0';
        return;
    }

    try {
        const cart = await apiRequest('/api/cart/');
        cartBadge.textContent = cart.total_items || 0;
    } catch (error) {
        console.error('Error updating cart badge:', error);
        cartBadge.textContent = '0';
    }
}

async function loadCart() {
    const token = getAuthToken();
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    showLoading(true);

    try {
        const cart = await apiRequest('/api/cart/');
        displayCart(cart);
    } catch (error) {
        showAlert('Error loading cart', 'error');
    } finally {
        showLoading(false);
    }
}

function displayCart(cart) {
    const cartItems = document.getElementById('cartItems');
    const emptyCart = document.getElementById('emptyCart');
    const cartContent = document.getElementById('cartContent');
    const subtotal = document.getElementById('subtotal');
    const totalItems = document.getElementById('totalItems');
    const total = document.getElementById('total');

    if (!cart.items || cart.items.length === 0) {
        if (emptyCart) emptyCart.classList.remove('hidden');
        if (cartContent) cartContent.classList.add('hidden');
        return;
    }

    if (emptyCart) emptyCart.classList.add('hidden');
    if (cartContent) cartContent.classList.remove('hidden');

    if (cartItems) {
        cartItems.innerHTML = cart.items.map(item => `
            <div class="cart-item">
                <img src="${item.product?.image_url || 'https://via.placeholder.com/100'}" 
                     alt="${item.product?.name}" 
                     class="cart-item-img">
                <div class="cart-item-details">
                    <h4 class="cart-item-title">${item.product?.name}</h4>
                    <p class="cart-item-price">$${item.product?.price.toFixed(2)} each</p>
                    <div class="quantity-controls">
                        <button class="quantity-btn" onclick="updateCartItemQuantity(${item.id}, ${item.quantity - 1})">-</button>
                        <span class="quantity-display">${item.quantity}</span>
                        <button class="quantity-btn" onclick="updateCartItemQuantity(${item.id}, ${item.quantity + 1})">+</button>
                    </div>
                </div>
                <div style="text-align: right;">
                    <p class="cart-item-price">$${(item.product?.price * item.quantity).toFixed(2)}</p>
                    <button class="btn btn-danger btn-sm" onclick="removeFromCart(${item.id})">Remove</button>
                </div>
            </div>
        `).join('');
    }

    if (subtotal) subtotal.textContent = `$${cart.total_price.toFixed(2)}`;
    if (totalItems) totalItems.textContent = cart.total_items;
    if (total) total.textContent = `$${cart.total_price.toFixed(2)}`;
}

async function updateCartItemQuantity(itemId, newQuantity) {
    if (newQuantity < 1) {
        removeFromCart(itemId);
        return;
    }

    try {
        await apiRequest(`/api/cart/update/${itemId}`, {
            method: 'PUT',
            body: JSON.stringify({ quantity: newQuantity })
        });

        loadCart();
        updateCartBadge();
    } catch (error) {
        showAlert(error.message || 'Failed to update quantity', 'error');
    }
}

async function removeFromCart(itemId) {
    try {
        await apiRequest(`/api/cart/remove/${itemId}`, {
            method: 'DELETE'
        });

        showAlert('Item removed from cart', 'success');
        loadCart();
        updateCartBadge();
    } catch (error) {
        showAlert(error.message || 'Failed to remove item', 'error');
    }
}

async function clearCart() {
    if (!confirm('Are you sure you want to clear your cart?')) return;

    try {
        await apiRequest('/api/cart/clear', {
            method: 'DELETE'
        });

        showAlert('Cart cleared', 'success');
        loadCart();
        updateCartBadge();
    } catch (error) {
        showAlert(error.message || 'Failed to clear cart', 'error');
    }
}

function proceedToCheckout() {
    window.location.href = 'checkout.html';
}

// ============= Checkout Functions =============

async function loadCheckoutData() {
    const token = getAuthToken();
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    try {
        const cart = await apiRequest('/api/cart/');

        if (!cart.items || cart.items.length === 0) {
            showAlert('Your cart is empty', 'error');
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
            return;
        }

        displayCheckoutSummary(cart);
    } catch (error) {
        showAlert('Error loading checkout data', 'error');
    }
}

function displayCheckoutSummary(cart) {
    const orderItems = document.getElementById('orderItems');
    const subtotal = document.getElementById('subtotal');
    const totalItems = document.getElementById('totalItems');
    const total = document.getElementById('total');

    if (orderItems) {
        orderItems.innerHTML = cart.items.map(item => `
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border-color);">
                <span>${item.product?.name} x${item.quantity}</span>
                <span>$${(item.product?.price * item.quantity).toFixed(2)}</span>
            </div>
        `).join('');
    }

    if (subtotal) subtotal.textContent = `$${cart.total_price.toFixed(2)}`;
    if (totalItems) totalItems.textContent = cart.total_items;
    if (total) total.textContent = `$${cart.total_price.toFixed(2)}`;
}

async function loadUserProfile() {
    const token = getAuthToken();
    if (!token) return;

    try {
        const user = await apiRequest('/api/users/me');

        const fullNameInput = document.getElementById('fullName');
        const phoneInput = document.getElementById('phone');
        const addressInput = document.getElementById('shippingAddress');

        if (fullNameInput && user.full_name) fullNameInput.value = user.full_name;
        if (phoneInput && user.phone) phoneInput.value = user.phone;
        if (addressInput && user.address) addressInput.value = user.address;
    } catch (error) {
        console.error('Error loading user profile:', error);
    }
}

async function placeOrder() {
    const shippingAddress = document.getElementById('shippingAddress').value;
    const paymentMethod = document.getElementById('paymentMethod').value;

    if (!shippingAddress) {
        showAlert('Please enter shipping address', 'error');
        return;
    }

    try {
        const order = await apiRequest('/api/orders/checkout', {
            method: 'POST',
            body: JSON.stringify({
                shipping_address: shippingAddress,
                payment_method: paymentMethod
            })
        });

        showAlert('Order placed successfully!', 'success');
        updateCartBadge();

        setTimeout(() => {
            window.location.href = 'orders.html';
        }, 2000);
    } catch (error) {
        showAlert(error.message || 'Failed to place order', 'error');
    }
}

// ============= Orders Functions =============

async function loadOrders() {
    const token = getAuthToken();
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    showLoading(true);

    try {
        const orders = await apiRequest('/api/orders/');
        displayOrders(orders);
    } catch (error) {
        showAlert('Error loading orders', 'error');
    } finally {
        showLoading(false);
    }
}

function displayOrders(orders) {
    const ordersList = document.getElementById('ordersList');
    const emptyOrders = document.getElementById('emptyOrders');

    if (!ordersList) return;

    if (!orders || orders.length === 0) {
        if (emptyOrders) emptyOrders.classList.remove('hidden');
        ordersList.innerHTML = '';
        return;
    }

    if (emptyOrders) emptyOrders.classList.add('hidden');

    ordersList.innerHTML = orders.map(order => `
        <div class="card" style="margin-bottom: 1.5rem;">
            <div class="card-body">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div>
                        <h3 class="card-title">Order #${order.id}</h3>
                        <p style="color: var(--text-secondary); font-size: 0.875rem;">
                            ${new Date(order.created_at).toLocaleDateString()} at ${new Date(order.created_at).toLocaleTimeString()}
                        </p>
                    </div>
                    <span class="product-category" style="background-color: ${getStatusColor(order.status)};">
                        ${order.status.toUpperCase()}
                    </span>
                </div>
                
                <div style="margin-bottom: 1rem;">
                    <strong>Items:</strong>
                    ${order.items?.map(item => `
                        <div style="margin-left: 1rem; margin-top: 0.5rem;">
                            ${item.product?.name} x${item.quantity} - $${item.price_at_purchase.toFixed(2)} each
                        </div>
                    `).join('') || 'No items'}
                </div>
                
                <div style="margin-bottom: 0.5rem;">
                    <strong>Shipping Address:</strong> ${order.shipping_address}
                </div>
                
                <div style="margin-bottom: 0.5rem;">
                    <strong>Payment Method:</strong> ${order.payment_method || 'N/A'}
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                    <strong style="font-size: 1.25rem;">Total: $${order.total_amount.toFixed(2)}</strong>
                </div>
            </div>
        </div>
    `).join('');
}

function getStatusColor(status) {
    const colors = {
        'pending': '#f59e0b',
        'confirmed': '#3b82f6',
        'processing': '#8b5cf6',
        'shipped': '#06b6d4',
        'delivered': '#10b981',
        'cancelled': '#ef4444'
    };
    return colors[status] || '#6b7280';
}
