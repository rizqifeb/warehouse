#!/usr/bin/env python
"""
Script to create sample data for the warehouse management system
"""
import os
import sys
import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warehouse_system.settings')
django.setup()

from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Product, Location, StockMovement, PurchaseOrder, PurchaseOrderItem

def create_sample_data():
    print("Creating sample data...")
    
    # Create superuser if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✓ Created admin user (username: admin, password: admin123)")
    
    # Create categories
    categories_data = [
        {'name': 'Electronics', 'description': 'Electronic devices and components'},
        {'name': 'Office Supplies', 'description': 'Office equipment and supplies'},
        {'name': 'Tools', 'description': 'Hand tools and equipment'},
        {'name': 'Furniture', 'description': 'Office and warehouse furniture'},
        {'name': 'Safety Equipment', 'description': 'Safety gear and equipment'},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories[cat_data['name']] = category
        if created:
            print(f"✓ Created category: {category.name}")
    
    # Create suppliers
    suppliers_data = [
        {
            'name': 'TechCorp Solutions',
            'contact_person': 'John Smith',
            'email': 'john@techcorp.com',
            'phone': '+1-555-0101',
            'address': '123 Tech Street, Silicon Valley, CA 94000'
        },
        {
            'name': 'Office Plus Inc',
            'contact_person': 'Sarah Johnson',
            'email': 'sarah@officeplus.com',
            'phone': '+1-555-0102',
            'address': '456 Business Ave, New York, NY 10001'
        },
        {
            'name': 'Industrial Tools Ltd',
            'contact_person': 'Mike Wilson',
            'email': 'mike@industrialtools.com',
            'phone': '+1-555-0103',
            'address': '789 Industrial Blvd, Detroit, MI 48201'
        },
        {
            'name': 'Furniture World',
            'contact_person': 'Lisa Brown',
            'email': 'lisa@furnitureworld.com',
            'phone': '+1-555-0104',
            'address': '321 Furniture Row, Atlanta, GA 30301'
        },
    ]
    
    suppliers = {}
    for sup_data in suppliers_data:
        supplier, created = Supplier.objects.get_or_create(
            name=sup_data['name'],
            defaults=sup_data
        )
        suppliers[sup_data['name']] = supplier
        if created:
            print(f"✓ Created supplier: {supplier.name}")
    
    # Create locations
    locations_data = [
        {'name': 'Warehouse A', 'description': 'Main warehouse storage area'},
        {'name': 'Warehouse B', 'description': 'Secondary storage area'},
        {'name': 'Office Storage', 'description': 'Office supply storage'},
        {'name': 'Loading Dock', 'description': 'Receiving and shipping area'},
    ]
    
    locations = {}
    for loc_data in locations_data:
        location, created = Location.objects.get_or_create(
            name=loc_data['name'],
            defaults={'description': loc_data['description']}
        )
        locations[loc_data['name']] = location
        if created:
            print(f"✓ Created location: {location.name}")
    
    # Create products
    products_data = [
        {
            'name': 'Laptop Computer',
            'sku': 'TECH-001',
            'description': 'High-performance business laptop',
            'category': 'Electronics',
            'supplier': 'TechCorp Solutions',
            'unit_price': 899.99,
            'reorder_level': 5
        },
        {
            'name': 'Wireless Mouse',
            'sku': 'TECH-002',
            'description': 'Ergonomic wireless mouse',
            'category': 'Electronics',
            'supplier': 'TechCorp Solutions',
            'unit_price': 29.99,
            'reorder_level': 20
        },
        {
            'name': 'Office Chair',
            'sku': 'FURN-001',
            'description': 'Ergonomic office chair with lumbar support',
            'category': 'Furniture',
            'supplier': 'Furniture World',
            'unit_price': 199.99,
            'reorder_level': 10
        },
        {
            'name': 'Desk Lamp',
            'sku': 'OFF-001',
            'description': 'LED desk lamp with adjustable brightness',
            'category': 'Office Supplies',
            'supplier': 'Office Plus Inc',
            'unit_price': 39.99,
            'reorder_level': 15
        },
        {
            'name': 'Screwdriver Set',
            'sku': 'TOOL-001',
            'description': 'Professional screwdriver set with 12 pieces',
            'category': 'Tools',
            'supplier': 'Industrial Tools Ltd',
            'unit_price': 24.99,
            'reorder_level': 8
        },
        {
            'name': 'Safety Helmet',
            'sku': 'SAFE-001',
            'description': 'Industrial safety helmet',
            'category': 'Safety Equipment',
            'supplier': 'Industrial Tools Ltd',
            'unit_price': 19.99,
            'reorder_level': 25
        },
        {
            'name': 'Printer Paper',
            'sku': 'OFF-002',
            'description': 'A4 printer paper, 500 sheets',
            'category': 'Office Supplies',
            'supplier': 'Office Plus Inc',
            'unit_price': 9.99,
            'reorder_level': 50
        },
        {
            'name': 'Monitor Stand',
            'sku': 'FURN-002',
            'description': 'Adjustable monitor stand',
            'category': 'Furniture',
            'supplier': 'Furniture World',
            'unit_price': 49.99,
            'reorder_level': 12
        },
    ]
    
    products = {}
    admin_user = User.objects.get(username='admin')
    
    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            sku=prod_data['sku'],
            defaults={
                'name': prod_data['name'],
                'description': prod_data['description'],
                'category': categories[prod_data['category']],
                'supplier': suppliers[prod_data['supplier']],
                'unit_price': prod_data['unit_price'],
                'reorder_level': prod_data['reorder_level']
            }
        )
        products[prod_data['sku']] = product
        if created:
            print(f"✓ Created product: {product.name} ({product.sku})")
    
    # Create initial stock movements
    stock_movements_data = [
        {'sku': 'TECH-001', 'quantity': 10, 'location': 'Warehouse A', 'reference': 'INITIAL-001'},
        {'sku': 'TECH-002', 'quantity': 50, 'location': 'Warehouse A', 'reference': 'INITIAL-002'},
        {'sku': 'FURN-001', 'quantity': 15, 'location': 'Warehouse B', 'reference': 'INITIAL-003'},
        {'sku': 'OFF-001', 'quantity': 25, 'location': 'Office Storage', 'reference': 'INITIAL-004'},
        {'sku': 'TOOL-001', 'quantity': 20, 'location': 'Warehouse A', 'reference': 'INITIAL-005'},
        {'sku': 'SAFE-001', 'quantity': 30, 'location': 'Warehouse B', 'reference': 'INITIAL-006'},
        {'sku': 'OFF-002', 'quantity': 100, 'location': 'Office Storage', 'reference': 'INITIAL-007'},
        {'sku': 'FURN-002', 'quantity': 18, 'location': 'Warehouse B', 'reference': 'INITIAL-008'},
    ]
    
    for movement_data in stock_movements_data:
        movement, created = StockMovement.objects.get_or_create(
            product=products[movement_data['sku']],
            reference=movement_data['reference'],
            defaults={
                'location': locations[movement_data['location']],
                'movement_type': 'IN',
                'quantity': movement_data['quantity'],
                'notes': 'Initial stock',
                'created_by': admin_user
            }
        )
        if created:
            print(f"✓ Created stock movement: {movement.product.name} +{movement.quantity}")
    
    # Create some sample purchase orders
    po_data = [
        {
            'po_number': 'PO-2024-001',
            'supplier': 'TechCorp Solutions',
            'order_date': date.today() - timedelta(days=5),
            'expected_delivery': date.today() + timedelta(days=10),
            'status': 'SENT',
            'notes': 'Urgent order for new laptops',
            'items': [
                {'sku': 'TECH-001', 'quantity': 5, 'unit_price': 899.99},
                {'sku': 'TECH-002', 'quantity': 10, 'unit_price': 29.99},
            ]
        },
        {
            'po_number': 'PO-2024-002',
            'supplier': 'Office Plus Inc',
            'order_date': date.today() - timedelta(days=2),
            'expected_delivery': date.today() + timedelta(days=7),
            'status': 'DRAFT',
            'notes': 'Monthly office supplies order',
            'items': [
                {'sku': 'OFF-001', 'quantity': 20, 'unit_price': 39.99},
                {'sku': 'OFF-002', 'quantity': 50, 'unit_price': 9.99},
            ]
        },
    ]
    
    for po in po_data:
        purchase_order, created = PurchaseOrder.objects.get_or_create(
            po_number=po['po_number'],
            defaults={
                'supplier': suppliers[po['supplier']],
                'order_date': po['order_date'],
                'expected_delivery': po['expected_delivery'],
                'status': po['status'],
                'notes': po['notes'],
                'created_by': admin_user
            }
        )
        
        if created:
            print(f"✓ Created purchase order: {purchase_order.po_number}")
            
            # Create purchase order items
            for item_data in po['items']:
                PurchaseOrderItem.objects.create(
                    purchase_order=purchase_order,
                    product=products[item_data['sku']],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price']
                )
                print(f"  ✓ Added item: {products[item_data['sku']].name}")
    
    print("\n🎉 Sample data created successfully!")
    print("\nLogin credentials:")
    print("Username: admin")
    print("Password: admin123")
    print("\nYou can now run 'python manage.py runserver' to start the application.")

if __name__ == '__main__':
    create_sample_data()
