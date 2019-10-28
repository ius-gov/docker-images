FROM python:3.8

WORKDIR /data

COPY ./bannedversions.json /data/
COPY ./versionchecker.py /data/
COPY ./requirements.txt /data

RUN pip install -r requirements.txt

