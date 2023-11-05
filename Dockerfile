# pull official base image
FROM python:3.12.0-bookworm

# set work directory
WORKDIR /usr/src/rest-api-pharmacy

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNTBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/src/rest-api-pharmacy/requirements.txt

# install requirements
RUN apt update && apt install -y python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /usr/src/rest-api-pharmacy/requirements.txt

# listen port for container
EXPOSE 8000

# copy project
COPY ./src /usr/src/rest-api-pharmacy/