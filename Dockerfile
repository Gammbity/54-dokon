FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip

COPY . /app

RUN pip install -r requirements.txt

CMD ["python3.10", "manage.py", "runserver"]