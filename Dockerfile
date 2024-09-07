FROM python:3.12-alpine3.20

RUN apk add postgresql-client build-base postgresql-dev
RUN adduser --disabled-password app_user

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt
RUN pip install --upgrade setuptools

COPY . /courses
WORKDIR /courses
EXPOSE 8000

USER app_user
