# Use the official Python 3.9 slim image as the base
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sqlite3 \
        vim \
        && rm -rf /var/lib/apt/lists/*

# Set the working directory to /workspace (to match the volume mount)
WORKDIR /workspace

# Install Python dependencies from requirements.txt (assume it exists in host mount)
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point to your Python script
CMD ["python", "main.py"]
