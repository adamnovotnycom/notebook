FROM python:3.14

RUN mkdir -p /mnt/app
ADD . /mnt/app
WORKDIR /mnt/app

RUN pip install -r requirements.txt

EXPOSE 8888