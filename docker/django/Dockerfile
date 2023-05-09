FROM python:3.10.10
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN apt-get update \
 && apt-get install -y uwsgi-plugin-python3 python3-dev default-libmysqlclient-dev build-essential default-mysql-client \
 && pip install --upgrade pip \
 && pip install -r requirements.txt
ADD . /code/