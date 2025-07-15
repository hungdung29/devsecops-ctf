FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    iputils-ping \
    nmap \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user (but make it vulnerable)
RUN useradd -m -s /bin/bash ctfuser && \
    chmod 755 /app && \
    chown -R ctfuser:ctfuser /app

USER ctfuser

# Set environment variable with flag for command injection challenge
ENV CMD_FLAG="CTF{c0mm4nd_1nj3ct10n_3nv_v4r5_2025}"

EXPOSE 5001

CMD ["python", "app.py"] 