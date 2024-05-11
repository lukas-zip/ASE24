# Orders Service

## Overview
The Order Service is a microservice used to manage orders. Through it users create orders, add/remove items to/from cart   

## Architecture
The documentation of the code is provided in the following wiki: http://localhost:63342/ASE24/docs/user_service/build/html/index.html?_ijt=lb94n4s57l5ph68rmh859d12sq&_ij_reload=RELOAD_ON_SAVE

This service is built using Flask. It is designed to be scalable and efficient, utilizing AWS services such as DynamoDB and S3 for data handling and storage.

### Directory Structure
```
orders
├── app  # Application code
│   ├── dynamodb_po.py  # Creates DynamoDB table to handle PO orders 
│   ├── dynamodb_users.py # Creates DynamoDB table to handle user orders 
│   ├── initialise_dynamo.py # Integrates with AWS DynamoDB for data operations
│   ├── __init__.py # Initializes the Flask application
│   ├── invoice.py #Handles invoice creation
│   ├── routes.py  # Defines all the Flask routes for the orders endpoints
│   └── utils.py #Helper functions 
├── docker-compose.yml # Composes the Docker orders-service including LocalStack
├── Dockerfile # Docker configuration for building the service container
├── pytest.ini # Pytest configuration file
├── README.md # This README file
├── requirements.txt # Python package dependencies
├── run.py  # Entry point to run the Flask application
└── tests
    ├── conftest.py # Configurations for pytest
    ├── __init__.py # Makes the directory a Python module
    ├── orders_dummy_data.py #Json files to compare orders reponse against
    ├── product_dummy_data.py #Dummy Product data
    ├── user_orders_test.py  # Tests related to orders functionalities
    └── utils.py #helper functions used by tests
```

## Getting Started

### Prerequisites
- Python 3.8 or newer
- Docker and Docker compose

### Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/lukas-zip/ASE24.git
   cd backend/orders
   ```

2. Start the individual microservice using Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Testing
To run the tests, execute the command (after starting the orders-service):
   ```bash
   docker-compose exec orders pytest
   ```