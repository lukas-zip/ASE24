#!/bin/bash

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




# Run tests for each service, except main service
#pytest /backend/user-service/tests/
#pytest services/service_2/

# Run tests for main service
#docker build -t main-service -f ./services/main_service/docker-compose.test.yml ./services/main_service
#docker build -t service-1 -f ./services/service_1/docker-compose.test.yml ./services/service_1
#docker build -t service-2 -f ./services/service_2/docker-compose.test.yml ./services/service_2

