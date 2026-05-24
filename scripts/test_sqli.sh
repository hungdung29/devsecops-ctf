#!/bin/bash

# test_sqli.sh
# Mục tiêu:
# - Gửi payload SQL Injection vào route /injection/login
# - Nếu response chứa CTF{...} hoặc FLAG CAPTURED thì chứng minh lỗi vẫn khai thác được
# - Khi đó script trả exit code 1 để làm pipeline FAIL

set -e

BASE_URL="${BASE_URL:-http://localhost:8080}"
TARGET_URL="$BASE_URL/injection/login"

echo "[*] Testing SQL Injection on: $TARGET_URL"

# Payload SQLi:
# username = admin' OR '1'='1' #
# Dấu # dùng để comment phần AND password = '...' phía sau trong MySQL
response=$(curl -s -X POST "$TARGET_URL" \
  --data-urlencode "username=admin' -- -" \
  --data-urlencode "password=test")

# Kiểm tra response có flag/proof hay không
if echo "$response" | grep -Eiq "CTF\{|FLAG CAPTURED|Login Successful"; then
  echo "[VULNERABLE] SQL Injection is exploitable."
  echo "$response" | grep -Eio "CTF\{[^< ]+\}|FLAG CAPTURED|Login Successful" || true
  exit 1
else
  echo "[OK] SQL Injection payload did not expose admin/flag."
  exit 0
fi
