# Use an official Python runtime as a parent image
FROM python:3.11-bookworm

# Ensures Python output is not buffered
ENV PYTHONUNBUFFERED 1

# Create the directory for the project
RUN mkdir /bazigaar
WORKDIR /bazigaar

# Copy requirements and install dependencies
COPY requirements.txt . 
RUN pip install psycopg2-binary --no-cache-dir
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the application with Django migrations
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
