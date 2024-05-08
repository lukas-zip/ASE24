# Review

## Description
The review service is designed to handle the adding and removing of reviews to products in the e-commerce shop. Besides adding and deleting a review for a product, a customer can also edit reviews that she/he previously made. 

## Architecture
This service is built using Python-Flask. By using DynamoDB from AWS for the data storage, the service is scalable and performant and procides a felxible data model.
The following describes the structure of the review-service:

```
review/
│
├── app/                      # Application code
│   ├── __init__.py           # Create the app
│   ├── dummydata_reviews.py  # Script to generate dummy data
│   ├── dynamodb_reviews.py   # DynamoDB integration
│   └── routes_reviews.py     # API routes
│
├── tests/                    # Test cases for the microservice
│   ├── __init__.py           # 
│   ├── conftest.py           # Creation of the test client
│   └── review_test.py        # Test cases 
│
├── Dockerfile                # Dockerfile for building the service
├── README.md                 # README file
├── requirements.txt          # Dependencies that have to be installed
└── run.py                    # Entry point to run the Flask application
```

## API Documentation
All API available in the application are documented in the additional document "API-calls".

## Getting Started

### Requriements
The requirements are installed by running the run.py with referce to the requirements.txt.
Docker must be running on the system.
To use the full capacity of the microservice, the user-service must run as descibed in the README.md of the services.

### Starting the Application
1. Change the path to the review folder
```
cd backend/reviews
```
2. Build the docker container for the single service
```
docker-compose build reviews
```
3. Start the individual microservice using Docker
```
docker-compose up reviews
```

## Testing
1. To start the tests for the review-service the test-container has to be created and started:
```
docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up -d
```
2. To start the test of the service run followong command:
```
docker-compose logs --tail=1000 -f reviews
```