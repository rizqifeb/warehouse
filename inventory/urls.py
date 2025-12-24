from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    
    # Stock Movements
    path('stock-movement/add/', views.stock_movement_create, name='stock_movement_create'),
    
    # Purchase Orders
    path('purchase-orders/', views.purchase_order_list, name='purchase_order_list'),
    path('purchase-orders/<int:pk>/', views.purchase_order_detail, name='purchase_order_detail'),
    path('purchase-orders/add/', views.purchase_order_create, name='purchase_order_create'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    
    # AJAX endpoints
    path('api/product/<int:pk>/', views.get_product_info, name='get_product_info'),
]
