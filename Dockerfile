FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /bot

COPY . /bot/

RUN pip install --no-cache-dir -r data/requirements.txt