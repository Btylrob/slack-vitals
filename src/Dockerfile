
FROM python:3.11-slim

WORKDIR /app

COPY main.py .
COPY .env .

# Install dependencies
RUN pip install slack_sdk python-dotenv

CMD ["python", "main.py"]
