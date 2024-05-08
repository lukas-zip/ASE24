# Financial Service

## Overview
The Financial Service is designed to handle payments and data management for our application. It interfaces with AWS DynamoDB for data storage and provides a Stripe integration.

## Architecture
The following is the directory structure of the Financial Service, outlining the primary components of the service:

### Directory Structure
```
financial-service/
│
├── app/ # Application code
│ ├── init.py # Initializes the Flask application
│ ├── dynamodb.py # Integrates with AWS DynamoDB for data operations
│ └── routes.py # Defines all the Flask routes for the financial endpoints
│
├── tests/ # Contains tests for the application
│ ├── __init__.py # Makes the directory a Python module
│ ├── conftest.py # Configurations for pytest
│ └── payment_test.py # Tests related to payment functionalities
│
├── Dockerfile # Docker configuration for building the service container
├── pytest.ini # Pytest configuration file
├── README.md # This README file
├── requirements.txt # Python package dependencies
└── run.py # Entry point to run the Flask application
```

## Getting Started

### Prerequisites
- Python 3.8 or newer
- Docker and Docker compose

### Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/lukas-zip/ASE24.git
   ```

2. As the financial service is dependent on other microservices like users, products and orders, we suggest executing the run.sh script in the ASE24 directory. This action initializes all services defined in docker-compose.yml.
   ```bash
   sh run.sh
   ```

## Testing
Similar for testing we suggest executing the test.sh script in the ASE24 directory.
   ```bash
   sh test.sh
   ```