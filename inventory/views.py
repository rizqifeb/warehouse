from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Product, Category, Supplier, StockMovement, Location, PurchaseOrder, PurchaseOrderItem
from .forms import ProductForm, StockMovementForm, PurchaseOrderForm, PurchaseOrderItemFormSet
import json


@login_required
def dashboard(request):
    """Main dashboard view"""
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(
        id__in=[p.id for p in Product.objects.all() if p.needs_reorder]
    ).count()
    total_suppliers = Supplier.objects.count()
    pending_orders = PurchaseOrder.objects.filter(status__in=['DRAFT', 'SENT']).count()
    
    # Recent stock movements
    recent_movements = StockMovement.objects.select_related('product', 'location', 'created_by')[:10]
    
    # Low stock products
    low_stock_items = [p for p in Product.objects.all() if p.needs_reorder][:10]
    
    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'total_suppliers': total_suppliers,
        'pending_orders': pending_orders,
        'recent_movements': recent_movements,
        'low_stock_items': low_stock_items,
    }
    return render(request, 'inventory/dashboard.html', context)


@login_required
def product_list(request):
    """List all products with search and filter"""
    products = Product.objects.select_related('category', 'supplier').all()
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Filter by supplier
    supplier_id = request.GET.get('supplier', '')
    if supplier_id:
        products = products.filter(supplier_id=supplier_id)
    
    # Filter low stock
    low_stock = request.GET.get('low_stock', '')
    if low_stock:
        low_stock_ids = [p.id for p in products if p.needs_reorder]
        products = products.filter(id__in=low_stock_ids)
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'suppliers': Supplier.objects.all(),
        'search_query': search_query,
        'selected_category': category_id,
        'selected_supplier': supplier_id,
        'low_stock_filter': low_stock,
    }
    return render(request, 'inventory/product_list.html', context)


@login_required
def product_detail(request, pk):
    """Product detail view with stock movements"""
    product = get_object_or_404(Product, pk=pk)
    stock_movements = product.stock_movements.select_related('location', 'created_by').all()[:20]
    
    context = {
        'product': product,
        'stock_movements': stock_movements,
    }
    return render(request, 'inventory/product_detail.html', context)


@login_required
def product_create(request):
    """Create new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def product_edit(request, pk):
    """Edit existing product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Edit Product'})


@login_required
def stock_movement_create(request):
    """Create stock movement"""
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.created_by = request.user
            
            # Adjust quantity based on movement type
            if movement.movement_type == 'OUT':
                movement.quantity = -abs(movement.quantity)
            elif movement.movement_type == 'IN':
                movement.quantity = abs(movement.quantity)
            
            movement.save()
            messages.success(request, 'Stock movement recorded successfully!')
            return redirect('product_detail', pk=movement.product.pk)
    else:
        form = StockMovementForm()
        # Pre-fill product if provided
        product_id = request.GET.get('product')
        if product_id:
            form.fields['product'].initial = product_id
    
    return render(request, 'inventory/stock_movement_form.html', {'form': form})


@login_required
def purchase_order_list(request):
    """List purchase orders"""
    orders = PurchaseOrder.objects.select_related('supplier', 'created_by').all()
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        orders = orders.filter(status=status)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            Q(po_number__icontains=search_query) |
            Q(supplier__name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': PurchaseOrder.STATUS_CHOICES,
        'selected_status': status,
        'search_query': search_query,
    }
    return render(request, 'inventory/purchase_order_list.html', context)


@login_required
def purchase_order_detail(request, pk):
    """Purchase order detail view"""
    order = get_object_or_404(PurchaseOrder, pk=pk)
    items = order.items.select_related('product').all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'inventory/purchase_order_detail.html', context)


@login_required
def purchase_order_create(request):
    """Create purchase order"""
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        formset = PurchaseOrderItemFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            
            formset.instance = order
            formset.save()
            
            messages.success(request, 'Purchase order created successfully!')
            return redirect('purchase_order_detail', pk=order.pk)
    else:
        form = PurchaseOrderForm()
        formset = PurchaseOrderItemFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Create Purchase Order'
    }
    return render(request, 'inventory/purchase_order_form.html', context)


@login_required
def reports(request):
    """Reports view"""
    # Stock summary
    products_with_stock = []
    for product in Product.objects.all():
        products_with_stock.append({
            'product': product,
            'current_stock': product.current_stock,
            'needs_reorder': product.needs_reorder
        })
    
    # Stock movements summary
    movements_summary = StockMovement.objects.values('movement_type').annotate(
        total_quantity=Sum('quantity')
    )
    
    context = {
        'products_with_stock': products_with_stock,
        'movements_summary': movements_summary,
    }
    return render(request, 'inventory/reports.html', context)


@login_required
def get_product_info(request, pk):
    """AJAX endpoint to get product information"""
    try:
        product = Product.objects.get(pk=pk)
        data = {
            'name': product.name,
            'sku': product.sku,
            'unit_price': str(product.unit_price),
            'current_stock': product.current_stock,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
