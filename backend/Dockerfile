FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 创建Spark jars目录并下载PostgreSQL JDBC驱动
RUN mkdir -p /opt/spark/jars && \
    wget -P /opt/spark/jars/ https://jdbc.postgresql.org/download/postgresql-42.6.0.jar || \
    echo "JDBC驱动下载失败，将使用psycopg2作为备选"

# 复制依赖文件并安装Python包
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY backend/ .

# 设置环境变量
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PYSPARK_PYTHON=python3
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]




