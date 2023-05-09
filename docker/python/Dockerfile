FROM python:3.9.16

COPY requirements.txt .

RUN apt-get update \
 && apt install -y locales \
 && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 \
 && python3 -m pip install --upgrade pip \
 && pip install -r requirements.txt

WORKDIR /code