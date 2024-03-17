# ASE24
In a world in which consumers are more likely to want local suppliers and sustainable individualized products, we pursue building a platform that gives creative individuals, artists and small businesses an opportunity to sell their products of any kind. Mainly having in mind handcrafted products like jewelry, headbands, paintings, pottery and other accessories for individuals, their home, their loved ones and places their life takes place in. Consumers are able to sign up, browse through the products on offer, inspect and also buy them.

## Architecture

The system comprises various microservices: `user-service`, `product-service`, `xxx`, ... each with its distinct Dockerfile responsible for building a Docker image. These services also maintain their respective directories named app, housing `__init__.py`, `dynamodb.py`, and `routes.py`. Moreover, every service includes a `requirements.txt` file outlining its dependencies and a `run.py` file for initiating the service.

To coordinate the different services, a `docker-compose.yml` file in the ASE24 directory orchestrates their integration.

## Usage

To utilize this application, ensure Docker and Docker Compose are installed on your system. Once installed, follow these steps in order to run the microservice architecture:

1. Verify Docker and Docker Compose installation.
2. Open your terminal or command prompt and navigate to the ASE24 directory.
3. Execute the run.sh script by entering `sh run.sh`. This action initializes all services defined in `docker-compose.yml`.
4. Launch a web browser and go to http://localhost:3000 to access the frontend of the application.
