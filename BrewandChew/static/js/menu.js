// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Cart functionality
document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    const cartButton = document.getElementById('cart-button');
    const cartModal = document.getElementById('cart-modal');
    const closeModal = document.querySelector('.close');
    const cartItemsContainer = document.getElementById('cart-items');
    const cartCountElement = document.getElementById('cart-count');
    const cartTotalAmount = document.getElementById('cart-total-amount');
    const checkoutButton = document.getElementById('checkout-button');

    // Add to cart functionality
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.closest('.menu-item').dataset.productId;
            addToCart(productId);
        });
    });

    // Cart modal functionality
    cartButton.addEventListener('click', () => {
        cartModal.style.display = 'block';
        loadCartItems();
    });

    closeModal.addEventListener('click', () => {
        cartModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == cartModal) {
            cartModal.style.display = 'none';
        }
    });

    // Function to add item to cart
    function addToCart(productId) {
        fetch(`/add-to-cart/${productId}/`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                updateCartCount();
            } else {
                alert('Error adding item to cart');
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert('Error adding item to cart');
        });
    }

    // Function to load cart items
    function loadCartItems() {
        fetch('/cart/')
            .then(response => response.json())
            .then(data => {
                cartItemsContainer.innerHTML = '';
                let total = 0;
                
                data.cart_items.forEach(item => {
                    total += item.total_price;
                    const itemElement = document.createElement('div');
                    itemElement.className = 'cart-item';
                    itemElement.innerHTML = `
                        <img src="${item.product.image}" alt="${item.product.name}" style="width: 50px; height: 50px;">
                        <div class="cart-item-details">
                            <h4>${item.product.name}</h4>
                            <p>Rs ${item.product.price} x ${item.quantity}</p>
                            <div class="quantity-controls">
                                <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
                                <span>${item.quantity}</span>
                                <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                            </div>
                        </div>
                        <button class="remove-item" onclick="removeFromCart(${item.id})">Remove</button>
                    `;
                    cartItemsContainer.appendChild(itemElement);
                });

                cartTotalAmount.textContent = total.toFixed(2);
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }

    // Function to update cart count
    function updateCartCount() {
        fetch('/get-cart-count/')
            .then(response => response.json())
            .then(data => {
                cartCountElement.textContent = data.cart_count;
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }

    // Function to remove item from cart
    window.removeFromCart = function(itemId) {
        fetch(`/remove-from-cart/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                loadCartItems();
                updateCartCount();
            } else {
                alert('Error removing item from cart');
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert('Error removing item from cart');
        });
    };

    // Function to update quantity
    window.updateQuantity = function(itemId, newQuantity) {
        if (newQuantity < 1) return;

        const formData = new FormData();
        formData.append('quantity', newQuantity);

        fetch(`/update-cart-quantity/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                loadCartItems();
                updateCartCount();
            } else {
                alert('Error updating quantity');
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert('Error updating quantity');
        });
    };

    // Checkout button functionality
    checkoutButton.addEventListener('click', () => {
        // Add your checkout logic here
        alert('Checkout functionality coming soon!');
    });

    // Initial cart count update
    updateCartCount();
}); 