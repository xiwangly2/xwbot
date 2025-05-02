FROM python:3.13.2-bookworm AS base
ARG TARGETARCH
ARG TARGETVARIANT

ENV TZ=Asia/Shanghai
WORKDIR /app
COPY . /app

RUN set -eux; \
    arch="$(uname -m)"; \
    case "$arch" in \
        x86_64|amd64) \
            echo "Installing full deps for x86_64…"; \
            pip install --no-cache-dir -r requirements.txt; \
            pip install --no-cache-dir pytest-playwright~=0.6.2 docstring_parser~=0.16; \
            playwright install --with-deps chromium \
            ;; \
        aarch64|arm64) \
            echo "Installing full deps for ARM64 (aarch64)…"; \
            pip install --no-cache-dir -r requirements.txt; \
            pip install --no-cache-dir pytest-playwright~=0.6.2 docstring_parser~=0.16; \
            playwright install --with-deps chromium \
            ;; \
        armv7*|armv6*|armhf) \
            echo "Installing minimal deps for 32-bit ARM ($arch)…"; \
            apt-get update; \
            apt-get install -y --no-install-recommends gcc python3-dev libpq-dev; \
            rm -rf /var/lib/apt/lists/*; \
            sed -i 's/psycopg\[binary\]/psycopg\[c\]/' requirements.txt; \
            pip install --no-cache-dir -r requirements.txt \
            ;; \
        *) \
            echo "Unknown arch ($arch), install only pure-Python deps…"; \
            pip install --no-cache-dir -r requirements.txt \
            ;; \
    esac

CMD ["python", "/app/main.py"]
