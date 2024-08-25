# Use an official Python runtime as a parent image with Alpine
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    build-base \
    linux-headers \
    curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Generate pyproject.toml from requirements.txt and install dependencies
RUN poetry init --no-interaction \
    && poetry add $(cat requirements.txt) \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the project files
COPY . /app/

# Collect static files
RUN python mis/manage.py collectstatic --noinput

# Expose the port that the server will run on
EXPOSE 8001

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "mis.wsgi:application"]