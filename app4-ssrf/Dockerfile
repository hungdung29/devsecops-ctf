FROM python:3.9-slim

WORKDIR /app

# Install system dependencies including tools that can be exploited
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    wget \
    netcat-traditional \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create vulnerable configuration files
RUN mkdir -p /app/config && \
    echo "admin_api_key=internal_secret_api_key_789" > /app/config/api.conf && \
    echo "database_url=postgresql://admin:supersecret@postgres:5432/internal_db" > /app/config/db.conf && \
    echo "CTF{ssrf_4nd_m1sc0nf1g_5}" > /app/config/flag.txt

# Create non-root user
RUN useradd -m -s /bin/bash ctfuser && \
    chmod 755 /app && \
    chmod -R 644 /app/config && \
    chown -R ctfuser:ctfuser /app

USER ctfuser

EXPOSE 5005

CMD ["python", "app.py"] 