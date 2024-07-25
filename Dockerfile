FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev
WORKDIR /auth
COPY /auth/* /auth
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /auth/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "auth.main:app", "--host", "0.0.0.0", "--port", "8000"]

