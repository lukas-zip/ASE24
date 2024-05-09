# User Service

## Overview
This inventory_management is a microservice that is designed to manage and administer all data related to products. It therefore handles insertions, deletions, updates etc. related matters with the help of a AWS localstack DynamoDb and S3 Bucket. This functionality is providing a API for product data operations.

## Architecture
This service is built with the use of a Flask backend technology. It is designed to be scalable and efficient, utilizing AWS Localstack services such as DynamoDB and S3 for product data handling and storage.

### Directory Structure
```
user-service/
│
├── app/                      # Application code
│   ├── __init__.py           # Initializes the Flask app
│   ├── dummydata.py          # Script to integrate dummy data
│   ├── dynamodb.py           # DynamoDB integration
│   ├── routes.py             # API routes
│   └── s3.py                 # S3 integration
│
├── dummydata/                # Contains JSON files for dummy data
│   └── products.json         # Dummy data for products
│
├── tests/                    # Test cases for the application
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   └── inventory_test.py     # Test cases for inventory_management
│
├── Dockerfile                # Dockerfile for building the service container
├── docker-compose.yml        # Composes the Docker user-service including LocalStack
├── README.md                 # This README file
├── requirements.txt          # Python package dependencies
└── run.py                    # Entry point to run the Flask application
```

## Getting Started

### Prerequisites
- Python 3.8 or newer
- Docker Deamon

### Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/lukas-zip/ASE24.git
   cd backend/inventory_management
   ```

2. Start the individual microservice using Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Testing
To run the tests, execute the command (after starting the user-service):
   ```bash
   docker-compose exec inventory_management pytest
   ```