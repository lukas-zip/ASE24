#!/bin/bash

docker-compose -f docker-compose.test.yml up -d
docker-compose logs --tail=1000 -f user-service
docker-compose down



# Exit on any error
#set -e
# An array of the service directories
#SERVICES=(user-service)
# Loop through the services and run pytest
#for SERVICE in "${SERVICES[@]}"; do
 #   echo "Running tests for $SERVICE"
    # Navigate to the service directory
    # cd "backend/$SERVICE"
    # Install the requirements if not already installed
    # pip install -r requirements.txt
    # Run pytest
   # pytest
    # Navigate back to the root directory
   # cd - > /dev/null
#done
#echo "All tests completed."
