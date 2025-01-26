FROM python:3.13.1-bookworm AS base

ENV TZ Asia/Shanghai

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install --with-deps

CMD ["python", "/app/main.py"]
