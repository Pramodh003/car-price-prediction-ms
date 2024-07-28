FROM python:3.9-slim

# Install dependencies and clean up
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the application code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Define entrypoint
ENTRYPOINT ["python", "-m", "predict.consumer"]

