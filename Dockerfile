# 使用官方Python运行时作为父镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src/ .

# 暴露端口
EXPOSE 8080

# 设置环境变量
ENV PYTHONPATH=/app

# 运行应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]