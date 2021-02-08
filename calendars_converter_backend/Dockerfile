# pull official base image
FROM python:3.8.6-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /usr/share/man/man1/
RUN apt update -y && apt install default-jre -y

# install dependencies
RUN pip install --upgrade pip setuptools wheel
COPY . .
RUN pip install -r requirements.txt

CMD pip install -r requirements.txt && gunicorn --bind 0.0.0.0:5000 main:app
