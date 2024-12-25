from django.contrib import admin
from .models import Catagory, Product, Cart, Order

# Register other models in the admin site
admin.site.register(Catagory)
admin.site.register(Product)

# Define a custom admin class for Cart
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')  # Fields to display in the admin list view

# Register the Cart model with the custom CartAdmin
admin.site.register(Cart, CartAdmin)

# Define a custom admin class for Order
class OrderAdmin(admin.ModelAdmin):
    # Method to get ordered products
    def get_ordered_products(self, obj):
        ordered_products = []
        
        # Ensure that Cart and Order have a correct relationship
        if hasattr(obj, 'cart_items') and obj.cart_items.exists():
            for cart_item in obj.cart_items.all():
                ordered_products.append(f"{cart_item.product.name} (Quantity: {cart_item.quantity})")
            return ", ".join(ordered_products)
        return "No Products"

    get_ordered_products.short_description = 'Ordered Products'

    fieldsets = [
        ('Order Details', {'fields': ['user', 'address', 'payment_method', 'total_price']}), 
        ('Status', {'fields': ['status']}), 
    ]
    list_display = ('user', 'ordered_at', 'total_price', 'status', 'address', 'get_ordered_products')  # Add get_ordered_products to list_display
    list_filter = ('status', 'ordered_at')

# Register the Order model with the custom OrderAdmin
admin.site.register(Order, OrderAdmin)
