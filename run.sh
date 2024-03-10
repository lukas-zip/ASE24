#!/bin/bash

docker build -t user-service -f ./services/user_service/Dockerfile ./services/user_service
docker build -t product-catalogue-service -f ./services/product_catalogue_service/Dockerfile ./services/product_catalogue_service

docker-compose down
docker-compose up