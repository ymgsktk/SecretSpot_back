FROM python:3.12.4

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
  libpq-dev \
  && pip install --upgrade pip \
  && pip install -r requirements.txt
