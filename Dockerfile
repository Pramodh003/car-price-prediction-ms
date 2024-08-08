FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8001
