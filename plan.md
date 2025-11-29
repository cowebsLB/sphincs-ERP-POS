# Main Idea

An **ERP** and **POS** connected to the same local database and cloud database.

- Using **SQLite DB** for local storage first.
- At the end of the day, the data gets pushed to the ERP for reviewing.

---

## Sphincs ERP

### Sections

#### 1. Staff Management

##### a. Staff Table (Unified)

Comprehensive staff database covering all employee types across all departments.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| staff_id        | Primary Key (PK)                               |
| employee_id     | Unique employee identifier/code                |
| first_name      |                                                |
| last_name       |                                                |
| date_of_birth   |                                                |
| gender          | Optional (for reporting)                       |
| email           |                                                |
| phone_number    |                                                |
| address         |                                                |
| emergency_contact| Name and phone of emergency contact            |
| hire_date       | Date of employment start                       |
| termination_date| Date of employment end (NULL if active)        |
| department      | kitchen, floor, cleaning, management, security, delivery, cashier |
| position        | Specific role within department                |
| employment_type | full_time, part_time, contract, temporary      |
| hourly_rate     | For payroll calculations                       |
| status          | active, on_leave, terminated, suspended        |
| notes           | Additional information                         |
| version         | Row version for sync conflict detection        |
| last_modified   | Timestamp of last modification                 |
| created_at      | Record creation timestamp                       |
| device_id       | POS terminal ID (optional for master data)     |
| user_id         | User who created/modified (FK to users table)  |

**Department Types**:

- **Kitchen**: Chef, Sous Chef, Line Cook, Prep Cook, Dishwasher
- **Floor**: Waiter, Server, Host/Hostess, Bartender, Barista, Busser
- **Cleaning**: Janitor, Cleaner, Maintenance Staff
- **Management**: Manager, Supervisor, Assistant Manager, General Manager
- **Cashier**: Cashier, POS Operator, Front Desk
- **Security**: Security Guard, Door Staff
- **Delivery**: Delivery Driver, Delivery Coordinator

##### b. Staff Schedule Table

Tracks work schedules and shifts for all staff members.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| schedule_id     | Primary Key (PK)                               |
| staff_id        | Foreign Key (FK)                               |
| shift_date      | Date of the shift                              |
| shift_start     | Start time of shift                            |
| shift_end       | End time of shift                              |
| break_duration  | Break time in minutes                          |
| department      | Department for this shift                      |
| status          | scheduled, confirmed, completed, cancelled, no_show |
| notes           | Shift-specific notes                           |
| version         | Row version for sync conflict detection        |
| last_modified   | Timestamp of last modification                 |
| created_at      | Record creation timestamp                       |
| device_id       | POS terminal ID                                |
| user_id         | User who created/modified (FK to users table)  |

##### c. Staff Attendance Table

Tracks clock-in/clock-out times and attendance records.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| attendance_id   | Primary Key (PK)                               |
| staff_id        | Foreign Key (FK)                               |
| schedule_id     | Foreign Key (FK) - links to scheduled shift    |
| clock_in        | Clock-in timestamp                             |
| clock_out       | Clock-out timestamp                            |
| break_start     | Break start time                               |
| break_end       | Break end time                                 |
| hours_worked    | Calculated hours (including breaks)            |
| overtime_hours  | Overtime hours if applicable                   |
| status          | present, absent, late, early_leave, sick, on_leave |
| notes           | Attendance notes                               |
| version         | Row version for sync conflict detection        |
| last_modified   | Timestamp of last modification                 |
| created_at      | Record creation timestamp                       |
| device_id       | POS terminal ID                                |
| user_id         | User who created/modified (FK to users table)  |

##### d. Staff Tasks Table

Tracks tasks assigned to staff members (especially for cleaning and maintenance).

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| task_id         | Primary Key (PK)                               |
| staff_id        | Foreign Key (FK)                               |
| task_type       | cleaning, maintenance, inspection, restocking, other |
| task_name       | Name/description of task                       |
| assigned_date   | Date task was assigned                         |
| due_date        | Deadline for task completion                   |
| completed_date  | Date task was completed                        |
| status          | pending, in_progress, completed, cancelled     |
| priority        | low, medium, high, urgent                      |
| notes           | Task details and notes                         |
| version         | Row version for sync conflict detection        |
| last_modified   | Timestamp of last modification                 |
| created_at      | Record creation timestamp                       |
| device_id       | POS terminal ID                                |
| user_id         | User who created/modified (FK to users table)  |

##### e. Staff Performance Table

Tracks performance metrics, reviews, and evaluations.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| performance_id  | Primary Key (PK)                               |
| staff_id        | Foreign Key (FK)                               |
| review_date     | Date of performance review                     |
| review_type     | daily, weekly, monthly, quarterly, annual      |
| rating          | Numerical rating (1-10 or 1-5)                |
| sales_performance| For sales staff - sales metrics                |
| customer_feedback| Customer ratings/comments                      |
| punctuality     | Attendance/punctuality score                   |
| notes           | Review notes and comments                      |
| reviewed_by     | FK to staff_id (manager who conducted review)  |
| version         | Row version for sync conflict detection        |
| last_modified   | Timestamp of last modification                 |
| created_at      | Record creation timestamp                       |
| device_id       | POS terminal ID                                |
| user_id         | User who created/modified (FK to users table)  |

##### f. Floor Staff Assignments Table

Tracks table/station assignments for floor staff (waiters, servers).

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| assignment_id   | Primary Key (PK)                               |
| staff_id        | Foreign Key (FK) - floor staff member          |
| table_number    | Table or station assigned                      |
| shift_date      | Date of assignment                             |
| shift_start     | Start time                                     |
| shift_end       | End time                                       |
| status          | assigned, active, completed                    |
| version         | Row version for sync conflict detection        |
| last_modified   | Timestamp of last modification                 |
| created_at      | Record creation timestamp                       |
| device_id       | POS terminal ID                                |
| user_id         | User who created/modified (FK to users table)  |

##### g. Cleaning Log Table

Tracks cleaning activities and maintenance tasks.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| log_id          | Primary Key (PK)                               |
| staff_id        | Foreign Key (FK) - cleaner/maintenance staff   |
| area            | Area cleaned (dining, kitchen, restroom, storage, etc.) |
| task_type       | sweeping, mopping, sanitizing, deep_clean, maintenance |
| start_time      | When cleaning started                          |
| end_time        | When cleaning completed                        |
| status          | completed, in_progress, scheduled              |
| notes           | Cleaning notes and observations                |
| version         | Row version for sync conflict detection        |
| last_modified   | Timestamp of last modification                 |
| created_at      | Record creation timestamp                       |
| device_id       | POS terminal ID                                |
| user_id         | User who created/modified (FK to users table)  |

---

#### 2. Kitchen Operations

##### a. Ingredients Table  

Tracks every raw ingredient used in the kitchen. Useful for inventory, recipes, and linking to waste/produce.

| Field         | Description                                    |
|---------------|------------------------------------------------|
| ingredient_id | Primary Key (PK)                               |
| name          |                                                |
| unit          | kg, liters, pcs, etc.                          |
| current_stock |                                                |
| reorder_level |                                                |
| supplier_id   | Foreign Key (FK) if you have suppliers table   |
| version       | Row version for sync conflict detection        |
| last_modified | Timestamp of last modification                 |
| created_at    | Record creation timestamp                       |
| device_id     | POS terminal ID (optional for master data)     |
| user_id       | User who created/modified (FK to users table)  |

##### b. Waste Table  

Tracks ingredients or products that got wasted—super important for cost tracking.

| Field         | Description                                    |
|---------------|------------------------------------------------|
| waste_id      | Primary Key (PK)                               |
| ingredient_id | Foreign Key (FK)                               |
| quantity      |                                                |
| reason        | spoiled, overcooked, etc.                      |
| date          |                                                |
| staff_id      | FK, optional (who logged it)                   |
| version       | Row version for sync conflict detection        |
| last_modified | Timestamp of last modification                 |
| created_at    | Record creation timestamp                       |
| device_id     | POS terminal ID (for multi-device sync)        |
| user_id       | User who created/modified (FK to users table)  |

##### c. Products Table  

Finished dishes or items sold via POS.

| Field         | Description                                        |
|---------------|----------------------------------------------------|
| product_id    | Primary Key (PK)                                   |
| name          |                                                    |
| category      | main dish, side, drink, etc.                       |
| price         |                                                    |
| recipe_id     | FK linking to ingredients via a recipe table       |
| version       | Row version for sync conflict detection            |
| last_modified | Timestamp of last modification                     |
| created_at    | Record creation timestamp                           |
| device_id     | POS terminal ID (optional for master data)         |
| user_id       | User who created/modified (FK to users table)      |

##### d. Produce Delivery Table  

Tracks incoming deliveries from suppliers.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| delivery_id     | Primary Key (PK)                               |
| supplier_id     | Foreign Key (FK)                               |
| ingredient_id   | Foreign Key (FK)                               |
| quantity        |                                                |
| delivery_date   |                                                |
| expiration_date |                                                |
| version         | Row version for sync conflict detection        |
| last_modified   | Timestamp of last modification                 |
| created_at      | Record creation timestamp                       |
| device_id       | POS terminal ID (for multi-device sync)        |
| user_id         | User who created/modified (FK to users table)  |

##### f. Kitchen Orders Table  

Tracks live orders in the kitchen for preparation. Links to POS sales and staff (both kitchen and floor staff).

| Field         | Description                                    |
|---------------|------------------------------------------------|
| order_id      | Primary Key (PK)                               |
| product_id    | Foreign Key (FK)                               |
| staff_id      | Foreign Key (FK, chef/prep)                    |
| floor_staff_id| Foreign Key (FK) - waiter/server who took order|
| table_number  | Table number (if applicable)                   |
| status        | pending, cooking, ready, served                |
| quantity      |                                                |
| timestamp     |                                                |
| version       | Row version for sync conflict detection        |
| last_modified | Timestamp of last modification                 |
| created_at    | Record creation timestamp                       |
| device_id     | POS terminal ID (for multi-device sync)        |
| user_id       | User who created/modified (FK to users table)  |

##### e. Suppliers Table  

Tracks vendors, contacts, and notes.

| Field        | Description                                    |
|--------------|------------------------------------------------|
| supplier_id  | Primary Key (PK)                               |
| name         |                                                |
| contact_info |                                                |
| address      |                                                |
| notes        |                                                |
| version      | Row version for sync conflict detection        |
| last_modified| Timestamp of last modification                 |
| created_at   | Record creation timestamp                       |
| device_id    | POS terminal ID (optional for master data)     |
| user_id      | User who created/modified (FK to users table)  |

---

## Sphincs POS

### Sections

#### 1. Sales Tables

##### a. Sales Transactions Table

Main table for all POS transactions.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| transaction_id  | Primary Key (PK)                               |
| receipt_number  | Unique receipt identifier                      |
| customer_id     | Foreign Key (FK), optional (for loyalty)       |
| staff_id        | Foreign Key (FK) - cashier/server/waiter       |
| floor_staff_id  | Foreign Key (FK) - waiter/server (if different from cashier) |
| table_number    | Table number (for dine-in orders)              |
| total_amount    |                                                |
| discount        |                                                |
| tax             |                                                |
| payment_method  | cash, card, mobile payment, etc.               |
| status          | completed, refunded, cancelled                 |
| timestamp       |                                                |
| notes           |                                                |
| version         | Row version for sync conflict detection        |
| last_modified   | Timestamp of last modification                 |
| created_at      | Record creation timestamp                       |
| device_id       | POS terminal ID (for multi-device sync)        |
| user_id         | User who created/modified (FK to users table)  |

##### b. Sale Items Table

Individual items in each transaction.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| sale_item_id    | Primary Key (PK)                               |
| transaction_id  | Foreign Key (FK)                               |
| product_id      | Foreign Key (FK)                               |
| quantity        |                                                |
| unit_price      | Price at time of sale                          |
| subtotal        | quantity × unit_price                          |
| discount        | Item-level discount                            |
| kitchen_order_id| FK linking to Kitchen Orders Table             |
| version         | Row version for sync conflict detection        |
| last_modified   | Timestamp of last modification                 |
| created_at      | Record creation timestamp                       |
| device_id       | POS terminal ID (for multi-device sync)        |
| user_id         | User who created/modified (FK to users table)  |

##### c. Customers Table

Optional customer database for loyalty programs.

| Field         | Description                                    |
|---------------|------------------------------------------------|
| customer_id   | Primary Key (PK)                               |
| name          |                                                |
| phone         |                                                |
| email         |                                                |
| loyalty_points|                                                |
| created_date  |                                                |

##### d. Payment Methods Table

Tracks different payment types and reconciliation.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| payment_id      | Primary Key (PK)                               |
| transaction_id  | Foreign Key (FK)                               |
| method          | cash, card, mobile, split payment              |
| amount          |                                                |
| reference       | Card transaction ID, etc.                      |
| timestamp       |                                                |

#### 2. POS Features

- **Quick Product Selection**: Grid/button interface for fast item entry
- **Barcode Scanning**: Support for barcode scanners
- **Kitchen Integration**: Real-time order sending to kitchen
- **Receipt Printing**: Thermal printer support
- **Multiple Payment Methods**: Cash, card, mobile payments
- **Discounts & Promotions**: Percentage or fixed amount discounts
- **Split Bills**: Multiple payment methods per transaction
- **Daily Reports**: Sales summary, top products, payment breakdown
- **Offline Mode**: Continue working when internet is down
- **Inventory Check**: Real-time stock availability
- **Keyboard Hotkeys**:
  - Quick shortcuts for common products (F1-F12, number keys)
  - Function keys for payment methods (Ctrl+C for cash, Ctrl+D for card)
  - Navigation shortcuts (Tab, Enter, Esc)
  - Customizable hotkey mapping per user/role
  - Visual hotkey indicators on product buttons

---

## Database Schema Standards

### Standard Fields for All Tables

To support sync conflict resolution and audit trails, all tables should include:

| Field         | Type      | Description                                    |
|---------------|-----------|------------------------------------------------|
| version       | INTEGER   | Increments on each update (starts at 1)        |
| last_modified | TIMESTAMP | Auto-updated on each modification              |
| created_at    | TIMESTAMP | Record creation time (immutable)               |
| device_id     | TEXT      | POS terminal identifier (for multi-device sync)|
| user_id       | INTEGER   | User who created/modified (FK to users table)  |

**Audit Consistency Rules**:

- **All Critical Tables**: Must include `device_id` and `user_id` for complete audit trail
- **Master Data Tables** (products, ingredients, suppliers): `device_id` optional, `user_id` required
- **Transactional Tables** (sales, orders, waste, deliveries): Both `device_id` and `user_id` required
- **System Tables** (users, roles): `device_id` optional, `user_id` can reference self or NULL
- **Auto-populate**: `user_id` should be set from current session context on INSERT/UPDATE
- **Immutable Fields**: `created_at` and initial `user_id` should never change after creation

### Version Control Strategy

- **Initial Version**: All new records start with `version = 1`
- **Update Version**: On any UPDATE, increment `version` and update `last_modified`
- **Sync Conflict Detection**: Compare local and remote versions during sync
- **Conflict Resolution**:
  - If versions match → Safe to update
  - If local version < remote version → Remote is newer, use remote
  - If local version > remote version → Local is newer, use local
  - If versions differ but both modified → Manual review required

---

## Database Architecture

### Local Database (SQLite)

- Primary database for POS operations
- Fast read/write for transactions
- Stores all POS data locally
- Sync queue for pending uploads
- **Version Control**: All tables include `version` (INTEGER) and `last_modified` (TIMESTAMP) for conflict detection
- **Device ID**: Each POS terminal has unique `device_id` for multi-terminal sync

#### SQLite Performance Optimization

**Critical Indexes** (Required for high-volume POS):

- **Foreign Key Indexes**: Index all foreign key columns for faster joins
  - `ingredient_id`, `product_id`, `supplier_id`, `staff_id`, `customer_id`, `transaction_id`, etc.
- **Timestamp Indexes**: Index `last_modified`, `created_at`, `timestamp` for time-based queries
- **Composite Indexes**:
  - `(device_id, last_modified)` for device-specific sync queries
  - `(status, timestamp)` for kitchen orders filtering
  - `(date, device_id)` for daily sales reports
- **Query Optimization**:
  - Use `EXPLAIN QUERY PLAN` to analyze slow queries
  - Consider `PRAGMA journal_mode=WAL` for better concurrency
  - Use prepared statements for repeated queries
  - Batch inserts for bulk operations
- **Pre-aggregated Tables**: Use aggregated tables for reporting to avoid expensive GROUP BY operations
- **Connection Pooling**: Limit concurrent connections to prevent lock contention

### Cloud Database

- PostgreSQL/MySQL for production
- Stores consolidated ERP data
- Historical data and analytics
- Multi-location support (future)

#### Schema Consistency (Local vs Cloud)

**Critical**: Keep data types consistent between SQLite (local) and PostgreSQL/MySQL (cloud) to prevent sync failures.

| SQLite Type    | PostgreSQL Type | MySQL Type      | Notes                                    |
|----------------|-----------------|-----------------|------------------------------------------|
| INTEGER        | INTEGER/BIGINT  | INT/BIGINT      | Match size (INT vs BIGINT)               |
| TEXT           | VARCHAR/TEXT    | VARCHAR/TEXT    | Match length constraints                 |
| REAL           | REAL/DOUBLE     | DOUBLE          | Precision consistency                    |
| BLOB           | BYTEA           | BLOB            | Binary data handling                     |
| TIMESTAMP      | TIMESTAMP       | DATETIME        | **CRITICAL**: Use same format (ISO 8601) |
| DATE           | DATE            | DATE            | Format consistency                       |
| BOOLEAN        | BOOLEAN         | TINYINT(1)      | 0/1 vs true/false mapping                |

**Best Practices**:

- Use ISO 8601 format for all timestamps: `YYYY-MM-DD HH:MM:SS`
- Store timestamps in UTC, convert to local time in application layer
- Use same precision for decimal/numeric types
- Test sync with edge cases: NULL values, empty strings, max lengths
- Version your schema migrations for both local and cloud
- Use migration scripts that update both databases simultaneously
- Validate data types before sync to catch mismatches early

### Sync Mechanism

#### Daily Sync Process

1. **End of Day (EOD) Process**:
   - POS closes daily transactions
   - Validates all transactions
   - Creates sync batch
   - Uploads to cloud ERP
   - Confirms successful sync

2. **Real-time Sync** (Optional):
   - Critical updates (inventory, prices)
   - Kitchen order status
   - Product availability

3. **Conflict Resolution**:
   - Row-level versioning: All tables include `version` (integer) and `last_modified` (timestamp) fields
   - Version comparison during sync to detect conflicts
   - Last-write-wins for non-critical data (with version check)
   - Manual review for financial discrepancies
   - Audit trail for all syncs with conflict logs
   - Three-way merge strategy for complex conflicts
   - **Automatic Rollback**: Failed syncs automatically rollback to previous state
   - **Conflict Log Table**: Tracks all sync conflicts and anomalies for analysis

#### Conflict Log Table

Tracks all sync conflicts, failures, and anomalies for debugging and analysis.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| conflict_id     | Primary Key (PK)                               |
| table_name      | Table where conflict occurred                  |
| record_id       | ID of the conflicting record                  |
| device_id       | Device that attempted the sync                 |
| conflict_type   | version_mismatch, data_conflict, sync_failure  |
| local_version   | Version number from local database             |
| remote_version  | Version number from cloud database             |
| local_data      | JSON snapshot of local data                    |
| remote_data     | JSON snapshot of remote data                   |
| resolution      | auto_resolved, manual_review, rolled_back      |
| resolved_by     | User ID who resolved (if manual)               |
| resolved_at     | Timestamp of resolution                        |
| error_message   | Error details if sync failed                   |
| created_at      | When conflict was detected                     |

4. **Multi-Device Sync** (Multiple POS Terminals):
   - Each POS terminal has unique `device_id`
   - Local-first: Each device maintains its own SQLite database
   - Peer-to-peer sync option: Direct sync between terminals on same network
   - Centralized sync: All devices sync to cloud, then cloud distributes updates
   - Conflict resolution per device: Last-write-wins with device priority (configurable)
   - Real-time inventory updates across all terminals
   - Transaction locking: Prevent duplicate transactions during sync
   - Sync queue per device: Tracks what needs to be synced from each terminal
   - Device status monitoring: Track which terminals are online/offline

---

## Additional ERP Sections

### 3. Inventory Management

#### a. Stock Movements Table

Tracks all inventory changes.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| movement_id     | Primary Key (PK)                               |
| ingredient_id   | Foreign Key (FK)                               |
| movement_type   | delivery, waste, usage, adjustment              |
| quantity        |                                                |
| reference_id    | FK to delivery/waste/order tables              |
| timestamp       |                                                |
| staff_id        | Foreign Key (FK)                               |

#### c. Automatic Stock Updates

**Inventory calculations are automatically triggered** when related events occur:

1. **SQLite Triggers** (Recommended for local DB):
   - `AFTER INSERT` on `waste` table → Decrease `current_stock` in `ingredients`
   - `AFTER INSERT` on `produce_delivery` table → Increase `current_stock` in `ingredients`
   - `AFTER UPDATE status='ready'` on `kitchen_orders` → Calculate ingredient usage from recipe and decrease stock
   - `AFTER INSERT` on `stock_movements` → Update `current_stock` based on movement_type

2. **Backend Logic** (Alternative/Additional):
   - Service layer methods that wrap database operations
   - Atomic transactions ensuring stock consistency
   - Validation to prevent negative stock
   - Stock adjustment logging for audit trail

3. **Stock Update Flow**:

   ```text
   Waste Entry → Trigger → Update Ingredients.current_stock
   Delivery Entry → Trigger → Update Ingredients.current_stock
   Kitchen Order (ready) → Trigger → Calculate Recipe → Update Ingredients.current_stock
   Manual Adjustment → Backend Logic → Update Ingredients.current_stock + Log Movement
   ```

4. **Stock Validation**:
   - Check stock availability before creating kitchen orders
   - Alert when stock goes below `reorder_level`
   - Prevent negative stock (with override option for admins)
   - Real-time stock display in POS

#### b. Recipe Table

Links products to ingredients with quantities.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| recipe_id       | Primary Key (PK)                               |
| product_id      | Foreign Key (FK)                               |
| ingredient_id   | Foreign Key (FK)                               |
| quantity_needed | Amount required per unit of product            |
| unit            |                                                |

### 4. Sales & Reporting

#### a. Daily Sales Summary Table

Aggregated daily sales data. Pre-aggregated for fast reporting.

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| summary_id      | Primary Key (PK)                               |
| date            |                                                |
| total_sales     |                                                |
| total_transactions|                                              |
| payment_method_breakdown| JSON or separate table        |
| top_products    | JSON array                                     |
| sync_status     | pending, synced, error                         |
| last_updated    | Timestamp of last aggregation                  |

#### c. Pre-Aggregated Reporting Tables (Optional Performance Optimization)

For high-volume operations, maintain separate aggregated tables for faster queries.

**Product Sales Aggregated Table**:

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| agg_id          | Primary Key (PK)                               |
| product_id      | Foreign Key (FK)                               |
| date            |                                                |
| total_quantity  | Sum of quantities sold                         |
| total_revenue   | Sum of revenue                                 |
| transaction_count| Number of transactions                        |
| last_updated    |                                                |

**Payment Method Aggregated Table**:

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| agg_id          | Primary Key (PK)                               |
| date            |                                                |
| payment_method  |                                                |
| total_amount    |                                                |
| transaction_count|                                              |
| last_updated    |                                                |

*Note: These can be populated via triggers, scheduled jobs, or real-time aggregation depending on performance needs.*

#### b. Reports Available

- **Daily Sales Report**: Revenue, transactions, payment methods
- **Product Performance**: Best sellers, slow movers
- **Inventory Reports**: Low stock alerts, waste analysis
- **Staff Performance Reports**:
  - Sales by staff member (cashiers, waiters, servers)
  - Kitchen efficiency (orders per hour, average prep time)
  - Floor staff performance (tables served, customer ratings)
  - Attendance reports (punctuality, absences, overtime)
  - Cleaning/maintenance task completion
  - Staff productivity metrics
- **Cost Analysis**: Ingredient costs vs. sales
- **Profit Margins**: Product profitability
- **Waste Reports**: Waste tracking and cost impact
- **Staff Scheduling Reports**: Shift coverage, labor costs, schedule compliance
- **Payroll Reports**: Hours worked, overtime, department labor costs

### 5. User Management

#### a. Users Table

System users (ERP and POS access).

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| user_id         | Primary Key (PK)                               |
| username        |                                                |
| password_hash   |                                                |
| role            | admin, manager, cashier, chef, staff           |
| permissions     | JSON array of permissions                      |
| is_active       |                                                |
| created_date    |                                                |
| last_login      |                                                |

#### b. Roles & Permissions

- **Admin**: Full system access
- **Manager**: Reports, inventory, staff management
- **Cashier**: POS operations, basic reports
- **Chef**: Kitchen orders, waste logging
- **Staff**: View-only access

---

## Technology Stack

### Application Type

- **Platform**: Windows Desktop Application
- **Language**: Python 3.9+
- **Architecture**: Desktop application with local SQLite database and cloud sync
- **Installation**: Custom setup wizard for Windows installation

### GUI Framework

- **Primary Options**:
  - **PyQt5/PyQt6**: Professional, feature-rich, native Windows look
  - **tkinter**: Built-in Python, lightweight, customizable
  - **Custom Framework**: Custom-built UI using Python libraries
- **UI Design**: Modern, responsive Windows-native interface
- **State Management**: Python classes and data structures (no web framework needed)

### Core Python Libraries

- **Database**:
  - `sqlite3`: Built-in SQLite support
  - `SQLAlchemy`: ORM for database operations and migrations
  - `alembic`: Database migration tool
- **GUI**:
  - `PyQt5/PyQt6` or `tkinter`: UI framework
  - `customtkinter`: Modern tkinter styling (if using tkinter)
  - `Pillow`: Image processing for UI elements
- **Data Handling**:
  - `pandas`: Data manipulation and reporting
  - `numpy`: Numerical operations (if needed for analytics)
  - `json`: Configuration and data serialization
  - `datetime`: Date/time handling
- **Configuration**:
  - `configparser`: Configuration file management
  - `pyyaml`: YAML configuration files (optional)

### Hardware Integration Libraries

- **Receipt Printing**:
  - `python-escpos`: ESC/POS printer support
  - `win32print`: Windows printing API
  - `reportlab`: PDF receipt generation (optional)
- **Barcode Scanner**:
  - `pyserial`: Serial port communication
  - `keyboard`: Keyboard input capture (for USB HID scanners)
  - `pywin32`: Windows API access
- **Cash Drawer**:
  - `python-escpos`: Cash drawer control via printer
  - `pyserial`: Direct serial control
- **Card Reader**:
  - Payment gateway SDKs (Stripe, Square, etc.)
  - `requests`: HTTP API communication

### Windows-Specific Libraries

- **System Integration**:
  - `pywin32`: Windows API access, registry, services
  - `wmi`: Windows Management Instrumentation
  - `psutil`: System and process utilities
- **File System**:
  - `pathlib`: Modern path handling
  - `shutil`: File operations
- **Windows Services**:
  - `pywin32`: Create Windows service for background sync
  - `python-daemon`: Alternative for background processes

### Setup & Installation

- **Installer Creation**:
  - `cx_Freeze`: Package Python app as Windows executable
  - `PyInstaller`: Create standalone Windows executables
  - `Inno Setup`: Professional Windows installer (with custom wizard)
  - `NSIS`: Nullsoft Scriptable Install System (alternative)
- **Custom Setup Wizard**:
  - Built with Python GUI framework (PyQt/tkinter)
  - Steps:
    1. Welcome screen
    2. License agreement
    3. Installation directory selection
    4. Database initialization
    5. Initial admin user setup
    6. Hardware configuration (printer, scanner, etc.)
    7. Cloud sync configuration (optional)
    8. Installation progress
    9. Completion and launch option
- **Packaging**:
  - `setuptools`: Python package management
  - `wheel`: Built distribution format

### Sync & Communication

- **HTTP Client**:
  - `requests`: HTTP requests for cloud sync
  - `urllib3`: Low-level HTTP library
- **Background Tasks**:
  - `threading`: Multi-threading for sync operations
  - `queue`: Task queue management
  - `schedule`: Scheduled tasks (EOD sync)
- **Data Serialization**:
  - `json`: JSON data format
  - `pickle`: Python object serialization (local use only)
- **Auto-Update**:
  - `requests`: GitHub API calls for release checking
  - `semver`: Semantic versioning comparison (optional)
  - `zipfile`: Extract update packages
  - `shutil`: File operations for update installation

### Reporting & Analytics

- **Report Generation**:
  - `reportlab`: PDF report generation
  - `openpyxl`: Excel file generation
  - `matplotlib`: Charts and graphs
  - `seaborn`: Statistical visualizations
- **Data Export**:
  - `pandas`: Data export to CSV, Excel, etc.
  - `csv`: CSV file handling

### Security & Authentication

- **Password Hashing**:
  - `bcrypt`: Secure password hashing
  - `passlib`: Password hashing library
- **Encryption**:
  - `cryptography`: Encryption for sensitive data
  - `keyring`: Secure credential storage (Windows Credential Manager)

### Testing & Development

- **Testing**:
  - `pytest`: Unit and integration testing
  - `unittest`: Built-in testing framework
- **Code Quality**:
  - `black`: Code formatting
  - `flake8`: Linting
  - `pylint`: Code analysis
- **Documentation**:
  - `sphinx`: Documentation generation
  - `docstrings`: Inline documentation

### Additional Utilities

- **Logging**:
  - `logging`: Built-in logging module
  - `loguru`: Enhanced logging (optional)
- **Date/Time**:
  - `pytz`: Timezone handling
  - `dateutil`: Advanced date parsing
- **Validation**:
  - `pydantic`: Data validation
  - `cerberus`: Schema validation

---

## Windows Application Architecture

### Application Structure

```
sphincs-erp-pos/
├── src/
│   ├── erp_main.py             # Sphincs ERP application entry point
│   ├── pos_main.py             # Sphincs POS application entry point
│   ├── gui/                    # GUI components
│   │   ├── splash_screen.py    # Splash screen with update checking
│   │   ├── pos_window.py       # Main POS interface
│   │   ├── erp_dashboard.py    # ERP dashboard
│   │   ├── login_window.py     # Login screen (shared)
│   │   └── widgets/            # Custom widgets
│   ├── database/               # Database layer (shared)
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── migrations/         # Database migrations
│   │   └── connection.py       # Database connection
│   ├── business/               # Business logic
│   │   ├── pos_logic.py        # POS operations
│   │   ├── inventory.py        # Inventory management
│   │   └── sync_service.py     # Cloud sync service
│   ├── hardware/               # Hardware integration
│   │   ├── printer.py          # Receipt printer
│   │   ├── scanner.py          # Barcode scanner
│   │   └── cash_drawer.py      # Cash drawer control
│   ├── config/                 # Configuration (shared)
│   │   └── settings.py         # App settings
│   └── utils/                  # Utilities (shared)
│       ├── logger.py           # Logging
│       ├── helpers.py          # Helper functions
│       └── update_checker.py   # Auto-update checker (GitHub releases)
├── setup_wizard/               # Custom setup wizard
│   ├── wizard_main.py          # Wizard entry point
│   ├── steps/                  # Wizard steps
│   │   ├── welcome.py
│   │   ├── database_setup.py
│   │   ├── admin_setup.py
│   │   └── hardware_config.py
│   └── resources/              # Wizard resources
├── installer/                  # Installer scripts
│   ├── inno_setup.iss          # Inno Setup script
│   └── build_installer.py      # Build script
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
└── README.md                   # Documentation
```

### Two Separate Applications

The system consists of **two separate Windows applications** that share the same database:

1. **Sphincs ERP** (`erp_main.py`)
   - ERP dashboard and management interface
   - Inventory management
   - Staff management
   - Reports and analytics
   - Supplier management
   - System administration

2. **Sphincs POS** (`pos_main.py`)
   - Point of Sale interface
   - Transaction processing
   - Receipt printing
   - Kitchen order integration
   - Real-time inventory checks

Both applications:

- Share the same SQLite database
- Use the same authentication system
- Can run simultaneously on the same machine
- Have separate desktop shortcuts
- Have separate Start Menu entries

### Windows-Specific Considerations

- **File Paths**: Use `pathlib` for cross-platform path handling
- **Registry**: Store configuration in Windows Registry (optional) or config files
- **Start Menu**: Create Start Menu shortcuts for both applications during installation
  - Sphincs ERP shortcut
  - Sphincs POS shortcut
- **Desktop Shortcuts**: Create desktop shortcuts for both applications:
  - **Sphincs ERP** desktop shortcut
  - **Sphincs POS** desktop shortcut
- **Application Icons**: Separate icons for ERP and POS applications
- **Executable Names**:
  - `SphincsERP.exe` for ERP application
  - `SphincsPOS.exe` for POS application
- **Auto-Start**: Optional Windows service for background sync
- **Windows Notifications**: Use Windows toast notifications for alerts
- **System Tray**: Optional system tray icon for background operations (can be separate for each app)
- **Windows Theme**: Respect Windows theme (light/dark mode)
- **DPI Scaling**: Support high-DPI displays
- **Windows Firewall**: Handle firewall exceptions for network sync
- **Multiple Instances**: Both applications can run simultaneously on the same machine
- **Splash Screen**: Both applications display a splash screen on startup with branding and update checking

### Splash Screen

Both **Sphincs ERP** and **Sphincs POS** applications display a splash screen during startup that provides visual feedback and performs initialization tasks, including update checking.

#### Splash Screen Features

**Visual Elements**:
- **Application Logo**: Large, centered logo (ERP or POS specific)
- **Application Name**: "Sphincs ERP" or "Sphincs POS"
- **Version Number**: Current application version displayed
- **Loading Indicator**: Animated progress indicator or spinner
- **Status Text**: Dynamic status messages (e.g., "Initializing...", "Loading database...", "Checking for updates...")
- **Background**: Branded background (gradient or solid color matching design system)

**Functionality**:
- **Initialization Tasks**: Performs startup tasks while displaying splash screen:
  - Database connection check
  - Configuration loading
  - Update checking (GitHub releases)
  - Resource loading
- **Update Check Integration**: Checks for updates during splash screen display
- **Update Notification Module**: If update detected, shows update notification overlay on splash screen
- **Minimum Display Time**: Ensures splash screen is visible for at least 1-2 seconds (even if initialization is fast)
- **Auto-Close**: Automatically closes when initialization completes and main window is ready

#### Splash Screen Update Notification Module

When an update is detected during splash screen initialization, an **update notification module** is displayed on the splash screen:

**Update Module Layout**:
- **Position**: Overlay on splash screen (centered or top-right)
- **Background**: Semi-transparent or solid background (matching design system)
- **Border**: Subtle border or shadow for visibility
- **Size**: Compact but readable (approximately 400x300px)

**Update Module Content**:
- **Icon**: Update/notification icon (e.g., download icon, bell icon)
- **Title**: "New Update Available" or "Update Available"
- **Version Info**:
  - Current version: `v1.2.3`
  - New version: `v1.3.0`
- **Brief Description**: Short summary of update (from release notes, first paragraph)
- **Action Buttons**:
  - **"Install Later"** button (secondary style)
  - **"Install Now"** button (primary style)

**Update Module Behavior**:
- **Non-Blocking**: App continues to launch normally regardless of user choice
- **User Choice**:
  - **"Install Later"**: Dismisses module, app launches normally, update notification can be shown later in-app
  - **"Install Now"**: Initiates update process (download → install → restart)
- **Auto-Dismiss**: If user doesn't interact, module can auto-dismiss after splash screen closes (optional)
- **Persistent**: If user clicks "Install Later", update notification can be shown again in the main app

#### Splash Screen Flow

**Startup Sequence**:

1. **Splash Screen Appears**:
   - Show splash screen immediately on app launch
   - Display logo, app name, version
   - Show loading indicator

2. **Initialization Tasks** (Parallel/Background):
   - Load configuration
   - Connect to database
   - Initialize services
   - **Check for updates** (GitHub API call)

3. **Update Check Result**:
   - **If Update Available**:
     - Display update notification module on splash screen
     - Wait for user interaction OR continue if user doesn't respond
   - **If No Update**:
     - Continue normal startup

4. **Main Window Ready**:
   - Prepare main application window
   - Load initial data

5. **Splash Screen Closes**:
   - Fade out splash screen
   - Show main application window
   - If update module was shown and user chose "Install Later", show update notification in main app

#### Splash Screen Design Specifications

**Dimensions**:
- **Width**: `600px` (or responsive to screen size)
- **Height**: `400px` (or responsive to screen size)
- **Position**: Centered on screen

**Colors** (from design system):
- **Background**: White or light gradient
- **Logo Area**: Primary blue accent
- **Text**: Dark gray (`#374151`)
- **Loading Indicator**: Primary blue (`#2563EB`)

**Typography**:
- **App Name**: `24px`, Semi-bold, Primary blue
- **Version**: `14px`, Regular, Medium gray
- **Status Text**: `12px`, Regular, Medium gray

**Animation**:
- **Fade In**: `250ms` ease-out
- **Fade Out**: `250ms` ease-in
- **Loading Spinner**: Continuous rotation animation

#### Implementation Details

**Splash Screen Module** (`src/gui/splash_screen.py`):
```python
class SplashScreen(QSplashScreen):
    def __init__(self, app_name, app_version, app_icon):
        super().__init__()
        self.app_name = app_name
        self.app_version = app_version
        self.setup_ui()
        self.update_checker = None
        self.update_available = False
    
    def setup_ui(self):
        """Setup splash screen UI"""
        # Create layout with logo, app name, version
        # Add loading indicator
        # Add status text area
    
    def check_for_updates(self):
        """Check for updates in background"""
        # Initialize update checker
        # Query GitHub API
        # If update available, show update module
    
    def show_update_module(self, update_info):
        """Display update notification module on splash screen"""
        # Create update module overlay
        # Show version info
        # Add "Install Later" and "Install Now" buttons
    
    def on_install_later(self):
        """Handle 'Install Later' button click"""
        # Dismiss update module
        # Continue app launch
        # Schedule update notification for later
    
    def on_install_now(self):
        """Handle 'Install Now' button click"""
        # Start update process
        # Download update
        # Install update
        # Restart application
```

**Integration with Main Application**:
- Splash screen is shown before main window
- Main window initialization happens in background
- Splash screen closes when main window is ready
- Update module interaction doesn't block app launch

### Auto-Update System

Both **Sphincs ERP** and **Sphincs POS** applications include automatic update functionality that checks for new releases from the GitHub repository.

#### Update Detection

**GitHub Release Checking**:
- **Repository**: GitHub repository URL (configurable)
- **API Endpoint**: `https://api.github.com/repos/{owner}/{repo}/releases/latest`
- **Check Frequency**:
  - **On application startup** (during splash screen initialization)
  - Manual check via "Check for Updates" menu option
  - Scheduled check (configurable, default: once per day)
- **Version Comparison**: Compare current version with latest GitHub release tag
- **Update Notification**:
  - **Primary**: Update notification module on splash screen (if update detected during startup)
  - **Secondary**: Update dialog in main application (if user chose "Install Later" or manual check)
  - **Tertiary**: System tray notification (optional)

#### Update Process

**Update Flow**:

1. **Check for Updates**:
   - Query GitHub Releases API (during splash screen initialization)
   - Compare current version with latest release tag
   - If newer version exists, show update notification

2. **Update Notification** (Splash Screen):
   - **If update detected during startup**:
     - Display update notification module on splash screen
     - Show current version, new version, brief description
     - Display "Install Later" and "Install Now" buttons
     - App continues to launch regardless of user choice
   - **If user chooses "Install Later"**:
     - Dismiss splash screen update module
     - App launches normally
     - Update notification can be shown again in main app

3. **Update Notification** (Main Application):
   - Display update dialog with:
     - Current version
     - New version available
     - Release notes (from GitHub release description)
     - "Update Now" and "Remind Me Later" options
   - Non-blocking (user can continue working)
   - Shown if user chose "Install Later" on splash screen or manual check

4. **Download Update**:
   - Download release assets (installer or update package)
   - Show download progress
   - Verify download integrity (checksum if available)

5. **Install Update**:
   - **Option A - Full Installer**: Launch installer, close app, run installer, restart app
   - **Option B - Update Package**: Extract update files, backup current installation, apply updates, restart app
   - **Option C - Auto-Updater**: Use dedicated updater executable that handles the update process

6. **Post-Update**:
   - Verify installation
   - Show "Update Complete" notification
   - Log update to update history

#### Update Configuration

**Settings** (stored in config file or Windows Registry):
- **Enable Auto-Update**: Boolean (default: `true`)
- **Check on Startup**: Boolean (default: `true`)
- **Check Interval**: Hours (default: `24`)
- **Auto-Download**: Boolean (default: `false` - user must confirm)
- **Auto-Install**: Boolean (default: `false` - user must confirm)
- **GitHub Repository**: Repository URL (e.g., `owner/repo-name`)
- **Update Channel**: `stable`, `beta`, `alpha` (default: `stable`)

#### Update Safety

**Safety Measures**:
- **Backup Before Update**: Create backup of current installation
- **Rollback Capability**: Keep previous version for rollback if update fails
- **Database Compatibility**: Check database schema version before applying update
- **Update Logging**: Log all update attempts and results
- **Error Handling**: Graceful handling of network errors, download failures
- **Offline Mode**: Skip update check if offline, queue for later

#### Update UI Components

**Splash Screen Update Module**:
- Overlay module displayed on splash screen when update detected
- Shows version information (current vs new)
- Brief update description
- **"Install Later"** button (secondary style) - dismisses module, app launches
- **"Install Now"** button (primary style) - starts update process
- Non-blocking (app launches regardless of choice)

**Update Dialog** (Main Application):
- Modal dialog showing update information
- Release notes display (scrollable)
- Download progress bar
- Install progress indicator
- Error messages if update fails
- **"Update Now"** and **"Remind Me Later"** buttons

**Update Menu Items**:
- **Help → Check for Updates**: Manual update check
- **Help → Update History**: View past updates
- **Settings → Update Settings**: Configure update behavior

**System Tray Notification**:
- Show notification when update is available (optional)
- Click to open update dialog

#### Implementation Details

**Update Checker Module** (`src/utils/update_checker.py`):
```python
class UpdateChecker:
    def __init__(self, repo_owner, repo_name, current_version):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    
    def check_for_updates(self):
        """Check GitHub for latest release"""
        # Query GitHub API
        # Compare versions
        # Return update info if available
    
    def download_update(self, release_url):
        """Download update package"""
        # Download release assets
        # Show progress
        # Verify integrity
    
    def install_update(self, update_path):
        """Install update"""
        # Backup current installation
        # Extract/install update
        # Restart application
```

**Update Service** (Background Thread):
- Runs update check on startup (non-blocking)
- Scheduled periodic checks
- Handles download in background
- Shows notifications when ready

**Version Management**:
- Store current version in `VERSION` file or `__version__` in code
- Use semantic versioning (e.g., `1.2.3`)
- Compare versions using `semver` library or custom comparison

#### GitHub Release Requirements

**Release Format**:
- **Tag Name**: Semantic version (e.g., `v1.2.3`)
- **Release Title**: Version number and brief description
- **Release Notes**: Detailed changelog in description
- **Assets**:
  - Windows installer (`.exe` or `.msi`)
  - Or update package (`.zip`)

**Release Assets**:
- `SphincsERP-Setup-v1.2.3.exe` - ERP installer
- `SphincsPOS-Setup-v1.2.3.exe` - POS installer
- Or combined: `Sphincs-ERP-POS-Setup-v1.2.3.exe`

#### Update Scenarios

**Scenario 1 - Both Apps Need Update**:
- Both apps check independently
- Each app shows its own update notification
- User can update both separately or together

**Scenario 2 - Only One App Needs Update**:
- Only the outdated app shows update notification
- Other app continues normally

**Scenario 3 - Update During Active Session**:
- User can defer update
- Update can be scheduled for later (e.g., end of day)
- Critical updates can force immediate update (with warning)

**Scenario 4 - Offline/Network Error**:
- Skip update check silently
- Log error for debugging
- Retry on next check interval

#### Update Logging

**Update History Table** (optional, in database or log file):
- `update_id`: Primary key
- `app_name`: `ERP` or `POS`
- `old_version`: Previous version
- `new_version`: Updated version
- `update_date`: Timestamp
- `update_status`: `success`, `failed`, `rolled_back`
- `release_notes`: Changelog
- `error_message`: If failed

### Custom Setup Wizard Details

#### Wizard Flow

1. **Welcome Screen**
   - Application name and version
   - Brief description
   - System requirements check
   - Next/Cancel buttons

2. **License Agreement**
   - Display license text
   - Accept/Decline radio buttons
   - Next button (disabled until accepted)

3. **Installation Directory**
   - Default: `C:\Program Files\Sphincs ERP+POS`
   - Browse button for custom location
   - Disk space check
   - Create directory if doesn't exist

4. **Database Initialization**
   - Create SQLite database file
   - Initialize schema
   - Create default tables
   - Progress indicator
   - Error handling and rollback

5. **Initial Admin User Setup**
   - Admin username
   - Admin password (with confirmation)
   - Email (optional)
   - Validation and error messages

6. **Hardware Configuration**
   - **Receipt Printer**:
     - Detect available printers
     - Select default printer
     - Test print option
   - **Barcode Scanner**:
     - Select scanner type (USB HID, Serial)
     - Test scan option
   - **Cash Drawer**:
     - Configure connection (via printer or direct)
     - Test open option
   - **Card Reader** (optional):
     - Payment gateway selection
     - API key configuration

7. **Cloud Sync Configuration** (Optional)
   - Enable/disable cloud sync
   - Cloud server URL
   - API credentials
   - Test connection button
   - Skip option

8. **Installation Progress**
   - Copy files to installation directory
   - Create database
   - Configure settings
   - Create desktop shortcuts for both applications:
     - **Sphincs ERP** shortcut
     - **Sphincs POS** shortcut
   - Create Start Menu entries for both applications
   - Progress bar with percentage
   - Cancel option (with cleanup)

9. **Completion**
   - Success message
   - Information about two applications created:
     - Sphincs ERP (desktop shortcut)
     - Sphincs POS (desktop shortcut)
   - Launch options:
     - Launch Sphincs ERP checkbox
     - Launch Sphincs POS checkbox
   - Open documentation checkbox
   - Finish button

#### Wizard Implementation

- **Framework**: Use same GUI framework as main app (PyQt/tkinter)
- **State Management**: Store wizard state in memory, write to config file at end
- **Validation**: Validate each step before proceeding
- **Error Handling**: Graceful error handling with user-friendly messages
- **Rollback**: Ability to rollback on cancellation or error
- **Logging**: Log all wizard actions for troubleshooting

#### Wizard Features

- **Back/Next Navigation**: Navigate between steps
- **Progress Indicator**: Show current step and total steps
- **Validation**: Real-time validation with error messages
- **Help**: Context-sensitive help for each step
- **Cancel**: Cancel at any time with confirmation
- **Minimize**: Allow minimizing wizard window
- **System Requirements**: Check Python version, disk space, permissions

---

## Implementation Phases

### Phase 0: Setup & Infrastructure

- [ ] Set up Python development environment
- [ ] Create project structure
- [ ] Create `requirements.txt` with all dependencies
- [ ] Set up version control (Git)
- [ ] Design and implement custom setup wizard
- [ ] Create installer build scripts (Inno Setup/PyInstaller)
- [ ] Configure installer to create two separate executables:
  - [ ] Sphincs ERP executable (`SphincsERP.exe`)
  - [ ] Sphincs POS executable (`SphincsPOS.exe`)
- [ ] Configure installer to create desktop shortcuts for both applications
- [ ] Configure installer to create Start Menu entries for both applications
- [ ] Design separate icons for ERP and POS applications
- [ ] Test installation process
- [ ] Create basic logging system
- [ ] Set up configuration management

### Phase 1: Core Database & Local POS

- [ ] Set up SQLite database schema with version fields
- [ ] Create database indexes (foreign keys, timestamps)
- [ ] Implement audit fields (device_id, user_id) on all tables
- [ ] Design and implement Windows GUI framework (PyQt/tkinter)
- [ ] Create shared login/authentication window
- [ ] Create `pos_main.py` entry point for Sphincs POS application
- [ ] Create basic POS interface (Windows native)
- [ ] Implement product selection and cart
- [ ] Basic transaction recording
- [ ] Receipt generation (ESC/POS printer support)
- [ ] Keyboard hotkey system for fast operations
- [ ] Windows-specific optimizations (DPI scaling, theme support)
- [ ] Create `erp_main.py` entry point for Sphincs ERP application (basic shell)
- [ ] Implement splash screen:
  - [ ] Create `splash_screen.py` module with splash screen UI
  - [ ] Design splash screen layout (logo, app name, version, loading indicator)
  - [ ] Implement splash screen animations (fade in/out, loading spinner)
  - [ ] Integrate splash screen with application startup
  - [ ] Add status text updates during initialization
  - [ ] Implement minimum display time (1-2 seconds)
  - [ ] Test splash screen on both ERP and POS applications
- [ ] Implement auto-update system:
  - [ ] Create `update_checker.py` module for GitHub release checking
  - [ ] Implement version comparison logic
  - [ ] Integrate update check into splash screen initialization
  - [ ] Create splash screen update notification module:
    - [ ] Design update module overlay UI
    - [ ] Add "Install Later" and "Install Now" buttons
    - [ ] Implement non-blocking update notification
    - [ ] Handle user interaction (install now vs install later)
  - [ ] Create update notification dialog (for main app)
  - [ ] Implement update download functionality
  - [ ] Add "Check for Updates" menu option (Help menu)
  - [ ] Add update settings to configuration
  - [ ] Implement update logging
  - [ ] Test update flow with GitHub releases (splash screen and main app)

### Phase 2: Kitchen Integration

- [ ] Kitchen Orders table and logic
- [ ] Real-time order display for kitchen
- [ ] Order status updates
- [ ] Kitchen staff assignment
- [ ] Floor staff integration (waiter/server assignment to orders)
- [ ] Table number tracking for dine-in orders

### Phase 3: Inventory Management

- [ ] Ingredients tracking
- [ ] Stock level monitoring
- [ ] Waste logging
- [ ] Delivery tracking
- [ ] Low stock alerts
- [ ] Automatic stock update triggers (SQLite triggers or backend logic)
- [ ] Stock validation before kitchen orders
- [ ] Real-time stock calculations

### Phase 4: ERP Dashboard

- [ ] Admin dashboard
- [ ] Sales reports
- [ ] Pre-aggregated reporting tables (optional performance optimization)
- [ ] Database performance tuning (indexes, query optimization)
- [ ] Inventory reports
- [ ] Comprehensive staff management system:
  - [ ] Staff database (all departments)
  - [ ] Staff scheduling system
  - [ ] Attendance tracking (clock-in/clock-out)
  - [ ] Staff task management
  - [ ] Floor staff table assignments
  - [ ] Cleaning log system
  - [ ] Staff performance tracking
- [ ] Supplier management

### Phase 5: Cloud Sync

- [ ] Cloud database setup
- [ ] Schema consistency validation (local vs cloud data types)
- [ ] Sync service implementation (Windows background service)
- [ ] EOD sync process
- [ ] Row-level versioning implementation (version + last_modified fields)
- [ ] Conflict resolution with version checking
- [ ] Conflict log table implementation
- [ ] Automatic rollback for failed syncs
- [ ] Sync status monitoring (Windows system tray icon)
- [ ] Multi-device sync logic (device_id tracking)
- [ ] Sync queue per device
- [ ] Device status monitoring
- [ ] Audit trail implementation (device_id + user_id on all critical tables)
- [ ] Windows service for background sync (optional)

### Phase 6: Advanced Features (Phased Approach)

**Note**: These features should be implemented incrementally based on business needs and user feedback. Don't attempt all at once.

**Phase 6a - Customer & Loyalty**:

- [ ] Customer loyalty program
- [ ] Customer analytics

**Phase 6b - Mobile & Integration**:

- [ ] Mobile app for managers
- [ ] API for third-party integrations
- [ ] Online ordering integration

**Phase 6c - Multi-Location**:

- [ ] Multi-location support
- [ ] Cross-location reporting
- [ ] Centralized inventory management

**Phase 6d - Advanced Analytics**:

- [ ] Advanced analytics with ML
- [ ] Predictive inventory management
- [ ] Sales forecasting

**Phase 6e - Internationalization**:

- [ ] Multi-currency support
- [ ] Multi-language support
- [ ] Regional compliance features

---

## Key Features Summary

### Two Separate Applications

The system consists of **two separate Windows applications**:

1. **Sphincs POS** - Point of Sale application
2. **Sphincs ERP** - Enterprise Resource Planning application

Both applications share the same database and can run simultaneously.

### Sphincs POS Features

✅ Fast transaction processing  
✅ Multiple payment methods  
✅ Kitchen order integration  
✅ Receipt printing  
✅ Offline capability  
✅ Daily sales reports  
✅ Real-time inventory checks  
✅ Barcode scanning support  
✅ Keyboard hotkeys for fast operations  
✅ Splash screen with update checking  
✅ Auto-update from GitHub releases  

### Sphincs ERP Features

✅ Inventory management  
✅ Waste tracking  
✅ Supplier management  
✅ Comprehensive staff management:

- All staff types (kitchen, floor, cleaning, management, security, delivery, cashier)
- Staff scheduling and shift management
- Attendance tracking (clock-in/clock-out)
- Task assignment and tracking
- Floor staff table assignments
- Cleaning and maintenance logs
- Staff performance reviews
✅ Sales analytics  
✅ Cost analysis  
✅ Recipe management  
✅ Advanced reporting and dashboards  
✅ Splash screen with update checking  
✅ Auto-update from GitHub releases  

### Integration Features

✅ Local-first architecture  
✅ Cloud sync  
✅ Real-time updates  
✅ Data backup  
✅ Multi-user support  

---

## Database Relationships

### Key Relationships

- **Products** → **Recipes** → **Ingredients**
- **Sales Transactions** → **Sale Items** → **Products**
- **Sale Items** → **Kitchen Orders**
- **Kitchen Orders** → **Staff** (kitchen staff) + **Staff** (floor staff)
- **Sales Transactions** → **Staff** (cashier/server) + **Staff** (floor staff)
- **Staff** → **Staff Schedule** → **Staff Attendance**
- **Staff** → **Staff Tasks** (cleaning, maintenance)
- **Staff** → **Floor Staff Assignments** (table assignments)
- **Staff** → **Cleaning Log** (cleaning activities)
- **Staff** → **Staff Performance** (reviews and evaluations)
- **Ingredients** → **Waste** / **Produce Delivery**
- **Ingredients** → **Suppliers**
- **Waste** → **Staff** (who logged waste)
- **Produce Delivery** → **Staff** (who received delivery)
- **All Tables** → **Users** (for audit trail)
- **All Tables** → **Staff** (where applicable for tracking)

---

## Risk Management & Mitigation

### Critical Risks & Solutions

This section addresses potential issues and provides mitigation strategies to prevent system failures, data corruption, and operational chaos.

---

### 1. Database Concurrency & Locking Issues

#### Problem: SQLite Database Locks

- Multiple POS terminals writing simultaneously → "database is locked" errors
- Long-running queries blocking transactions
- Deadlocks between applications

#### Solutions

- **WAL Mode**: Enable Write-Ahead Logging (`PRAGMA journal_mode=WAL`) for better concurrency
- **Connection Pooling**: Limit concurrent connections per application (max 2-3 per POS terminal)
- **Transaction Timeouts**: Implement 5-second timeout with retry logic (exponential backoff)
- **Read-Only Connections**: Use separate read-only connections for reports/dashboards
- **Query Optimization**: Keep transactions short, avoid long-running queries during peak hours
- **Lock Detection**: Monitor for lock contention, alert if locks exceed threshold
- **Queue System**: Queue write operations during high contention periods
- **Database Sharding** (Future): Consider separate databases per terminal with sync

#### Implementation

```python
# Example: Connection with timeout and retry
def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn
```

---

### 2. Version Conflicts & Data Overwrites

#### Problem: Last-Write-Wins Failures

- Version conflicts not properly detected
- Sales or inventory data overwritten incorrectly
- Manual database edits bypassing version control

#### Solutions

- **Strict Version Checking**: Always compare versions before UPDATE operations
- **Optimistic Locking**: Fail UPDATE if version doesn't match, require refresh
- **Conflict Detection**: Log all conflicts to Conflict Log table for review
- **Read-Only Database Access**: Prevent direct SQLite file access (encrypt or restrict permissions)
- **Application-Level Validation**: Validate data before database operations
- **Transaction Isolation**: Use proper isolation levels for critical operations
- **Audit Trail**: Log all version changes with before/after snapshots
- **Manual Override Protection**: Require admin approval for manual database edits

#### Implementation

```python
# Example: Version-aware update
def update_with_version(table, record_id, data, expected_version):
    current = get_record(table, record_id)
    if current['version'] != expected_version:
        raise VersionConflictError("Record was modified by another user")
    # Proceed with update, increment version
```

---

### 3. Trigger Hell & Stock Calculation Errors

#### Problem: Trigger-Induced Chaos

- Triggers firing at wrong times
- Recipe changes causing negative stock
- Cascading trigger failures
- Stock updates not atomic

#### Solutions

- **Disable Triggers During Critical Operations**: Temporarily disable triggers during bulk updates
- **Atomic Transactions**: Wrap stock updates in transactions with rollback on error
- **Pre-Validation**: Check stock availability BEFORE creating kitchen orders
- **Recipe Locking**: Prevent recipe modifications during active shifts
- **Stock Reserve System**: Reserve stock when order created, deduct when order completed
- **Trigger Logging**: Log all trigger executions for debugging
- **Fallback Logic**: If trigger fails, use application-level stock calculation
- **Recipe Versioning**: Track recipe changes, maintain historical versions

#### Implementation

```python
# Example: Stock reservation system
def create_kitchen_order(product_id, quantity):
    # Reserve stock first
    reserve_stock(product_id, quantity)
    try:
        # Create order
        order = create_order(product_id, quantity)
        # Deduct stock when order ready
        return order
    except Exception:
        # Release reservation on error
        release_reservation(product_id, quantity)
        raise
```

---

### 4. Schema Drift & Type Mismatches

#### Problem: Local vs Cloud Schema Inconsistencies

- TEXT vs VARCHAR mismatches
- TIMESTAMP format differences
- Missing columns in one database
- Migration failures

#### Solutions

- **Schema Versioning**: Track schema version in both databases
- **Migration Scripts**: Version-controlled migrations for both SQLite and cloud DB
- **Schema Validation**: Validate schema on startup, fail if mismatch detected
- **Type Normalization**: Use consistent types (always TEXT for strings, INTEGER for numbers)
- **Migration Testing**: Test migrations on staging before production
- **Rollback Plan**: Maintain ability to rollback schema changes
- **Automated Checks**: Run schema validation before sync operations
- **Documentation**: Document all schema changes with migration notes

#### Implementation

```python
# Example: Schema validation
def validate_schema():
    local_version = get_schema_version(local_db)
    cloud_version = get_schema_version(cloud_db)
    if local_version != cloud_version:
        raise SchemaMismatchError("Schema versions don't match")
```

---

### 5. Cloud Sync Failures & Data Corruption

#### Problem: Network Failures & Partial Uploads

- EOD sync interrupted → partial data in cloud
- Network timeouts → transactions lost
- Corrupt data synced to cloud
- Sync conflicts not resolved

#### Solutions

- **Idempotent Sync**: Design sync operations to be safely repeatable
- **Batch Transactions**: Sync in small batches (100-500 records) with checkpoints
- **Sync Queue**: Queue all sync operations, retry on failure
- **Data Validation**: Validate data before and after sync
- **Checksums**: Calculate checksums for data integrity verification
- **Incremental Sync**: Only sync changed records (use last_modified timestamp)
- **Rollback on Failure**: Rollback entire batch if any record fails
- **Sync Status Tracking**: Track sync status per record, retry failed records
- **Manual Sync Trigger**: Allow manual sync retry from UI
- **Offline Mode Protection**: Mark transactions as "pending sync" until confirmed

#### Implementation

```python
# Example: Batch sync with checkpoints
def sync_batch(records, batch_size=100):
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        try:
            sync_records(batch)
            mark_synced(batch)
        except Exception as e:
            log_sync_error(batch, e)
            raise  # Stop sync on error
```

---

### 6. Staff & Scheduling Data Integrity

#### Problem: Schedule/Attendance Mismatches

- Clock-in without schedule → overtime calculations break
- Overlapping shifts → multiple staff on same table
- Task tracking incomplete → reports inaccurate

#### Solutions

- **Schedule Validation**: Require schedule before allowing clock-in
- **Shift Conflict Detection**: Prevent overlapping assignments
- **Automatic Schedule Creation**: Auto-create schedule if missing (with alert)
- **Attendance Validation**: Validate clock-in against schedule, flag discrepancies
- **Task Completion Tracking**: Require task completion before shift end
- **Data Completeness Checks**: Validate all required fields before saving
- **Manager Approval**: Require manager approval for schedule exceptions
- **Audit Logging**: Log all schedule and attendance changes

#### Implementation

```python
# Example: Schedule validation
def clock_in(staff_id, timestamp):
    schedule = get_schedule(staff_id, timestamp.date())
    if not schedule:
        raise NoScheduleError("No schedule found for this date")
    if timestamp < schedule.shift_start - timedelta(minutes=15):
        raise EarlyClockInError("Too early to clock in")
    # Proceed with clock-in
```

---

### 7. POS Transaction Errors

#### Problem: Sales Data Corruption

- Keyboard hotkey misfires → wrong quantities
- Barcode scanner misreads → wrong items
- Offline mode conflicts → duplicates or lost sales
- Split payment bugs → money disappears

#### Solutions

- **Input Validation**: Validate all inputs (quantities, prices, items) before transaction
- **Confirmation Dialogs**: Require confirmation for large quantities or high-value items
- **Barcode Validation**: Verify scanned barcode exists in database before adding to cart
- **Transaction Locking**: Lock transaction during payment processing
- **Receipt Verification**: Print receipt immediately, store transaction ID
- **Offline Transaction Queue**: Queue offline transactions, validate before sync
- **Duplicate Detection**: Check for duplicate transactions (same timestamp, same items)
- **Payment Reconciliation**: Reconcile payments daily, flag discrepancies
- **Audit Trail**: Log all transaction changes with user and timestamp

#### Implementation

```python
# Example: Transaction validation
def process_transaction(items, payment):
    # Validate items
    for item in items:
        if item.quantity <= 0:
            raise InvalidQuantityError("Quantity must be positive")
        if not product_exists(item.product_id):
            raise InvalidProductError("Product not found")
    
    # Validate payment
    total = sum(item.subtotal for item in items)
    if payment.amount != total:
        raise PaymentMismatchError("Payment amount doesn't match total")
    
    # Process transaction
    transaction = create_transaction(items, payment)
    return transaction
```

---

### 8. Inventory Calculation Errors

#### Problem: Negative Stock & Miscalculations

- Stock going negative due to simultaneous updates
- Recipe calculations incorrect
- Waste logging not applied
- Manual adjustments not logged

#### Solutions

- **Stock Reservation**: Reserve stock when order created, deduct when completed
- **Atomic Stock Updates**: Use database transactions for all stock changes
- **Negative Stock Prevention**: Check stock before deduction, prevent negative values
- **Recipe Validation**: Validate recipe quantities before allowing order
- **Waste Validation**: Require waste reason and approval for large amounts
- **Adjustment Logging**: Log all manual adjustments with reason and approver
- **Stock Reconciliation**: Daily stock reconciliation with physical counts
- **Alert System**: Alert when stock goes below reorder level or negative

#### Implementation

```python
# Example: Atomic stock update
def update_stock(ingredient_id, quantity_change, reason):
    with db.transaction():
        current = get_stock(ingredient_id)
        new_stock = current + quantity_change
        if new_stock < 0:
            raise NegativeStockError("Stock cannot go negative")
        update_stock_value(ingredient_id, new_stock)
        log_stock_movement(ingredient_id, quantity_change, reason)
```

---

### 9. Reporting & Aggregation Errors

#### Problem: Report Inaccuracies

- Aggregated tables wrong → reports don't match POS
- Pre-aggregation triggers slow system
- Cloud vs local data mismatch

#### Solutions

- **Reconciliation Reports**: Compare aggregated data with source data daily
- **Incremental Aggregation**: Update aggregates incrementally, not full recalculation
- **Background Processing**: Run aggregations in background, don't block UI
- **Data Validation**: Validate aggregated data against source before displaying
- **Cache Invalidation**: Invalidate cache when source data changes
- **Report Timestamps**: Show data freshness timestamp on all reports
- **Manual Refresh**: Allow manual report refresh with progress indicator
- **Error Reporting**: Log aggregation errors, alert administrators

#### Implementation

```python
# Example: Incremental aggregation
def update_daily_sales_summary(date):
    # Only process new transactions since last aggregation
    last_updated = get_last_aggregation_time(date)
    new_transactions = get_transactions_since(date, last_updated)
    update_summary(date, new_transactions)
    set_last_aggregation_time(date, now())
```

---

### 10. User Authentication & Session Issues

#### Problem: Auth & Permission Failures

- Multiple device logins → permission conflicts
- Role misconfiguration → unauthorized access
- Password storage issues → security breaches

#### Solutions

- **Session Management**: Track active sessions, limit concurrent logins per user
- **Device Registration**: Register devices, require re-auth on new device
- **Role Validation**: Validate permissions on every operation, not just login
- **Password Security**: Use bcrypt with proper salt, never store plaintext
- **Session Timeout**: Auto-logout after inactivity (15-30 minutes)
- **Audit Logging**: Log all authentication attempts and permission checks
- **Permission Testing**: Test all roles, ensure proper access control

#### Implementation

```python
# Example: Session management
def login(username, password, device_id):
    user = authenticate(username, password)
    # Check existing sessions
    active_sessions = get_active_sessions(user.id)
    if len(active_sessions) >= MAX_CONCURRENT_SESSIONS:
        raise TooManySessionsError("Maximum concurrent sessions reached")
    # Create new session
    session = create_session(user.id, device_id)
    return session
```

---

### 11. Hardware Integration Failures

#### Problem: Hardware Malfunctions

- Printer fails → receipts not printed
- Scanner misbehaves → orders slow
- Cash drawer doesn't open → checkout chaos
- Device ID conflicts

#### Solutions

- **Hardware Detection**: Detect hardware on startup, alert if missing
- **Fallback Options**: Provide manual alternatives (manual entry if scanner fails)
- **Error Handling**: Graceful degradation when hardware unavailable
- **Hardware Testing**: Test hardware in setup wizard, validate before use
- **Device ID Management**: Generate unique device IDs, prevent conflicts
- **Hardware Status Monitoring**: Monitor hardware status, alert on failures
- **Retry Logic**: Retry hardware operations with exponential backoff
- **User Notifications**: Notify users when hardware issues detected

#### Implementation

```python
# Example: Hardware fallback
def print_receipt(transaction):
    try:
        printer.print(transaction)
    except PrinterError:
        # Fallback: save to PDF or show on screen
        save_receipt_pdf(transaction)
        show_receipt_on_screen(transaction)
        alert_user("Printer unavailable, receipt saved to PDF")
```

---

### 12. Windows-Specific Issues

#### Problem: Windows Platform Problems

- DPI scaling fails → UI unreadable
- Firewall blocks sync → EOD fails
- Registry corruption → app crashes
- Service failures → sync never happens

#### Solutions

- **DPI Awareness**: Mark application as DPI-aware in manifest
- **Firewall Configuration**: Auto-configure firewall rules during installation
- **Registry Backup**: Backup registry keys before modification
- **Service Monitoring**: Monitor Windows service, auto-restart on failure
- **Error Logging**: Comprehensive Windows event log integration
- **Installation Validation**: Validate installation after setup wizard
- **Compatibility Testing**: Test on multiple Windows versions (10, 11)
- **User Permissions**: Request proper permissions during installation

#### Implementation

```python
# Example: DPI awareness
# In application manifest or code
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)  # System DPI aware
```

---

### 13. Multi-Device Sync Conflicts

#### Problem: Sync Deadlocks & Data Loops

- Real-time updates cause deadlocks
- Peer-to-peer sync creates loops
- Partial failures corrupt data

#### Solutions

- **Sync Locking**: Use distributed locks (file-based or database) for sync operations
- **Sync Ordering**: Establish sync order (device priority) to prevent loops
- **Conflict Resolution UI**: Simple, fast conflict resolution interface
- **Sync Status Dashboard**: Show sync status for all devices
- **Automatic Retry**: Auto-retry failed syncs with exponential backoff
- **Sync Validation**: Validate data after sync, rollback if invalid
- **Sync Logging**: Comprehensive sync logging for troubleshooting

#### Implementation

```python
# Example: Sync locking
def sync_with_lock(device_id):
    lock_file = f"sync_lock_{device_id}.lock"
    if os.path.exists(lock_file):
        raise SyncInProgressError("Sync already in progress")
    try:
        create_lock_file(lock_file)
        perform_sync(device_id)
    finally:
        remove_lock_file(lock_file)
```

---

### 14. Implementation & Deployment Risks

#### Problem: Development & Deployment Issues

- Over-engineering MVP → nothing works
- Python version mismatches → app won't run
- Installer failures → users can't install

#### Solutions

- **MVP First**: Build minimal viable product, add features incrementally
- **Version Pinning**: Pin Python and library versions in requirements.txt
- **Testing**: Comprehensive testing (unit, integration, end-to-end)
- **Staged Rollout**: Test on small group before full deployment
- **Rollback Plan**: Maintain ability to rollback to previous version
- **Installation Testing**: Test installer on clean Windows machines
- **Documentation**: Comprehensive user and developer documentation
- **Monitoring**: Monitor application health, alert on errors

#### Implementation

```python
# Example: Version checking
def check_python_version():
    import sys
    if sys.version_info < (3, 9):
        raise PythonVersionError("Python 3.9+ required")
```

---

### 15. Human Error & Process Issues

#### Problem: User Mistakes Amplify System Issues

- Staff ignore system → inventory wrong
- Managers override numbers → conflicts
- Floor staff ignore assignments → chaos

#### Solutions

- **User Training**: Comprehensive training for all staff roles
- **Process Documentation**: Clear procedures for common tasks
- **Validation & Confirmation**: Require confirmation for critical operations
- **Audit Trails**: Track all user actions for accountability
- **Error Messages**: Clear, actionable error messages
- **Help System**: Context-sensitive help and tooltips
- **Regular Audits**: Regular data audits to catch errors early
- **Manager Oversight**: Require manager approval for overrides

---

### General Best Practices

1. **Comprehensive Logging**: Log everything (errors, warnings, info, debug)
2. **Error Handling**: Never fail silently, always log and notify
3. **Data Validation**: Validate all inputs at every layer
4. **Transaction Safety**: Use transactions for all multi-step operations
5. **Backup Strategy**: Regular automated backups (daily at minimum)
6. **Monitoring**: Monitor system health, alert on anomalies
7. **Testing**: Test all scenarios, especially edge cases
8. **Documentation**: Document all processes and procedures
9. **User Feedback**: Collect user feedback, iterate based on issues
10. **Incremental Development**: Build incrementally, test frequently

---

## Security Considerations

- Password hashing (bcrypt/argon2)
- Role-based access control (RBAC)
- Audit logging for sensitive operations
- Data encryption at rest (cloud)
- Secure API communication (HTTPS)
- Session management
- Input validation and sanitization

---

## Future Enhancements

**Note**: All future enhancements should follow a phased approach. Prioritize based on business value and user feedback. Don't attempt to implement everything at once.

### Phase 6+ Features (Incremental Rollout)

- Mobile app for managers
- Customer loyalty app
- Online ordering integration
- Delivery management
- Multi-currency support
- Multi-language support
- Advanced analytics with ML
- Predictive inventory management
- Integration with accounting software
- Email/SMS notifications
- **Multi-Device Sync**: Full support for multiple POS terminals with real-time synchronization
- **Peer-to-Peer Sync**: Direct terminal-to-terminal sync on local network
- **Advanced Conflict Resolution**: Three-way merge, conflict visualization, and resolution UI
- **Performance Optimization**: Pre-aggregated tables for high-volume reporting
- **Customizable Hotkeys**: User-configurable keyboard shortcuts per role

### Implementation Strategy

- **MVP First**: Get core functionality working before adding advanced features
- **User Feedback**: Gather feedback after each phase before moving to next
- **Performance Monitoring**: Monitor system performance before adding resource-intensive features
- **Incremental Testing**: Test each feature thoroughly before adding the next
- **Documentation**: Document each feature as it's added
