# ASE24
In a world in which consumers are more likely to want local suppliers and sustainable individualized products, we pursue building a platform that gives creative individuals, artists and small businesses an opportunity to sell their products of any kind. Mainly having in mind handcrafted products like jewelry, headbands, paintings, pottery and other accessories for individuals, their home, their loved ones and places their life takes place in. Consumers are able to sign up, browse through the products on offer, inspect and also buy them.

## Wiki
User Service
   ```bash
   cd docs/user_service/build/html
   open index.html
   ```
Reviews
   ```bash
   cd docs/reviews/build/html
   open index.html
   ```
Inventory Management
   ```bash
   cd docs/inventory_management/build/html
   open index.html
   ```
Financial Service
   ```bash
   cd docs/financial_service/build/html
   open index.html
   ```

## Architecture

The system comprises various microservices: `user-service`, `inventory_management`, `orders`, `reviews` and `financial-service` each with its distinct Dockerfile responsible for building a Docker image. These services also maintain their respective directories named `app`, housing `__init__.py`, `dynamodb.py`  and `routes.py`. Moreover, every service includes a `requirements.txt` file outlining its dependencies and a `run.py` file for initiating the service. Additionally, each service includes a test folder to evaluate and test its functionalities.

To coordinate the different services, a `docker-compose.yml` file in the ASE24 directory orchestrates their integration.

## Tests

Tests are executable locally by entering `sh test.sh` in the console (ASE24 directory). This action triggers the `docker-compose.test.yml` file, launching the specified tests (make sure that all requirements are installed e.g. by running the application). Furthermore the tests are executed automatically by the CI pipeline (CircleCi) when new commits are pushed to github.
   ```bash
  sh test.sh
   ```

## Usage

To utilize this application, ensure Docker and Docker Compose are installed on your system. Once installed, follow these steps in order to run the microservice architecture:

1. Verify Docker and Docker Compose installation.
2. Open your terminal or command prompt and navigate to the ASE24 directory.
3. Execute the run.sh script by entering `sh run.sh`. This action initializes all services defined in `docker-compose.yml`.
   ```bash
   sh run.sh
   ```
4. Launch a web browser and go to http://localhost:3000 to access the frontend of the application.

### Example Login Data

1. Shops:
- Email: micro@example.com
- Password: password11

- Email: hydro@example.com
- Password: password22

- Email: electro@example.com
- Password: password33

2. Users:
- Email: john.doe@example.com
- Password: password1

- Email: jane.doe@example.com
- Password: password2

- Email: max.smith@example.com
- Password: password3


### Example Credit Card Details
Please visit https://docs.stripe.com/testing
or just use:
- Card number: 4242 4242 4242 4242
- Date: Any future data
- CVC: Any 3 digits
