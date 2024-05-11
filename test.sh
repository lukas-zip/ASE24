#!/bin/bash

docker-compose -f docker-compose.test.yml up -d
docker-compose logs --tail=1000 -f user-service
docker-compose logs --tail=1000 -f inventory_management
docker-compose logs --tail=1000 -f reviews
docker-compose logs --tail=1000 -f financial-service
docker-compose logs --tail=1000 -f orders
docker-compose down
