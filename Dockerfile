FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create upload directories
RUN mkdir -p static/uploads/listings static/uploads/avatars

# Set environment
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Run migrations and start
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 app:app
