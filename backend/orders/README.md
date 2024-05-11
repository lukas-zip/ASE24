# User Service

## Overview
The Order Service is a microservice used to manage orders. Through it users create orders, add/remove items to/from cart   

## Architecture
The documentation of the code is provided in the following wiki: http://localhost:63342/ASE24/docs/user_service/build/html/index.html?_ijt=lb94n4s57l5ph68rmh859d12sq&_ij_reload=RELOAD_ON_SAVE

This service is built using Flask. It is designed to be scalable and efficient, utilizing AWS services such as DynamoDB and S3 for data handling and storage.

### Directory Structure
```

```

## Getting Started

### Prerequisites
- Python 3.8 or newer
- Docker and Docker compose

### Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/lukas-zip/ASE24.git
   cd backend/orders-service
   ```

2. Start the individual microservice using Docker Compose:
   ```bash
   docker-compose up --build
   ```

### Example Login Data
Below you will find example login data which can be used for testing and demonstration purposes. 

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


## Testing
To run the tests, execute the command (after starting the user-service):
   ```bash
   docker-compose exec user-service pytest
   ```