#FROM python:3.10.0

#WORKDIR /app

#COPY ./requirements.txt .

#RUN pip3 install boto3

#RUN pip3 install flask

#RUN pip3 install logging

#RUN pip3 install json

#RUN pip3 install localstack

#RUN pip3 install -r requirements.txt

#COPY . .

#CMD ["python3", "myfirstflask.py"]


# Use an official Node runtime as a parent image
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies
RUN npm install

RUN npm install axios

#RUN logging install

# Build the React app
RUN npm run build

# Expose the port the app runs on
EXPOSE 3000

# Serve the app
CMD ["npm", "start"]
