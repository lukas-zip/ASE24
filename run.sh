#!/bin/bash

docker build -t ./backend/user-service/Dockerfile user-service:latest .
docker run -p 5000:5000 user-service

docker-compose build
docker-compose up