# 第一阶段：构建阶段
FROM python:3.9 as builder
WORKDIR /build

# 安装构建所需依赖项
RUN apt-get update && apt-get install -y libgcc1
RUN pip install flask markdown oss2 requests chardet cryptography Flask-CORS

# 复制应用代码
COPY . .

# 第二阶段：运行阶段
FROM python:3.9-slim as runner
WORKDIR /app

# RUN echo "https://mirrors.163.com/alpine/v3.18/main/" > /etc/apk/repositories

# 安装运行所需依赖项
# RUN apk update && apk add libgcc
RUN apt-get update && apt-get install -y libgcc1

COPY . .
COPY --from=builder /build/*.py .
COPY --from=builder /build/templates .
COPY --from=builder /build/files .
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

ENV STATIC_DOMAIN=http://static.example.com

# 暴露端口
EXPOSE 5000

# 定义启动命令
CMD ["python", "app.py"]

