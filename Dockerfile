FROM python:3.9-slim

# Install build dependencies for psycopg2
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev

# Create a user and set working directory
RUN useradd -ms /bin/bash pramodh
WORKDIR /home/pramodh

# Copy the entire auth directory and requirements.txt
COPY auth/ /home/pramodh/auth/
#COPY requirements.txt /home/pramodh/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /home/pramodh/auth/requirements.txt

# Change ownership
RUN chown -R pramodh:pramodh /home/pramodh

# Switch to the non-root user
USER pramodh

# Expose the port and specify the command to run
EXPOSE 8000
CMD ["uvicorn", "auth.main:app", "--host", "0.0.0.0", "--port", "8000"]

