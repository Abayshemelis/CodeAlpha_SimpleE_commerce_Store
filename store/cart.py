from .models import Product
from decimal import Decimal

class Cart:
    def __init__(self, request):
        self.session = request.session
        # Retrieve the existing cart or create a new one
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        
        # If product is already in cart, increment quantity
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += int(quantity)
        else:
            self.cart[product_id] = {
                'price': str(product.price),
                'quantity': int(quantity)
            }
        
        self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Replace old quantity with the new one from the input field
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = product_qty

        self.session.modified = True

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True

    def get_prods(self):
        # Get IDs from the cart keys
        product_ids = self.cart.keys()
        # Fetch products from database
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        # Useful for returning a dictionary of {product_id: quantity}
        return self.cart

    def get_total(self):
        # Calculate the grand total of the cart
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        total = Decimal(0)
        for key, value in self.cart.items():
            qty = value.get('quantity', 0)
            # Find the matching product and add to total
            for product in products:
                if str(product.id) == key:
                    total += (product.price * qty)
        return total

    def __len__(self):
        # Returns total items count (sum of all quantities)
        return sum(item.get('quantity', 0) for item in self.cart.values())

    # --- NEW: Clears the cart after a successful checkout ---
    def clear(self):
        if 'session_key' in self.session:
            del self.session['session_key']
        self.session.modified = True