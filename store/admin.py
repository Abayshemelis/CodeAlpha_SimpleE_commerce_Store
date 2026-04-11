from django.contrib import admin
from .models import Category, Product, ContactMessage, Order, OrderItem

# --- 1. Category Admin ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} 

# --- 2. Product Admin ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Added 'is_active' so you can hide products easily
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at'] 
    list_editable = ['price', 'stock', 'is_active'] # Edit price and stock without clicking into the product
    search_fields = ['name', 'description']

# --- 3. Contact Message Admin ---
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'message']
    # Making these readonly ensures you don't accidentally edit a customer's message
    readonly_fields = ['name', 'email', 'message', 'created_at']

# --- 4. Order System (Advanced Inline) ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 
    readonly_fields = ['product', 'quantity', 'price', 'total_price']
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Updated to show the new 'status' instead of just 'shipped'
    list_display = ['id', 'full_name', 'amount_paid', 'status', 'date_ordered']
    list_filter = ['status', 'date_ordered', 'shipping_city']
    search_fields = ['full_name', 'email', 'shipping_address']
    list_editable = ['status'] # Change order status (Pending/Shipped/etc) directly from the list
    inlines = [OrderItemInline]
    
    fieldsets = [
        ('Customer Information', {
            'fields': ['user', 'full_name', 'email', 'shipping_address', 'shipping_city']
        }),
        ('Financial Info', {
            'fields': ['amount_paid', 'date_ordered']
        }),
        ('Order Tracking', {
            'fields': ['status', 'date_shipped']
        }),
    ]
    readonly_fields = ['date_ordered']

# Note: OrderItem is handled inside OrderAdmin via Inlines, 
# but we register it here just in case you want to search items specifically.
admin.site.register(OrderItem)