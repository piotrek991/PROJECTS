FROM python:3.11.1-bullseye as linux-base

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
      sudo \
      curl \
      vim \
      unzip \
      rsync \
      openjdk-11-jdk \
      build-essential \
      software-properties-common \
      ssh \
      chromium && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app
WORKDIR /app

COPY requirements/requirements.txt .
RUN pip3 install -r requirements.txt
RUN playwright install







