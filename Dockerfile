FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt ./
COPY setup.py ./
COPY README.md ./
COPY LICENSE ./
COPY tests ./
COPY instagram_to_discord ./

RUN apt-get update -y
RUN apt-get install -y git
RUN pip3 install -r requirements.txt
RUN python3 setup.py install
