FROM python:3.10.10-slim-bullseye AS builder

ENV TZ Asia/Shanghai

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/app/main.py"]
