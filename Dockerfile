FROM python:3.7-buster
LABEL maintainer="Luan Mai"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apt-get update && \
    pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./*.py /app/

RUN python -m pytest
RUN useradd -ms /bin/bash user

USER user
