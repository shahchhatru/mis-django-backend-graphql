# Use an official Python runtime as a parent image
FROM python:3.12-slim AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the dependency files for caching
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Copy the rest of the application code
COPY . .

WORKDIR /app/mis
# Collect static files AFTER all dependencies and app files are present
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8001



# Command to run the application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8001", "mis.wsgi:application"]
