# Use the official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Expose the port
EXPOSE 8080

# Run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]


