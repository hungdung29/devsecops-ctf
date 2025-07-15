FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create vulnerable files directory
RUN mkdir -p /app/data && \
    echo "secret_key_12345" > /app/data/encryption_key.txt && \
    echo "CTF{cr4pt0_f41lur3_3xp0s3d_2025}" > /app/data/secret_flag.txt

# Create non-root user but keep file permissions loose
RUN useradd -m -s /bin/bash ctfuser && \
    chmod 755 /app && \
    chmod -R 644 /app/data && \
    chown -R ctfuser:ctfuser /app

USER ctfuser

EXPOSE 5004

CMD ["python", "app.py"] 