FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    postgresql-server-dev-all \
    gcc \
    python3-dev

RUN python -m pip install --upgrade pip wheel setuptools

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app


RUN chmod +x /app/start.sh