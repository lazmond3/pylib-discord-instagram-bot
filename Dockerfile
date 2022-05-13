FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt ./
COPY README.md ./
COPY LICENSE ./
COPY tests ./
COPY instagram_to_discord ./instagram_to_discord/

RUN apt-get update -y
RUN apt-get install -y git ffmpeg
RUN pip3 install -r requirements.txt
CMD python3 -u -m instagram_to_discord
