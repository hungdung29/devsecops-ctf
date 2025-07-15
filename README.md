# OWASP Top 10 CTF Challenge 2025

Welcome to the OWASP Top 10 CTF Challenge! This is a comprehensive Capture The Flag (CTF) environment designed for software security workshops and educational purposes.

## 🎯 Overview

This CTF environment contains multiple vulnerable web applications that demonstrate the OWASP Top 10 vulnerabilities. Each application focuses on specific vulnerability types and provides hands-on experience with common web security issues.

## 🏗️ Architecture

The environment consists of:

- **4 Vulnerable Web Applications**
- **2 Database Services** (MySQL, PostgreSQL)
- **1 Internal Flag Server**
- **1 Nginx Reverse Proxy**

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- At least 2GB of available RAM
- Basic knowledge of web application security

### Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd ctf-2025
```

2. Start the environment:

```bash
docker-compose up -d
```

3. Wait for all services to be ready (about 2-3 minutes)

4. Access the applications:

```
http://localhost           - Main dashboard
http://localhost/injection/ - SQL/Command injection
http://localhost/access/   - Access control vulnerabilities
http://localhost/crypto/   - Cryptographic failures
http://localhost/ssrf/     - SSRF and misconfigurations
```

### Stopping the Environment

```bash
docker-compose down
```

## 🎪 Applications & Vulnerabilities

### 1. Injection Vulnerabilities (`/injection/`)

**OWASP A03: Injection**

- **Port**: 5001 (via `/injection/`)
- **Database**: MySQL
- **Vulnerabilities**:
  - SQL Injection (Login bypass, Data extraction)
  - Command Injection (Network tools)

### 2. Broken Access Control (`/access/`)

**OWASP A01: Broken Access Control**

- **Port**: 5003 (via `/access/`)
- **Database**: PostgreSQL
- **Vulnerabilities**:
  - Missing Function Level Access Control (Admin panel access)
  - Directory Traversal (File access)
  - Insecure API Endpoints

**Test Accounts**:

- `employee1 / password123`
- `employee2 / qwerty456`

### 3. Cryptographic Failures (`/crypto/`)

**OWASP A02: Cryptographic Failures**

- **Port**: 5004 (via `/crypto/`)
- **Vulnerabilities**:
  - Weak Hashing Algorithms (MD5)
  - Predictable Random Number Generation

### 4. SSRF & Security Misconfiguration (`/ssrf/`)

**OWASP A05: Security Misconfiguration & A10: Server-Side Request Forgery**

- **Port**: 5005 (via `/ssrf/`)
- **Vulnerabilities**:
  - Server-Side Request Forgery (SSRF)
  - Internal Service Access

## 🛠️ Tools & Techniques

### Common Attack Techniques

1. **SQL Injection**:

   ```sql
   admin' OR '1'='1' --
   admin' --
   ```

2. **Command Injection**:

   ```bash
   127.0.0.1; cat /proc/version
   127.0.0.1 && env
   ```

3. **Path Traversal**:

   ```
   ../secrets/flag.txt
   ../../etc/passwd
   ```

4. **SSRF Payloads**:

   ```
   http://flag-server:8080/flags
   http://flag-server:8080/admin
   ```

5. **MD5 Hash Cracking**:
   ```bash
   # Use external tools like hashcat or online crackers
   # The admin password is a common word + 1-3 digits
   hashcat -m 0 -a 3 <hash> ?l?l?l?l?l?l?l?d?d?d
   ```

### Special Attack Notes

- **Access Control Bypass**: Admin panel is accessible without proper role checking
- **Path Traversal**: File viewer accepts `?file=` parameter vulnerable to directory traversal
- **Rate Limiting**: Crypto app has rate limiting on hash attempts - use external tools
- **Random Prediction**: Random numbers are seeded with time rounded to 30-second intervals
- **Internal Network**: Flag server only accessible from internal Docker network

## 📚 Learning Resources

### OWASP Top 10 2021 Coverage

This CTF environment covers the following OWASP Top 10 categories:

1. **A01** - Broken Access Control ✅ (Access app)
2. **A02** - Cryptographic Failures ✅ (Crypto app)
3. **A03** - Injection ✅ (Injection app)
4. **A04** - Insecure Design ⚪ (Internal flag server)
5. **A05** - Security Misconfiguration ✅ (SSRF app)
6. **A06** - Vulnerable and Outdated Components ⚪ (Internal flag server)
7. **A07** - Identification and Authentication Failures ❌ (Not implemented)
8. **A08** - Software and Data Integrity Failures ⚪ (Internal flag server)
9. **A09** - Security Logging and Monitoring Failures ⚪ (Internal flag server)
10. **A10** - Server-Side Request Forgery (SSRF) ✅ (SSRF app)

### Additional Resources

- [OWASP Top 10 Documentation](https://owasp.org/Top10/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP CheatSheet Series](https://cheatsheetseries.owasp.org/)

## 🚨 Security Warning

**⚠️ IMPORTANT**: This environment contains intentionally vulnerable applications.

- **DO NOT** deploy this in production environments
- **DO NOT** use these applications as templates for real projects
- **ONLY** use in isolated, controlled environments
- **ENSURE** proper network isolation when running

## 🐛 Troubleshooting

### Common Issues

1. **Services not starting**:

   ```bash
   docker-compose logs <service-name>
   ```

2. **Port conflicts**:

   - Check if port 80 is available (main access point)
   - Internal application ports (5001, 5003-5005, 8080) should not conflict as they're containerized
   - Modify `docker-compose.yml` if needed

3. **Database connection issues**:

   - Wait for databases to fully initialize (2-3 minutes)
   - Check database logs: `docker-compose logs mysql postgres`

4. **Permission issues**:
   ```bash
   sudo chown -R $USER:$USER .
   ```

### Resetting the Environment

To completely reset all data:

```bash
docker-compose down -v
docker-compose up -d
```

## 🤝 Contributing

This CTF environment is designed for educational purposes. If you find issues or want to contribute:

1. Create detailed bug reports
2. Suggest new vulnerability scenarios
3. Improve documentation
4. Add new challenge categories

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- [Manuel Wieser - @mwieser](https://github.com/mwieser)

---

**Happy Hacking! 🏴‍☠️**

Remember: The goal is to learn and understand these vulnerabilities so you can better defend against them in real applications.
