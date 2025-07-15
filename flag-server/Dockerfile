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

# Create sensitive files
RUN mkdir -p /app/secrets && \
    echo "master_admin_password=SuperSecretPassword123!" > /app/secrets/admin.txt

# Create non-root user
RUN useradd -m -s /bin/bash ctfuser && \
    chmod 755 /app && \
    chmod -R 600 /app/secrets && \
    chown -R ctfuser:ctfuser /app

USER ctfuser

EXPOSE 8080

CMD ["python", "app.py"] 