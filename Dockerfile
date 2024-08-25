# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Fix the requirements.txt file and install Python dependencies
RUN sed -i 's/>=2.8.6aniso8601==9.0.1/>=2.8.6\naniso8601==9.0.1/' requirements.txt \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /app/

# Collect static files (if needed)
RUN python mis/manage.py collectstatic --noinput

# Expose the port that the server will run on
EXPOSE 8001

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "mis.wsgi:application"]