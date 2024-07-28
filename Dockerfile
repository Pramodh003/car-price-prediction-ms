FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev
WORKDIR /auth
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8001
CMD ["uvicorn", "models.main:app", "--host", "0.0.0.0", "--port", "8001"]