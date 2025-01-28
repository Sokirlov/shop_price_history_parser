FROM python:3.12-slim
LABEL authors="sokirlov"

WORKDIR /app
COPY . /app
RUN sudo apt update && sudo apt install google-chrome-stable -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
