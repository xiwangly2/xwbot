FROM python:3.13.2-bookworm AS base

ENV TZ=Asia/Shanghai

WORKDIR /app

COPY . /app

# 根据架构选择性安装
RUN arch=$(uname -m) && \
    if [ "$arch" = "x86_64" ] || [ "$arch" = "aarch64" ]; then \
        # 主流架构安装完整依赖
        pip install --no-cache-dir -r requirements.txt && \
        pip install --no-cache-dir pytest-playwright~=0.6.2 docstring_parser~=0.16 && \
        playwright install --with-deps chromium; \
    elif [ "$arch" = "arm" ]; then \
        apt update && \
        apt install -y gcc python3-dev libpq-dev && \
        apt-get clean && rm -rf /var/lib/apt/lists/* && \
        # 替换 psycopg[binary] 为 psycopg[c]
        sed -i 's/psycopg\[binary\]/psycopg\[c\]/' requirements.txt && \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        # 其他架构安装部分依赖
        pip install --no-cache-dir -r requirements.txt; \
    fi

CMD ["python", "/app/main.py"]