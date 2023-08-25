FROM python:alpine

WORKDIR /app

COPY requirements.txt requirements.txt
COPY setup.sh setup.sh
COPY src/getWeather.py getWeather.py
COPY initdb.sql initdb.sql
COPY config.ini config.ini

RUN apk add --no-cache bash

CMD /bin/sh setup.sh
