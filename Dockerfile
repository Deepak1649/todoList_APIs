# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Apply database migrations
RUN python manage.py migrate

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]
