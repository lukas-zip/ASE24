# Dockerfile for user-service
FROM python:3.9

# Set working directory
WORKDIR /user_service

# Copy source code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8001

# Command to run the application
CMD ["python", "run.py"]
