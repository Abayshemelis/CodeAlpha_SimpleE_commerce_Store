from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal

# --- 1. Category Model ---
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

# --- 2. Product Model ---
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products', 
        null=True, 
        blank=True
    )
    description = models.TextField()
    # Added default=0.00 to prevent NoneType errors
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/images/placeholder.png'

# --- 3. Contact Message Model ---
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    
    class Meta:
        ordering = ['-created_at'] 

# --- 4. Order System ---
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=1000)
    shipping_city = models.CharField(max_length=100, default="Hawassa")
    
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order #{self.id} - {self.full_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    @property
    def total_price(self):
        """
        Calculates the subtotal for this item. 
        Safety check: If price is None, it defaults to 0 to prevent crashes.
        """
        safe_price = self.price if self.price is not None else Decimal('0.00')
        return safe_price * self.quantity