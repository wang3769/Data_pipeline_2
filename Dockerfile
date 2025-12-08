# Boilerplate Dockerfile for Python Application Containerization

# Stage 1: Base image
# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set metadata
LABEL maintainer="Your Name <your.email@example.com>"
LABEL description="Python application container"

# Set working directory inside container
WORKDIR /app

# Stage 2: Install system dependencies (if needed)
# Example: for build tools, database clients, etc.
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Stage 3: Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 4: Copy application code
COPY . .

# Stage 5: Set environment variables (optional)
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

# Stage 6: Expose port (if your app runs a service)
# EXPOSE 8000

# Stage 7: Define the entry point or default command
# Option A: Run a Python script
CMD ["python", "main.py"]

# Option B: Run a web server (e.g., Flask, FastAPI)
# CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Option C: Run bash shell for debugging
# CMD ["bash"]

# ============================================
# Quick Commands to Build and Run:
# ============================================
# Build the image:
#   docker build -t finiance-pipeline:1.0 . (note that " ." is important indicating current directory)
#
# Run the container:
#   docker run --rm finiance-pipeline:1.0
#
# Run with volume mount (for local development):
#   docker run --rm -v $(pwd):/app my-python-app:1.0
#
# Run interactively:
#   docker run --rm -it my-python-app:1.0 bash
#
# ============================================
