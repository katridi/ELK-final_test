FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY *.py /app/
COPY ./elastic_schemas /app/elastic_schemas


USER root
RUN echo 'alias movie="python /app/app.py"' >> ~/.bashrc


CMD ["bash"]