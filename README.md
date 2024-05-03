# Vendor-Management-System
## Overview
The Vendor Management System is a web application designed to manage vendors and purchase orders efficiently.

## Features
- List and create vendors
- Retrieve, update, and delete vendors
- List and create purchase orders
- Retrieve, update, and delete purchase orders
- Calculate vendor performance metrics
- Acknowledge purchase orders
- Obtain authentication token for API access

## Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Swetha374/Vendor-Management-System.git
   cd Vendor-Management-System
2.Install dependencies:
   pip install -r requirements.txt
3.Database migrations:
   python manage.py makemigrations
   python manage.py migrate
4.Run the server:
   python manage.py runserver

Usage
Access the application:
   Open your web browser and navigate to http://localhost:8000.
Authentication:
   Before accessing protected endpoints, you need to obtain an authentication token. Send a POST request to http://localhost:8000/api/token/ with your username and password to obtain the token.
API Endpoints:
   Vendors:
   List all vendors: GET /api/vendors/
   Create a new vendor: POST /api/vendors/
   Retrieve a vendor by ID: GET /api/vendors/<vendor_id>/
   Update a vendor by ID: PUT /api/vendors/<vendor_id>/
   Delete a vendor by ID: DELETE /api/vendors/<vendor_id>/
   Purchase Orders:
   List all purchase orders: GET /api/purchase-orders/
   Create a new purchase order: POST /api/purchase-orders/
   Retrieve a purchase order by ID: GET /api/purchase-orders/<po_id>/
   Update a purchase order by ID: PUT /api/purchase-orders/<po_id>/
   Delete a purchase order by ID: DELETE /api/purchase-orders/<po_id>/
   Vendor Performance Metrics:
   Retrieve vendor performance metrics: GET /api/vendors/<vendor_id>/performance/
   Acknowledge Purchase Order:
   Acknowledge a purchase order: POST /api/purchase-orders/<po_id>/acknowledge/


## Authentication Token
The Vendor Management System uses token-based authentication to secure its API endpoints. To access protected endpoints, you need to obtain an authentication token by authenticating with your username and password.

### Obtaining an Authentication Token
To obtain an authentication token, you can send a POST request to the token obtain endpoint with your username and password, then will get token and send it using 'Token "token"'
