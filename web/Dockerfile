FROM python:3.10

RUN apt-get update && apt-get install -y openssl

RUN mkdir /ssl

RUN openssl req -x509 -newkey rsa:4096 -keyout /ssl/key.pem -out /ssl/cert.pem -days 365 -nodes -subj '/CN=localhost'

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

COPY . .