# User Service

## Overview
The User Service is a microservice designed to manage user data for our application. It handles tasks such as storing user information, integrating with AWS DynamoDB for data storage, and providing an API for user data operations.

## Architecture
This service is built using Flask. It is designed to be scalable and efficient, utilizing AWS services such as DynamoDB and S3 for data handling and storage.

### Directory Structure
```
user-service/
│
├── app/                      # Application code
│   ├── __init__.py           # Initializes the Flask app
│   ├── dummydata.py          # Script to generate dummy data
│   ├── dynamodb.py           # DynamoDB integration
│   ├── routes.py             # API routes
│   └── s3.py                 # S3 integration
│
├── dummydata/                # Contains JSON files for dummy data
│   ├── shops.json            # Dummy data for shops
│   └── users.json            # Dummy data for users
│
├── tests/                    # Test cases for the application
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   └── user_test.py          # Test cases for user operations
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
- Docker and Docker compose

### Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/lukas-zip/ASE24.git
   cd backend/user-service
   ```

2. Start the individual microservice using Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Testing
To run the tests, execute the command (after starting the user-service):
   ```bash
   docker-compose exec user-service pytest
   ```