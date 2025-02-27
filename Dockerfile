FROM python:3.13.2-bookworm AS base

ENV TZ=Asia/Shanghai

WORKDIR /app

COPY . /app

# 根据架构选择性安装
RUN arch=$(uname -m) && \
    apt update && \
    apt install libpq-dev -y && \
    if [ "$arch" = "x86_64" ] || [ "$arch" = "aarch64" ]; then \
        # 主流架构安装完整依赖
        pip install --no-cache-dir -r requirements.txt && \
        pip install --no-cache-dir playwright~=1.50.0 aisuite[all]~=0.1.10 docstring_parser~=0.16 && \
        playwright install --with-deps chromium; \
    else \
        if [ "$arch" = "s390x" ]; then \
            # 仅在 s390x 上排除 psycopg2
            grep -v "psycopg2-binary" requirements.txt | pip install --no-cache-dir -r /dev/stdin; \
        else \
            # 其他架构安装部分依赖 \
            pip install --no-cache-dir -r requirements.txt; \
        fi; \
    fi

CMD ["python", "/app/main.py"]
