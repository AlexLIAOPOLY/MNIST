FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install --upgrade pip && \
    pip install wheel setuptools && \
    pip install -r requirements.txt

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV MNIST_PRELOAD_DATA=1

# 暴露端口(Render会覆盖这个设置，使用PORT环境变量)
EXPOSE 8080

# 启动应用
CMD gunicorn --bind 0.0.0.0:$PORT app:app --log-file=- 