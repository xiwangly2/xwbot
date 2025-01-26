FROM python:3.13.1-bookworm AS base

ENV TZ Asia/Shanghai

WORKDIR /app

COPY . /app

# 检查系统架构，如果是 x86_64 或 aarch64 则安装 playwright
RUN arch=$(uname -m) && \
    if [ "$arch" = "x86_64" ] || [ "$arch" = "aarch64" ] || [ "$arch" = "amd64" ] || [ "$arch" = "arm64" ]; then \
        pip install --no-cache-dir -r requirements.txt && \
        playwright install --with-deps; \
    else \
        pip install --no-cache-dir -r requirements.txt; \
    fi

CMD ["python", "/app/main.py"]
