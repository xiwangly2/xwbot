FROM python:3.13.1-bookworm AS base

ENV TZ Asia/Shanghai

WORKDIR /app

COPY . /app

# 设置镜像源，可选
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/app/main.py"]
