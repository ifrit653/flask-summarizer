# Use a lightweight Python image
FROM python:3.9-slim

# Set environment variables to avoid interactive prompts
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Set the working directory
WORKDIR /app

# Copy application code into the container
COPY . /app

# Install Flask and any other Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Expose the Flask port (default 5000)
EXPOSE 5000

# Use Gunicorn for production serving (better than Flask's built-in server)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
