FROM python:3-alpine

WORKDIR /server

COPY requirements.txt .

RUN ["pip", "install", "-r", "requirements.txt"]

COPY . .

ENV host=0.0.0.0
ENV port=80
EXPOSE 80

CMD [ "python", "server.py" ]