# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.11-bookworm

# The enviroment Variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Get the Real World example app
#RUN git clone https://github.com/gothinkster/django-realworld-example-app.git /drf_src

# Set the working directory to /drf
# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.
RUN mkdir /bazigaar
WORKDIR /bazigaar

# Add ./requirements.txt /bazigaar-admin/

# Install any needed packages specified in requirements.txt
#RUN pip install -r requirements.txt
#ADD . /bazigaar-admin/
COPY requirements.txt .
RUN pip install psycopg2-binary --no-cache-dir
RUN pip install -r requirements.txt
COPY . .
#RUN apt install libpq-dev

#VOLUME /drf_src
# COPY . .
EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# CMD python manage.py makemigrations && python manage.py migrate && gunicorn -b 0.0.0.0:8000 configurations.wsgi:application

