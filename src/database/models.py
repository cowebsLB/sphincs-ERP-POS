"""
Database Models for Sphincs ERP + POS
SQLAlchemy ORM Models
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Time, Text, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class BaseModel(Base):
    """Base model with common fields for sync and versioning"""
    __abstract__ = True
    
    version = Column(Integer, default=1, nullable=False)
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    device_id = Column(String(100), nullable=True)
    user_id = Column(Integer, nullable=True)  # FK to staff who created/modified


# ============================================================================
# STAFF & ROLES
# ============================================================================

class Role(BaseModel):
    """Roles and permissions table"""
    __tablename__ = 'roles'
    
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False, unique=True)  # cashier, kitchen, manager, admin
    permissions = Column(JSON, nullable=True)  # JSON object with permission flags (legacy)
    
    # Relationships
    staff = relationship("Staff", back_populates="role")
    permission_records = relationship("Permission", back_populates="role", cascade="all, delete-orphan")


class Permission(BaseModel):
    """Granular permissions table"""
    __tablename__ = 'permissions'
    
    permission_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)
    permission_name = Column(String(100), nullable=False)  # e.g., 'view_products', 'add_products'
    
    # Relationships
    role = relationship("Role", back_populates="permission_records")


class Staff(BaseModel):
    """Staff/Employees table"""
    __tablename__ = 'staff'
    
    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    hire_date = Column(Date, nullable=False)
    status = Column(String(20), default='active', nullable=False)  # active/inactive
    
    # Relationships
    role = relationship("Role", back_populates="staff")
    orders = relationship("Order", back_populates="staff")
    purchase_orders = relationship("PurchaseOrder", back_populates="staff")
    waste_records = relationship("Waste", back_populates="recorded_by_staff")


# ============================================================================
# PRODUCTS & CATEGORIES
# ============================================================================

class Category(BaseModel):
    """Product categories table"""
    __tablename__ = 'categories'
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)  # Drink, Main, Side, Dessert
    description = Column(Text, nullable=True)
    
    # Relationships
    products = relationship("Product", back_populates="category")


class Product(BaseModel):
    """Products/Menu items table"""
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=True)  # Cost to make this product
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    image_url = Column(String(500), nullable=True)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


# ============================================================================
# INVENTORY & INGREDIENTS
# ============================================================================

class Supplier(BaseModel):
    """Suppliers table"""
    __tablename__ = 'suppliers'
    
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    contact_person = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    status = Column(String(20), default='active', nullable=False)  # active/inactive
    
    # Relationships
    ingredients = relationship("Ingredient", back_populates="supplier")
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")


class Ingredient(BaseModel):
    """Ingredients table"""
    __tablename__ = 'ingredients'
    
    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    unit = Column(String(20), nullable=False)  # kg, liters, pcs, etc.
    cost_per_unit = Column(Float, nullable=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'), nullable=True)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="ingredients")
    inventory = relationship("Inventory", back_populates="ingredient")
    waste_records = relationship("Waste", back_populates="ingredient")
    po_items = relationship("POItem", back_populates="ingredient")


class Inventory(BaseModel):
    """Inventory/Stock table"""
    __tablename__ = 'inventory'
    
    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), nullable=False)
    quantity = Column(Float, nullable=False, default=0.0)
    unit = Column(String(20), nullable=False)
    location = Column(String(100), nullable=True)  # storage area
    reorder_level = Column(Float, nullable=False, default=0.0)
    status = Column(String(20), default='active', nullable=False)  # active/inactive
    
    # Relationships
    ingredient = relationship("Ingredient", back_populates="inventory")


# ============================================================================
# ORDERS & CUSTOMERS
# ============================================================================

class Customer(BaseModel):
    """Customers table"""
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    loyalty_points = Column(Integer, default=0, nullable=False)
    status = Column(String(20), default='active', nullable=False)  # active/inactive
    
    # Relationships
    orders = relationship("Order", back_populates="customer")


class Order(BaseModel):
    """Orders table"""
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=True)  # Optional for walk-ins
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    order_type = Column(String(20), nullable=False)  # dine-in, takeaway, delivery
    table_number = Column(String(20), nullable=True)
    order_status = Column(String(20), default='pending', nullable=False)  # pending, in_kitchen, completed, cancelled
    order_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=True)  # cash, card, digital
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    staff = relationship("Staff", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order")


class OrderItem(BaseModel):
    """Order items table"""
    __tablename__ = 'order_items'
    
    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)  # Price at time of order
    total_price = Column(Float, nullable=False)  # quantity × unit_price
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


# ============================================================================
# DISCOUNTS & PAYMENTS
# ============================================================================

class Discount(BaseModel):
    """Discounts/Promotions table"""
    __tablename__ = 'discounts'
    
    discount_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    type = Column(String(20), nullable=False)  # percentage, fixed
    value = Column(Float, nullable=False)  # Percentage (0-100) or fixed amount
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    applicable_products = Column(JSON, nullable=True)  # List of product_ids or null for all
    is_active = Column(Boolean, default=True, nullable=False)


class Payment(BaseModel):
    """Payments table"""
    __tablename__ = 'payments'
    
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String(20), nullable=False)  # cash, card, digital
    payment_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(20), default='paid', nullable=False)  # paid, refunded, pending
    
    # Relationships
    order = relationship("Order", back_populates="payments")


# ============================================================================
# WASTE & PURCHASE ORDERS
# ============================================================================

class Waste(BaseModel):
    """Waste/Spoilage table"""
    __tablename__ = 'waste'
    
    waste_id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), nullable=False)
    quantity = Column(Float, nullable=False)
    reason = Column(String(100), nullable=True)  # spoilage, overproduction, damaged
    recorded_by = Column(Integer, ForeignKey('staff.staff_id'), nullable=True)
    waste_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    ingredient = relationship("Ingredient", back_populates="waste_records")
    recorded_by_staff = relationship("Staff", back_populates="waste_records")


class PurchaseOrder(BaseModel):
    """Purchase Orders table"""
    __tablename__ = 'purchase_orders'
    
    po_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    order_date = Column(Date, nullable=False)
    expected_delivery = Column(Date, nullable=True)
    status = Column(String(20), default='pending', nullable=False)  # pending, received, cancelled
    
    # Relationships
    supplier = relationship("Supplier", back_populates="purchase_orders")
    staff = relationship("Staff", back_populates="purchase_orders")
    po_items = relationship("POItem", back_populates="purchase_order", cascade="all, delete-orphan")


class POItem(BaseModel):
    """Purchase Order Items table"""
    __tablename__ = 'po_items'
    
    po_item_id = Column(Integer, primary_key=True, autoincrement=True)
    po_id = Column(Integer, ForeignKey('purchase_orders.po_id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="po_items")
    ingredient = relationship("Ingredient", back_populates="po_items")


# ============================================================================
# TABLES / SEATING
# ============================================================================

class Table(BaseModel):
    """Tables/Seating table"""
    __tablename__ = 'tables'
    
    table_id = Column(Integer, primary_key=True, autoincrement=True)
    table_number = Column(String(20), nullable=False, unique=True)
    seats = Column(Integer, nullable=False)
    location = Column(String(100), nullable=True)
    status = Column(String(20), default='available', nullable=False)  # available, occupied


# ============================================================================
# RECIPES
# ============================================================================

class Recipe(BaseModel):
    """Recipe table - Links products to ingredients"""
    __tablename__ = 'recipes'
    
    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), nullable=False)
    quantity_needed = Column(Float, nullable=False)  # Amount needed per unit of product
    unit = Column(String(20), nullable=False)  # Unit of measurement
    
    # Relationships
    product = relationship("Product", backref="recipe_items")
    ingredient = relationship("Ingredient", backref="recipe_usage")


# ============================================================================
# FINANCIAL/ACCOUNTING
# ============================================================================

class Account(BaseModel):
    """Chart of Accounts"""
    __tablename__ = 'accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    account_code = Column(String(20), nullable=False, unique=True)  # e.g., "1000", "2000"
    account_name = Column(String(200), nullable=False)
    account_type = Column(String(50), nullable=False)  # asset, liability, equity, revenue, expense
    parent_account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=True)
    balance = Column(Float, default=0.0, nullable=False)
    currency = Column(String(10), default='USD', nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    parent_account = relationship("Account", remote_side=[account_id], backref="sub_accounts")
    transactions = relationship("Transaction", back_populates="account")


class Transaction(BaseModel):
    """Financial Transactions"""
    __tablename__ = 'transactions'
    
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    transaction_type = Column(String(50), nullable=False)  # debit, credit
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default='USD', nullable=False)
    exchange_rate = Column(Float, default=1.0, nullable=False)  # For multi-currency
    description = Column(Text, nullable=True)
    reference_type = Column(String(50), nullable=True)  # order, expense, invoice, payment
    reference_id = Column(Integer, nullable=True)  # ID of related record
    transaction_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    account = relationship("Account", back_populates="transactions")


class Invoice(BaseModel):
    """Invoices table"""
    __tablename__ = 'invoices'
    
    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_number = Column(String(50), nullable=False, unique=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'), nullable=True)
    invoice_type = Column(String(20), nullable=False)  # sales, purchase
    subtotal = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, nullable=False)
    currency = Column(String(10), default='USD', nullable=False)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)
    status = Column(String(20), default='draft', nullable=False)  # draft, sent, paid, overdue, cancelled
    pdf_path = Column(String(500), nullable=True)  # Path to generated PDF
    notes = Column(Text, nullable=True)
    
    # Relationships
    customer = relationship("Customer", backref="invoices")
    supplier = relationship("Supplier", backref="invoices")


class Expense(BaseModel):
    """Expenses table"""
    __tablename__ = 'expenses'
    
    expense_id = Column(Integer, primary_key=True, autoincrement=True)
    expense_category = Column(String(100), nullable=False)  # utilities, salaries, supplies, rent, etc.
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default='USD', nullable=False)
    expense_date = Column(Date, nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'), nullable=True)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=True)  # For salary expenses
    payment_method = Column(String(50), nullable=True)  # cash, card, bank_transfer
    receipt_path = Column(String(500), nullable=True)  # Path to receipt image/PDF
    is_recurring = Column(Boolean, default=False, nullable=False)
    recurring_frequency = Column(String(20), nullable=True)  # monthly, weekly, yearly
    
    # Relationships
    supplier = relationship("Supplier", backref="expenses")
    staff = relationship("Staff", backref="salary_expenses")


class Tax(BaseModel):
    """Tax configuration and records"""
    __tablename__ = 'taxes'
    
    tax_id = Column(Integer, primary_key=True, autoincrement=True)
    tax_name = Column(String(100), nullable=False)  # VAT, Sales Tax, Service Tax
    tax_rate = Column(Float, nullable=False)  # Percentage (e.g., 10.0 for 10%)
    tax_type = Column(String(20), nullable=False)  # percentage, fixed
    applicable_to = Column(String(50), nullable=True)  # all, products, services, specific_categories
    applicable_categories = Column(JSON, nullable=True)  # List of category_ids if applicable_to is specific
    effective_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


# ============================================================================
# MULTI-LOCATION
# ============================================================================

class Location(BaseModel):
    """Locations/Branches table"""
    __tablename__ = 'locations'
    
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    location_code = Column(String(20), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    manager_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    manager = relationship("Staff", backref="managed_locations")


# ============================================================================
# STAFF PERFORMANCE & HR
# ============================================================================

class Attendance(BaseModel):
    """Staff attendance tracking"""
    __tablename__ = 'attendance'
    
    attendance_id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    attendance_date = Column(Date, nullable=False)
    clock_in = Column(DateTime, nullable=True)
    clock_out = Column(DateTime, nullable=True)
    break_duration = Column(Integer, default=0, nullable=False)  # Minutes
    total_hours = Column(Float, nullable=True)  # Calculated hours worked
    status = Column(String(20), default='present', nullable=False)  # present, absent, late, on_leave
    notes = Column(Text, nullable=True)
    
    # Relationships
    staff = relationship("Staff", backref="attendance_records")


class ShiftSchedule(BaseModel):
    """Staff shift scheduling"""
    __tablename__ = 'shift_schedules'
    
    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    shift_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    break_duration = Column(Integer, default=0, nullable=False)  # Minutes
    shift_type = Column(String(20), nullable=True)  # morning, afternoon, evening, night
    status = Column(String(20), default='scheduled', nullable=False)  # scheduled, confirmed, cancelled, completed
    notes = Column(Text, nullable=True)
    
    # Relationships
    staff = relationship("Staff", backref="shift_schedules")


class Payroll(BaseModel):
    """Payroll records"""
    __tablename__ = 'payroll'
    
    payroll_id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    base_salary = Column(Float, nullable=False)
    hours_worked = Column(Float, nullable=False)
    hourly_rate = Column(Float, nullable=True)
    overtime_hours = Column(Float, default=0.0, nullable=False)
    overtime_rate = Column(Float, nullable=True)
    tips = Column(Float, default=0.0, nullable=False)
    bonuses = Column(Float, default=0.0, nullable=False)
    deductions = Column(Float, default=0.0, nullable=False)  # Tax, insurance, etc.
    gross_pay = Column(Float, nullable=False)
    net_pay = Column(Float, nullable=False)
    currency = Column(String(10), default='USD', nullable=False)
    payment_date = Column(Date, nullable=True)
    status = Column(String(20), default='pending', nullable=False)  # pending, paid, cancelled
    notes = Column(Text, nullable=True)
    
    # Relationships
    staff = relationship("Staff", backref="payroll_records")


# ============================================================================
# CUSTOMER LOYALTY & MARKETING
# ============================================================================

class LoyaltyProgram(BaseModel):
    """Loyalty program configuration"""
    __tablename__ = 'loyalty_programs'
    
    program_id = Column(Integer, primary_key=True, autoincrement=True)
    program_name = Column(String(200), nullable=False)
    points_per_currency = Column(Float, nullable=False)  # e.g., 1 point per $1
    tier_system = Column(JSON, nullable=True)  # Tier definitions with thresholds
    is_active = Column(Boolean, default=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)


class Coupon(BaseModel):
    """Coupons/Promotional codes"""
    __tablename__ = 'coupons'
    
    coupon_id = Column(Integer, primary_key=True, autoincrement=True)
    coupon_code = Column(String(50), nullable=False, unique=True)
    coupon_name = Column(String(200), nullable=False)
    discount_type = Column(String(20), nullable=False)  # percentage, fixed
    discount_value = Column(Float, nullable=False)
    min_purchase_amount = Column(Float, nullable=True)
    max_discount_amount = Column(Float, nullable=True)
    usage_limit = Column(Integer, nullable=True)  # Total usage limit
    usage_count = Column(Integer, default=0, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


class CustomerFeedback(BaseModel):
    """Customer feedback and reviews"""
    __tablename__ = 'customer_feedback'
    
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 stars
    feedback_text = Column(Text, nullable=True)
    sentiment = Column(String(20), nullable=True)  # positive, neutral, negative (calculated)
    feedback_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    customer = relationship("Customer", backref="feedback")
    order = relationship("Order", backref="feedback")


# ============================================================================
# SUPPLIER RATING & PROCUREMENT
# ============================================================================

class SupplierRating(BaseModel):
    """Supplier performance rating"""
    __tablename__ = 'supplier_ratings'
    
    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'), nullable=False)
    purchase_order_id = Column(Integer, ForeignKey('purchase_orders.po_id'), nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    on_time_delivery = Column(Boolean, nullable=True)
    quality_rating = Column(Integer, nullable=True)  # 1-5
    price_rating = Column(Integer, nullable=True)  # 1-5
    communication_rating = Column(Integer, nullable=True)  # 1-5
    notes = Column(Text, nullable=True)
    rating_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    supplier = relationship("Supplier", backref="ratings")
    purchase_order = relationship("PurchaseOrder", backref="ratings")


# ============================================================================
# SECURITY & AUDIT
# ============================================================================

class AuditLog(BaseModel):
    """Audit trail for all system changes"""
    __tablename__ = 'audit_logs'
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=True)
    action = Column(String(100), nullable=False)  # create, update, delete, login, logout
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=True)
    old_values = Column(JSON, nullable=True)  # Previous values
    new_values = Column(JSON, nullable=True)  # New values
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    staff = relationship("Staff", backref="audit_logs")


# ============================================================================
# INVENTORY ENHANCEMENTS
# ============================================================================

class InventoryExpiry(BaseModel):
    """Inventory expiry tracking"""
    __tablename__ = 'inventory_expiry'
    
    expiry_id = Column(Integer, primary_key=True, autoincrement=True)
    inventory_id = Column(Integer, ForeignKey('inventory.inventory_id'), nullable=False)
    batch_number = Column(String(100), nullable=True)
    expiry_date = Column(Date, nullable=False)
    quantity = Column(Float, nullable=False)
    alert_days_before = Column(Integer, default=7, nullable=False)  # Alert X days before expiry
    is_expired = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    inventory = relationship("Inventory", backref="expiry_records")


class Barcode(BaseModel):
    """Barcode/RFID tracking"""
    __tablename__ = 'barcodes'
    
    barcode_id = Column(Integer, primary_key=True, autoincrement=True)
    barcode_value = Column(String(200), nullable=False, unique=True)
    barcode_type = Column(String(20), nullable=False)  # EAN13, UPC, QR, RFID
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    product = relationship("Product", backref="barcodes")
    ingredient = relationship("Ingredient", backref="barcodes")


# ============================================================================
# NOTIFICATIONS & ALERTS
# ============================================================================


class Notification(BaseModel):
    """Centralized notifications emitted by background monitors and modules"""
    __tablename__ = 'notifications'
    
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    module = Column(String(100), nullable=False)  # inventory, operations, sales, finance, system
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default='info', nullable=False)  # info, warning, critical
    source_type = Column(String(100), nullable=True)  # model/table name
    source_id = Column(Integer, nullable=True)  # related record id
    payload = Column(JSON, nullable=True)  # extra metadata
    is_read = Column(Boolean, default=False, nullable=False)
    read_at = Column(DateTime, nullable=True)
    triggered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    notified_user_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=True)
    
    # Relationships
    notified_user = relationship("Staff", backref="notifications")


class NotificationPreference(BaseModel):
    """User-level notification preferences"""
    __tablename__ = 'notification_preferences'
    __table_args__ = (
        UniqueConstraint('staff_id', 'channel', name='uq_notification_pref_channel'),
    )
    
    preference_id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    channel = Column(String(100), nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    severity_threshold = Column(String(20), default='info', nullable=False)
    desktop_enabled = Column(Boolean, default=True, nullable=False)
    mobile_enabled = Column(Boolean, default=True, nullable=False)
    snoozed_until = Column(DateTime, nullable=True)
    
    staff = relationship("Staff", backref="notification_preferences")


# ============================================================================
# ADVANCED OPERATIONS MODULES
# ============================================================================


class Reservation(BaseModel):
    """Customer reservations & waitlist management"""
    __tablename__ = 'reservations'
    
    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(200), nullable=False)
    contact_info = Column(String(200), nullable=True)
    reservation_datetime = Column(DateTime, nullable=False)
    party_size = Column(Integer, nullable=False, default=2)
    table_id = Column(Integer, ForeignKey('tables.table_id'), nullable=True)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'), nullable=True)
    status = Column(String(20), default='pending', nullable=False)  # pending, confirmed, seated, completed, cancelled
    channel = Column(String(50), nullable=True)  # phone, web, walk-in
    special_requests = Column(Text, nullable=True)
    reminder_sent = Column(Boolean, default=False, nullable=False)
    
    table = relationship("Table", backref="reservations")
    staff = relationship("Staff", backref="reservations")
    location = relationship("Location", backref="reservations")


class VendorContract(BaseModel):
    """Supplier contracts and SLA tracking"""
    __tablename__ = 'vendor_contracts'
    
    contract_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'), nullable=False)
    contract_title = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    renewal_date = Column(Date, nullable=True)
    auto_renew = Column(Boolean, default=False, nullable=False)
    contract_value = Column(Float, nullable=True)
    sla_terms = Column(Text, nullable=True)
    penalty_terms = Column(Text, nullable=True)
    status = Column(String(20), default='active', nullable=False)  # active, expiring, expired, terminated
    
    supplier = relationship("Supplier", backref="contracts")


class TrainingModule(BaseModel):
    """Staff training modules"""
    __tablename__ = 'training_modules'
    
    module_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    duration_hours = Column(Float, nullable=True)
    is_required = Column(Boolean, default=False, nullable=False)
    attachment_path = Column(String(500), nullable=True)


class TrainingAssignment(BaseModel):
    """Training assignments for staff"""
    __tablename__ = 'training_assignments'
    
    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey('training_modules.module_id'), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    assigned_date = Column(Date, default=datetime.utcnow, nullable=False)
    due_date = Column(Date, nullable=True)
    completion_date = Column(Date, nullable=True)
    score = Column(Float, nullable=True)
    status = Column(String(20), default='assigned', nullable=False)  # assigned, in_progress, completed, overdue
    
    module = relationship("TrainingModule", backref="assignments")
    staff = relationship("Staff", backref="training_assignments")


class Certification(BaseModel):
    """Staff certifications & renewals"""
    __tablename__ = 'certifications'
    
    certification_id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    certification_name = Column(String(200), nullable=False)
    provider = Column(String(200), nullable=True)
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    status = Column(String(20), default='active', nullable=False)  # active, expired, revoked
    certificate_path = Column(String(500), nullable=True)
    
    staff = relationship("Staff", backref="certifications")


class QualityAudit(BaseModel):
    """Quality & compliance audits"""
    __tablename__ = 'quality_audits'
    
    audit_id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'), nullable=True)
    auditor_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=True)
    audit_date = Column(Date, nullable=False)
    area = Column(String(100), nullable=False)  # kitchen, dining, storage, etc.
    score = Column(Integer, nullable=True)
    findings = Column(Text, nullable=True)
    corrective_actions = Column(Text, nullable=True)
    follow_up_date = Column(Date, nullable=True)
    status = Column(String(20), default='open', nullable=False)  # open, in_progress, closed
    
    location = relationship("Location", backref="quality_audits")
    auditor = relationship("Staff", backref="quality_audits")


class MaintenanceAsset(BaseModel):
    """Assets/equipment tracking"""
    __tablename__ = 'maintenance_assets'
    
    asset_id = Column(Integer, primary_key=True, autoincrement=True)
    asset_name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=True)
    serial_number = Column(String(100), nullable=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'), nullable=True)
    purchase_date = Column(Date, nullable=True)
    warranty_expiry = Column(Date, nullable=True)
    status = Column(String(20), default='active', nullable=False)  # active, maintenance, retired
    
    location = relationship("Location", backref="assets")


class MaintenanceTask(BaseModel):
    """Maintenance tasks and work orders"""
    __tablename__ = 'maintenance_tasks'
    
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey('maintenance_assets.asset_id'), nullable=True)
    description = Column(Text, nullable=False)
    priority = Column(String(20), default='medium', nullable=False)  # low, medium, high
    assigned_to = Column(Integer, ForeignKey('staff.staff_id'), nullable=True)
    scheduled_date = Column(Date, nullable=True)
    completed_date = Column(Date, nullable=True)
    cost = Column(Float, nullable=True)
    status = Column(String(20), default='open', nullable=False)  # open, in_progress, completed, cancelled
    
    asset = relationship("MaintenanceAsset", backref="tasks")
    assignee = relationship("Staff", backref="maintenance_tasks")


class DeliveryVehicle(BaseModel):
    """Delivery fleet vehicles"""
    __tablename__ = 'delivery_vehicles'
    
    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    license_plate = Column(String(50), nullable=True)
    capacity = Column(String(50), nullable=True)
    status = Column(String(20), default='available', nullable=False)  # available, in_use, maintenance
    last_serviced_date = Column(Date, nullable=True)


class DeliveryAssignment(BaseModel):
    """Delivery routing & assignments"""
    __tablename__ = 'delivery_assignments'
    
    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=True)
    driver_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=True)
    vehicle_id = Column(Integer, ForeignKey('delivery_vehicles.vehicle_id'), nullable=True)
    assigned_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    departure_time = Column(DateTime, nullable=True)
    delivery_time = Column(DateTime, nullable=True)
    route_notes = Column(Text, nullable=True)
    status = Column(String(20), default='assigned', nullable=False)  # assigned, in_transit, delivered, failed, cancelled
    
    order = relationship("Order", backref="delivery_assignment")
    driver = relationship("Staff", backref="delivery_assignments")
    vehicle = relationship("DeliveryVehicle", backref="assignments")


class MenuEngineeringInsight(BaseModel):
    """Menu engineering analysis"""
    __tablename__ = 'menu_engineering'
    
    insight_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    popularity_index = Column(Float, nullable=True)
    profitability_index = Column(Float, nullable=True)
    menu_class = Column(String(50), nullable=True)  # star, plow horse, puzzle, dog
    recommendation = Column(Text, nullable=True)
    analysis_date = Column(Date, default=datetime.utcnow, nullable=False)
    
    product = relationship("Product", backref="menu_insights")


class EventBooking(BaseModel):
    """Event & catering bookings"""
    __tablename__ = 'event_bookings'
    
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(200), nullable=False)
    contact_info = Column(String(200), nullable=True)
    event_type = Column(String(100), nullable=True)
    event_date = Column(DateTime, nullable=False)
    location_id = Column(Integer, ForeignKey('locations.location_id'), nullable=True)
    guest_count = Column(Integer, nullable=True)
    budget = Column(Float, nullable=True)
    status = Column(String(20), default='inquiry', nullable=False)  # inquiry, confirmed, planning, completed, cancelled
    requirements = Column(Text, nullable=True)
    
    location = relationship("Location", backref="event_bookings")


class EventStaffAssignment(BaseModel):
    """Staff assignments for events"""
    __tablename__ = 'event_staff_assignments'
    
    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event_bookings.event_id'), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    role = Column(String(100), nullable=True)
    hours_committed = Column(Float, nullable=True)
    
    event = relationship("EventBooking", backref="staff_assignments")
    staff = relationship("Staff", backref="event_assignments")


class SafetyIncident(BaseModel):
    """Health & safety incidents"""
    __tablename__ = 'safety_incidents'
    
    incident_id = Column(Integer, primary_key=True, autoincrement=True)
    incident_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    location_id = Column(Integer, ForeignKey('locations.location_id'), nullable=True)
    reported_by = Column(Integer, ForeignKey('staff.staff_id'), nullable=True)
    severity = Column(String(20), default='minor', nullable=False)  # minor, moderate, major, critical
    category = Column(String(100), nullable=True)  # injury, hazard, compliance, contamination
    description = Column(Text, nullable=False)
    injuries_reported = Column(Boolean, default=False, nullable=False)
    action_taken = Column(Text, nullable=True)
    follow_up_date = Column(Date, nullable=True)
    status = Column(String(20), default='open', nullable=False)  # open, investigating, resolved, closed
    
    location = relationship("Location", backref="safety_incidents")
    reporter = relationship("Staff", backref="reported_incidents")
