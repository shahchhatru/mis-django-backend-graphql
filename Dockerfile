# Use an official Python runtime as a parent image with Alpine
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apk update && apk upgrade && \
    apk add --no-cache gcc g++ musl-dev curl libffi-dev postgresql-dev \
    zlib-dev jpeg-dev freetype-dev linux-headers

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Convert requirements.txt to poetry format and install dependencies
RUN sed -e 's/==/>=/g' -e 's/$/,/g' requirements.txt > requirements_poetry.txt && \
    poetry init --no-interaction && \
    poetry add $(cat requirements_poetry.txt) && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the rest of the project files
COPY . /app/

# Collect static files (if needed)
RUN python mis/manage.py collectstatic --noinput

# Expose the port that the server will run on
EXPOSE 8001

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "mis.wsgi:application"]