FROM python:3.13.2-bookworm AS base

ENV TZ=Asia/Shanghai

WORKDIR /app

COPY . /app

# 根据架构选择性安装
RUN arch=$(uname -m) && \
    apt update && \
    apt install -y gcc python3-dev libpq-dev && \
    if [ "$arch" = "x86_64" ] || [ "$arch" = "aarch64" ]; then \
        # 主流架构安装完整依赖
        pip install --no-cache-dir -r requirements.txt && \
        pip install --no-cache-dir pytest-playwright~=0.6.2 docstring_parser~=0.16 aisuite[all]~=0.1.10 && \
        playwright install --with-deps chromium; \
    else \
        # 其他架构安装部分依赖 \
        pip install --no-cache-dir -r requirements.txt; \
    fi

CMD ["python", "/app/main.py"]
