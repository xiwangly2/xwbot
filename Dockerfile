FROM python:3.13.1-bookworm AS base

ENV TZ=Asia/Shanghai

WORKDIR /app

COPY . /app

# 根据架构选择性安装
RUN arch=$(uname -m) && \
    if [ "$arch" = "x86_64" ] || [ "$arch" = "aarch64" ]; then \
        # 主流架构安装完整依赖
        pip install --no-cache-dir -r requirements.txt && \
        pip install --no-cache-dir pytest-playwright~=0.6.2 && \
        playwright install --with-deps; \
    else \
        # 非主流架构（ppc64le/s390x）排除 psycopg2
        grep -v "psycopg2" requirements.txt | pip install --no-cache-dir -r /dev/stdin; \
    fi

CMD ["python", "/app/main.py"]
