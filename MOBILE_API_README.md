# Mobile Companion App API

## Overview

The Mobile Companion App provides both a mobile-optimized web interface and a REST API for native mobile app development.

## Mobile Web Interface

Access the mobile-optimized dashboard from the ERP by clicking "Mobile" in the sidebar. This provides a touch-friendly interface optimized for mobile devices.

## REST API

The REST API allows native mobile apps (iOS/Android) to integrate with the ERP system.

### Starting the API Server

```bash
python src/api/start_mobile_api.py
```

The API will be available at: `http://localhost:5000/api/mobile`

### API Endpoints

#### Health Check
- **GET** `/api/mobile/health`
- Returns API status

#### Orders
- **GET** `/api/mobile/orders` - Get recent orders
  - Query params: `limit` (default: 50), `status` (optional)
- **GET** `/api/mobile/orders/<id>` - Get order details
- **PUT** `/api/mobile/orders/<id>/status` - Update order status
  - Body: `{"status": "completed"}`

#### Products
- **GET** `/api/mobile/products` - Get products/menu items
  - Query params: `category` (optional), `active_only` (default: true)

#### Dashboard
- **GET** `/api/mobile/dashboard` - Get dashboard statistics

#### Inventory
- **GET** `/api/mobile/inventory/alerts` - Get low stock alerts

#### Staff
- **POST** `/api/mobile/staff/clock-in` - Clock in
  - Body: `{"staff_id": 1}`
- **POST** `/api/mobile/staff/clock-out` - Clock out
  - Body: `{"staff_id": 1}`

### Example Usage

```python
import requests

# Get orders
response = requests.get('http://localhost:5000/api/mobile/orders?limit=10')
orders = response.json()['orders']

# Update order status
response = requests.put(
    'http://localhost:5000/api/mobile/orders/123/status',
    json={'status': 'completed'}
)

# Clock in
response = requests.post(
    'http://localhost:5000/api/mobile/staff/clock-in',
    json={'staff_id': 1}
)
```

### Dependencies

For the API server, install:
```bash
pip install flask flask-cors
```

## Mobile App Development

You can use this API to build native mobile apps using:
- React Native
- Flutter
- Swift (iOS)
- Kotlin (Android)
- Or any framework that supports HTTP/REST APIs

The API uses standard JSON responses and follows RESTful conventions.

