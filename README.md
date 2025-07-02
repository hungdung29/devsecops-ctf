# OWASP Top 10 CTF Challenge 2024

Welcome to the OWASP Top 10 CTF Challenge! This is a comprehensive Capture The Flag (CTF) environment designed for software security workshops and educational purposes.

## 🎯 Overview

This CTF environment contains multiple vulnerable web applications that demonstrate the OWASP Top 10 vulnerabilities. Each application focuses on specific vulnerability types and provides hands-on experience with common web security issues.

## 🏗️ Architecture

The environment consists of:

- **5 Vulnerable Web Applications**
- **2 Database Services** (MySQL, PostgreSQL)
- **1 Redis Cache**
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

4. Access the main dashboard:

```
http://localhost
```

### Stopping the Environment

```bash
docker-compose down
```

## 🎪 Applications & Vulnerabilities

### 1. Injection Vulnerabilities (`/injection/`)

**OWASP A03: Injection**

- **Port**: 5001
- **Database**: MySQL
- **Vulnerabilities**:
  - SQL Injection (Error-based, Union-based, Blind)
  - Cross-Site Scripting (XSS)
  - Command Injection
  - NoSQL Injection

**Flags to Find**:

- `CTF{1nj3ct10n_m4st3r_2024}`
- `CTF{sql_1nj3ct10n_m4st3r_2024}`
- `CTF{bl1nd_sql1_n1nj4_2024}`
- `CTF{un10n_s3l3ct_h3r0_2024}`

### 2. Authentication Failures (`/auth/`)

**OWASP A07: Identification and Authentication Failures**

- **Port**: 5002
- **Database**: Redis
- **Vulnerabilities**:
  - Weak Password Policies
  - Brute Force Protection Bypass
  - Session Management Issues
  - JWT Vulnerabilities
  - Password Reset Flaws

**Default Credentials**:

- `admin / admin`
- `user1 / password`
- `john / 123456`
- `alice / alice123`

**Flags to Find**:

- `CTF{4uth_byp4ss_h4ck3r_2024}`
- `CTF{p4ssw0rd_r3s3t_vuln_2024}`
- `CTF{4dm1n_4cc3ss_gr4nt3d_2024}`

### 3. Broken Access Control (`/access/`)

**OWASP A01: Broken Access Control**

- **Port**: 5003
- **Database**: PostgreSQL
- **Vulnerabilities**:
  - Insecure Direct Object References (IDOR)
  - Privilege Escalation
  - Missing Function Level Access Control
  - Directory Traversal

**Flags to Find**:

- `CTF{4cc3ss_c0ntr0l_pwn3d_2024}`
- `CTF{m4st3r_4p1_k3y_3xp0s3d_2024}`
- `CTF{b4ckd00r_4cc3ss_gr4nt3d_2024}`

### 4. Cryptographic Failures (`/crypto/`)

**OWASP A02: Cryptographic Failures**

- **Port**: 5004
- **Vulnerabilities**:
  - Weak Encryption Algorithms
  - Hard-coded Encryption Keys
  - Insecure Random Number Generation
  - Hash Collision Attacks
  - Certificate Validation Issues

**Flags to Find**:

- `CTF{cr4pt0_f41lur3_3xp0s3d_2024}`
- `CTF{w34k_3ncr4pt10n_2024}`
- `CTF{h4rd_c0d3d_k3y_2024}`

### 5. SSRF & Security Misconfiguration (`/ssrf/`)

**OWASP A05: Security Misconfiguration & A10: Server-Side Request Forgery**

- **Port**: 5005
- **Vulnerabilities**:
  - Server-Side Request Forgery (SSRF)
  - Information Disclosure
  - Default Configurations
  - Unnecessary HTTP Methods
  - Verbose Error Messages

**Flags to Find**:

- `CTF{ssrf_4nd_m1sc0nf1g_2024}`
- `CTF{s3cur1ty_m1sc0nf1g_2024}`
- `CTF{1nf0rm4t10n_d1scl0sur3_2024}`

### 6. Internal Flag Server

**OWASP A04, A06, A08, A09: Design Flaws, Vulnerable Components, Integrity Failures, Logging Failures**

- **Port**: 8080 (Internal only)
- **Access**: Via SSRF or other internal access methods
- **Contains flags for**:
  - Insecure Design
  - Vulnerable and Outdated Components
  - Software and Data Integrity Failures
  - Security Logging and Monitoring Failures

## 🛠️ Tools & Techniques

### Recommended Tools

- **Burp Suite** or **OWASP ZAP** - Web application security scanner
- **SQLMap** - Automated SQL injection tool
- **Curl** - Command line HTTP client
- **Browser Developer Tools** - Built-in browser debugging
- **Postman** - API testing tool

### Common Attack Techniques

1. **SQL Injection**:

   ```sql
   ' OR '1'='1' --
   ' UNION SELECT 1,2,3,4 --
   ```

2. **XSS Payloads**:

   ```html
   <script>
     alert("XSS");
   </script>
   <img src=x onerror=alert('XSS')>
   ```

3. **Command Injection**:

   ```bash
   ; cat /etc/passwd
   && whoami
   ```

4. **SSRF Payloads**:
   ```
   http://localhost:8080/
   http://flag-server:8080/
   file:///etc/passwd
   ```

## 🎖️ Scoring

### Flag Format

All flags follow the format: `CTF{...}`

### Point Values

- **Easy Flags**: 100 points
- **Medium Flags**: 200 points
- **Hard Flags**: 300 points
- **Hidden Flags**: 500 points

### Total Available Points

- **25+ Flags** available across all applications
- **Maximum Score**: ~5000 points

## 📚 Learning Resources

### OWASP Top 10 2021

1. **A01** - Broken Access Control
2. **A02** - Cryptographic Failures
3. **A03** - Injection
4. **A04** - Insecure Design
5. **A05** - Security Misconfiguration
6. **A06** - Vulnerable and Outdated Components
7. **A07** - Identification and Authentication Failures
8. **A08** - Software and Data Integrity Failures
9. **A09** - Security Logging and Monitoring Failures
10. **A10** - Server-Side Request Forgery (SSRF)

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

   - Check if ports 80, 5001-5005, 8080 are available
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

Created for software security workshops and educational purposes.

---

**Happy Hacking! 🏴‍☠️**

Remember: The goal is to learn and understand these vulnerabilities so you can better defend against them in real applications.
