# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy script and env
COPY main.py .
COPY .env .

# Install dependencies
RUN pip install slack_sdk python-dotenv

# Run the monitor script
CMD ["python", "main.py"]
