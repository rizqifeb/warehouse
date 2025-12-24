from django.contrib import admin
from .models import Category, Supplier, Product, Location, StockMovement, PurchaseOrder, PurchaseOrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    list_filter = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'supplier', 'unit_price', 'current_stock', 'needs_reorder', 'created_at']
    search_fields = ['name', 'sku']
    list_filter = ['category', 'supplier', 'created_at']
    readonly_fields = ['current_stock', 'needs_reorder']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'location', 'movement_type', 'quantity', 'reference', 'created_by', 'created_at']
    search_fields = ['product__name', 'reference']
    list_filter = ['movement_type', 'location', 'created_at']
    readonly_fields = ['created_at']


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'supplier', 'status', 'order_date', 'total_amount', 'created_by', 'created_at']
    search_fields = ['po_number', 'supplier__name']
    list_filter = ['status', 'order_date', 'created_at']
    inlines = [PurchaseOrderItemInline]
    readonly_fields = ['total_amount']
