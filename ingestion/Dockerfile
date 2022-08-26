FROM python:3.8-slim-buster

WORKDIR /app

COPY ./ingestion/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./ingestion/*.py /app/

RUN mkdir /app/data

CMD [ "python", "/app/ingest.py" ]