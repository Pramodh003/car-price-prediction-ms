FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev
WORKDIR /predict
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "predict.consumer"]

