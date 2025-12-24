# Warehouse Management System

A comprehensive Django-based warehouse information system for managing inventory, products, suppliers, and purchase orders.

## Features

### 📦 Product Management
- Add, edit, and view products with SKU tracking
- Categorize products and assign suppliers
- Set reorder levels and track stock status
- Product search and filtering

### 📊 Inventory Tracking
- Real-time stock level monitoring
- Stock movement recording (IN/OUT/ADJUSTMENT)
- Low stock alerts and notifications
- Location-based inventory tracking

### 🏢 Supplier Management
- Maintain supplier contact information
- Track supplier-product relationships
- Supplier performance monitoring

### 🛒 Purchase Order Management
- Create and manage purchase orders
- Track order status (Draft/Sent/Received/Cancelled)
- Purchase order item management
- Automatic stock updates upon receipt

### 📈 Reports & Analytics
- Stock level reports
- Movement history tracking
- Low stock alerts
- Purchase order summaries

### 👥 User Management
- Role-based access control
- User authentication and authorization
- Activity tracking

## Technology Stack

- **Backend**: Django 6.0
- **Frontend**: Bootstrap 5.1.3, jQuery 3.6.0
- **Database**: SQLite (default, easily configurable for PostgreSQL/MySQL)
- **Icons**: Font Awesome 6.0
- **Styling**: Custom CSS with responsive design

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/rizqifeb/warehouse.git
   cd warehouse
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python manage.py loaddata sample_data.json
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Login with your superuser credentials

## Usage

### Getting Started

1. **Setup Basic Data**
   - Create categories for your products
   - Add suppliers information
   - Set up warehouse locations

2. **Add Products**
   - Navigate to Products → Add Product
   - Fill in product details including SKU, category, and supplier
   - Set reorder levels for automatic low stock alerts

3. **Record Stock Movements**
   - Use Stock → Record Movement to add or remove inventory
   - Track all stock changes with references and notes

4. **Create Purchase Orders**
   - Navigate to Orders → Create Order
   - Add products and quantities
   - Track order status through fulfillment

5. **Monitor Dashboard**
   - View real-time statistics
   - Check low stock alerts
   - Review recent activities

### Key Features

#### Dashboard
- Overview of total products, low stock items, suppliers, and pending orders
- Recent stock movements timeline
- Low stock alerts with quick action buttons
- Quick access to common tasks

#### Product Management
- Comprehensive product catalog with search and filtering
- Stock level monitoring with visual indicators
- Product detail pages with movement history
- Bulk operations support

#### Inventory Control
- Real-time stock tracking
- Movement history with user attribution
- Location-based inventory management
- Automated reorder point notifications

#### Purchase Orders
- Complete purchase order lifecycle management
- Multi-item orders with individual tracking
- Status updates and delivery tracking
- Integration with stock movements

## Configuration

### Database Configuration
The system uses SQLite by default. To use PostgreSQL or MySQL:

1. Install the appropriate database adapter:
   ```bash
   pip install psycopg2-binary  # For PostgreSQL
   # or
   pip install mysqlclient      # For MySQL
   ```

2. Update `warehouse_system/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',  # or mysql
           'NAME': 'warehouse_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',  # or 3306 for MySQL
       }
   }
   ```

### Email Configuration
For email notifications (optional):

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## API Endpoints

The system includes basic API endpoints for integration:

- `GET /api/product/<id>/` - Get product information
- Additional endpoints can be added as needed

## Security Features

- CSRF protection enabled
- User authentication required for all operations
- SQL injection protection through Django ORM
- XSS protection with template escaping

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the code comments for implementation details

## Roadmap

### Planned Features
- [ ] Barcode scanning integration
- [ ] Advanced reporting with charts
- [ ] Email notifications for low stock
- [ ] Multi-warehouse support
- [ ] Mobile app companion
- [ ] Integration with accounting systems
- [ ] Advanced user permissions
- [ ] Audit trail enhancements

### Version History
- **v1.0.0** - Initial release with core functionality
  - Product management
  - Inventory tracking
  - Purchase orders
  - Basic reporting
  - User authentication

## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Product List
![Product List](screenshots/products.png)

### Stock Movement
![Stock Movement](screenshots/stock-movement.png)

*Note: Screenshots will be added once the system is deployed*

---

**Built with ❤️ using Django and Bootstrap**
