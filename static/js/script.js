document.addEventListener('DOMContentLoaded', function () {
    console.log("Ethio Marketing: Logic & Mobile Nav Loaded! 🚀");

    // --- 0. MOBILE MENU TOGGLE (Path 3) ---
    const menuToggle = document.querySelector('#mobile-menu');
    const navList = document.querySelector('#nav-list');

    if (menuToggle && navList) {
        menuToggle.addEventListener('click', function() {
            // Toggles the dropdown menu
            navList.classList.toggle('active');
            // Animates the hamburger bars (if CSS is applied)
            menuToggle.classList.toggle('is-active');
        });
    }

    const cartCountElement = document.getElementById('cart_count');
    const toast = document.getElementById('cart-toast');

    // --- 1. ADD TO CART LOGIC ---
    const cartButtons = document.querySelectorAll('.add-to-cart, .btn-cart-action');

    cartButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const productID = this.value; 
            const productName = this.getAttribute('data-name') || "Product";
            const quantityInput = document.getElementById('qty-input-' + productID);
            const productQty = quantityInput ? quantityInput.value : 1;

            fetch('/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: new URLSearchParams({
                    'product_id': productID,
                    'product_qty': productQty,
                    'action': 'post'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (cartCountElement && data.qty !== undefined) {
                    cartCountElement.innerText = data.qty;
                }
                if(toast) {
                    toast.innerText = productQty + " x " + productName + " added! 🛒";
                    toast.classList.remove('toast-hidden');
                    toast.classList.add('toast-visible');
                    setTimeout(() => {
                        toast.classList.remove('toast-visible');
                        toast.classList.add('toast-hidden');
                    }, 3000);
                }
                
                // Button feedback animation
                const originalText = this.innerText;
                this.innerText = "Added! ✅";
                const originalBg = this.style.backgroundColor;
                this.style.backgroundColor = "#27ae60";
                setTimeout(() => {
                    this.innerText = originalText;
                    this.style.backgroundColor = originalBg;
                }, 1000);
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // --- 2. REMOVE FROM CART LOGIC ---
    const deleteButtons = document.querySelectorAll('.delete-product, .btn-remove-item');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const productID = this.getAttribute('data-index') || this.value;

            fetch('/delete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: new URLSearchParams({
                    'product_id': productID,
                    'action': 'post'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (cartCountElement && data.qty !== undefined) {
                    cartCountElement.innerText = data.qty;
                }
                location.reload(); 
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // --- 3. UPDATE QUANTITY LOGIC ---
    const updateButtons = document.querySelectorAll('.update-cart-btn');

    updateButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const productID = this.getAttribute('data-index');
            const quantity = document.getElementById('select' + productID).value;

            fetch('/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: new URLSearchParams({
                    'product_id': productID,
                    'product_qty': quantity,
                    'action': 'post'
                })
            })
            .then(response => response.json())
            .then(data => {
                location.reload();
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

// --- CSRF HELPER ---
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