from django.contrib import admin
from .models import POSProduct, Sale, POSCustomer

@admin.register(POSProduct)
class POSProductAdmin(admin.ModelAdmin):
    list_display = ["name", "sku", "category", "price", "cost", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "sku", "category"]

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "customer_name", "total", "discount", "tax", "created_at"]
    list_filter = ["payment_method"]
    search_fields = ["receipt_number", "customer_name", "cashier"]

@admin.register(POSCustomer)
class POSCustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email", "loyalty_points", "total_purchases", "created_at"]
    list_filter = ["tier"]
    search_fields = ["name", "phone", "email"]
