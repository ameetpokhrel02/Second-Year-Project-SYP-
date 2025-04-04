const addToCartButtons = document.querySelectorAll('.add-to-cart');
        const favoriteButtons = document.querySelectorAll('.favorite');
        const cartCountElement = document.getElementById('cart-count');
        const cartButton = document.getElementById('cart-button');
        const cartModal = document.getElementById('cart-modal');
        const closeModal = document.querySelector('.close');
        const favoriteModal = document.getElementById('favorite-modal');
        const closeFavoriteModal = document.querySelector('.close-favorite');
        const cartItemsList = document.getElementById('cart-items');
        const favoriteItemsList = document.getElementById('favorite-items');
        const themeToggle = document.getElementById('theme-toggle');
        let cartCount = 0;
        let cartItems = [];
        let favoriteItems = [];

        addToCartButtons.forEach(button => {
            button.addEventListener('click', () => {
                const item = button.parentElement;
                const itemName = item.querySelector('h3').textContent;
                const itemPrice = item.querySelector('.price').textContent;
                const itemImage = item.querySelector('img').src;

                cartCount++;
                cartCountElement.textContent = cartCount;

                const existingItem = cartItems.find(cartItem => cartItem.name === itemName);
                if (existingItem) {
                    existingItem.quantity++;
                } else {
                    cartItems.push({ name: itemName, price: itemPrice, image: itemImage, quantity: 1 });
                }
                updateCartItems();
            });
        });

        favoriteButtons.forEach(button => {
            button.addEventListener('click', () => {
                const item = button.parentElement;
                const itemName = item.querySelector('h3').textContent;
                const itemPrice = item.querySelector('.price').textContent;
                const itemImage = item.querySelector('img').src;

                const existingItem = favoriteItems.find(favoriteItem => favoriteItem.name === itemName);
                if (!existingItem) {
                    favoriteItems.push({ name: itemName, price: itemPrice, image: itemImage });
                }
                updateFavoriteItems();
            });
        });

        cartButton.addEventListener('click', () => {
            cartModal.style.display = 'block';
        });

        closeModal.addEventListener('click', () => {
            cartModal.style.display = 'none';
        });

        closeFavoriteModal.addEventListener('click', () => {
            favoriteModal.style.display = 'none';
        });

        window.addEventListener('click', (event) => {
            if (event.target == cartModal) {
                cartModal.style.display = 'none';
            }
            if (event.target == favoriteModal) {
                favoriteModal.style.display = 'none';
            }
        });

        function updateCartItems() {
            cartItemsList.innerHTML = '';
            cartItems.forEach(item => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <img src="${item.image}" alt="${item.name}" style="width: 50px; height: 50px;">
                    ${item.name} - ${item.price} x ${item.quantity}
                    <button class="remove-item" data-name="${item.name}">Remove</button>
                `;
                cartItemsList.appendChild(li);
            });

            const removeButtons = document.querySelectorAll('.remove-item');
            removeButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const itemName = button.getAttribute('data-name');
                    const itemIndex = cartItems.findIndex(cartItem => cartItem.name === itemName);
                    if (itemIndex > -1) {
                        cartCount -= cartItems[itemIndex].quantity;
                        cartItems.splice(itemIndex, 1);
                        cartCountElement.textContent = cartCount;
                        updateCartItems();
                    }
                });
            });
        }

        function updateFavoriteItems() {
            favoriteItemsList.innerHTML = '';
            favoriteItems.forEach(item => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <img src="${item.image}" alt="${item.name}" style="width: 50px; height: 50px;">
                    ${item.name} - ${item.price}
                `;
                favoriteItemsList.appendChild(li);
            });
        }

        // Text animation
        const text = "Tasty the delicious dishes";
        const animatedText = document.getElementById('animated-text');
        let index = 0;

        function typeText() {
            if (index < text.length) {
                animatedText.innerHTML += `<span style="color: ${getRandomColor()};">${text.charAt(index)}</span>`;
                index++;
                setTimeout(typeText, 50); // Reduced delay to make the animation faster
            }
        }

        function getRandomColor() {
            const letters = '0123456789ABCDEF';
            let color = '#';
            for (let i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        }

        typeText();

        // Theme toggle
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            const icon = themeToggle.querySelector('i');
            if (document.body.classList.contains('dark-mode')) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        });
        favoriteButtons.forEach(button => {
            button.addEventListener('click', () => {
                const itemId = button.getAttribute('data-item-id');
                fetch(`/cafe/add_to_favorites/${itemId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const icon = button.querySelector('i');
                        icon.classList.toggle('far');
                        icon.classList.toggle('fas');
                    }
                });
            });
        });
        
        favoriteButtons.forEach(button => {
            button.addEventListener('click', () => {
                const itemId = button.getAttribute('data-item-id');
                fetch(`/cafe/add_to_favorites/${itemId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const icon = button.querySelector('i');
                        icon.classList.toggle('far');
                        icon.classList.toggle('fas');
                    }
                });
            });
        });
        
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
        document.querySelectorAll('.add-to-cart').forEach((button) => {
            button.addEventListener('click', function() {
                const productId = this.closest('.menu-item').dataset.productId;
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
            });
        });

        // Function to update cart count
        function updateCartCount() {
            fetch('/cart/')
                .then(response => response.json())
                .then(data => {
                    document.getElementById("cart-count").textContent = data.cart_count;
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        }

        // Cart modal functionality
        const cartButton = document.getElementById('cart-button');
        const cartModal = document.getElementById('cart-modal');
        const closeModal = document.querySelector('.close');

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

        // Function to load cart items
        function loadCartItems() {
            fetch('/cart/')
                .then(response => response.json())
                .then(data => {
                    const cartItemsList = document.getElementById('cart-items');
                    cartItemsList.innerHTML = '';
                    
                    data.cart_items.forEach(item => {
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <img src="${item.product.image}" alt="${item.product.name}" style="width: 50px; height: 50px;">
                            ${item.product.name} - Rs ${item.product.price} x ${item.quantity}
                            <button class="remove-item" data-id="${item.id}">Remove</button>
                        `;
                        cartItemsList.appendChild(li);
                    });

                    // Add event listeners to remove buttons
                    document.querySelectorAll('.remove-item').forEach(button => {
                        button.addEventListener('click', function() {
                            const itemId = this.dataset.id;
                            removeFromCart(itemId);
                        });
                    });
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        }

        // Function to remove item from cart
        function removeFromCart(itemId) {
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
        }
