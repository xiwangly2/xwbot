# 第一阶段：基础依赖（全架构通用）
FROM --platform=$BUILDPLATFORM python:3.13.1-bookworm as base
ENV TZ=Asia/Shanghai
WORKDIR /app

# 安装跨架构基础依赖
RUN apt update && \
    apt install -y --no-install-recommends \
    libpq5 \
    $(if [ "$(uname -m)" = "s390x" ]; then echo "python3-dev gcc"; fi) \
    && rm -rf /var/lib/apt/lists/*

# 第二阶段：架构适配构建阶段
FROM base as builder
COPY requirements.txt .

# 使用BuildKit缓存并处理架构差异
RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$TARGETARCH" = "s390x" ]; then \
        grep -v "psycopg2-binary" requirements.txt | pip install --no-cache-dir -r /dev/stdin; \
    else \
        pip install --no-cache-dir -r requirements.txt \
        && pip install --no-cache-dir pytest-playwright~=0.6.2; \
        && playwright install --with-deps chromium; \
    fi

# 最终阶段：生产镜像
FROM base as production
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY . /app

# 安装&架构特定清理
RUN playwright install --with-deps chromium; \
    if [ "$TARGETARCH" != "s390x" ]; then \
    apt purge -y python3-dev gcc && \
    apt autoremove -y; \
    fi && \
    rm -rf /var/lib/apt/lists/*

CMD ["python", "/app/main.py"]