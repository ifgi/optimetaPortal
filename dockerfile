#dockerfile
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#directory
WORKDIR /test

#install dependencies
COPY requirements.txt /test/

RUN pip install -r requirements.txt

COPY . /test/