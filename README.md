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

## Authentication Token
The Vendor Management System uses token-based authentication to secure its API endpoints. To access protected endpoints, you need to obtain an authentication token by authenticating with your username and password.

### Obtaining an Authentication Token
To obtain an authentication token, you can send a POST request to the token obtain endpoint with your username and password, then will get token and send it using 'Token "token"'
