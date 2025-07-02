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
    echo "CTF{1ns3cur3_d3s1gn_fl4w_2024}" > /app/secrets/design_flag.txt && \
    echo "CTF{vuln3r4bl3_c0mp0n3nts_2024}" > /app/secrets/components_flag.txt && \
    echo "CTF{1nt3gr1ty_f41lur3_2024}" > /app/secrets/integrity_flag.txt && \
    echo "CTF{l0gg1ng_m0n1t0r1ng_2024}" > /app/secrets/monitoring_flag.txt && \
    echo "master_admin_password=SuperSecretPassword123!" > /app/secrets/admin.txt

# Create non-root user
RUN useradd -m -s /bin/bash ctfuser && \
    chmod 755 /app && \
    chmod -R 600 /app/secrets && \
    chown -R ctfuser:ctfuser /app

USER ctfuser

EXPOSE 8080

CMD ["python", "app.py"] 