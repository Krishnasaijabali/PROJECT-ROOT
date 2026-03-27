# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY app.py .
COPY data ./data

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]