FROM python:3.9.5-slim-buster

RUN apt-get update \
  && apt-get -y install gcc vim antiword \
  && apt-get clean

# Set working directory for all following in container commands
WORKDIR /usr/src/app

# Handle all necessary dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

ARG AZURE_KEY
ARG AZURE_ENDPOINT
ARG DEBUG

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV AZURE_KEY ${AZURE_KEY}
ENV AZURE_ENDPOINT ${AZURE_ENDPOINT}
ENV DEBUG ${DEBUG}

# Realistically, everything above this point should be cached on 90% of builds

# Install App
COPY . .

# make the ingest directory
RUN mkdir /usr/src/app/ingest