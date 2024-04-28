#!/bin/bash

<<<<<<< HEAD
# Run tests for each service, except main service
pytest services/user-service/
pytest services/product-catalogue-service/

# Run tests for main service
docker build -t user-service -f ./services/user_service/Dockerfile ./services/user_service
docker build -t product-catalogue-service -f ./services/product_catalogue_service/Dockerfile ./services/product_catalogue_service

docker-compose -f docker-compose.test.yml up -d
docker-compose logs --tail=1000 -f user-service
docker-compose logs --tail=1000 -f product-catalogue-service
docker-compose down
=======
docker-compose -f docker-compose.test.yml up -d
docker-compose logs --tail=1000 -f user-service
docker-compose down

# Exit on any error
#set -e
# An array of your service directories
#SERVICES=(user-service)
# Loop through the services and run pytest
#for SERVICE in "${SERVICES[@]}"; do
 #   echo "Running tests for $SERVICE"
    # Navigate to the service directory
  #  cd "backend/$SERVICE"
    # Optionally, you might want to activate a virtual environment here
    # source venv/bin/activate
    # Install the requirements if not already installed
    # pip install -r requirements.txt
    # Run pytest
   # pytest
    # Navigate back to the root directory
   # cd - > /dev/null
#done
#echo "All tests completed."

>>>>>>> db66721aeb71cd451fdc4baf6e3063d5286478cd
