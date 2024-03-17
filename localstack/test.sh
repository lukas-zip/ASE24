#!/bin/bash

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