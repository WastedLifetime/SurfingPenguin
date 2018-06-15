FROM python:3.6.5-slim
ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
WORKDIR /app/src
RUN pytest
