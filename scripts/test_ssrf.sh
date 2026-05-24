#!/bin/bash

# test_ssrf.sh
# Mục tiêu:
# - Gửi target_url trỏ tới flag-server nội bộ
# - Nếu response chứa CTF{...}, chứng minh SSRF vẫn khai thác được
# - Khi đó script trả exit code 1 để làm pipeline FAIL

set -e

BASE_URL="${BASE_URL:-http://localhost:8080}"
TARGET_URL="$BASE_URL/ssrf/proxy"
INTERNAL_FLAG_URL="http://flag-server:8080/flags"

echo "[*] Testing SSRF on: $TARGET_URL"
echo "[*] Internal target: $INTERNAL_FLAG_URL"

response=$(curl -s -X POST "$TARGET_URL" \
  --data-urlencode "target_url=$INTERNAL_FLAG_URL")

if echo "$response" | grep -Eiq "CTF\{|ssrf_flag"; then
  echo "[VULNERABLE] SSRF is exploitable."
  echo "$response" | grep -Eio "CTF\{[^\"< ]+\}|ssrf_flag" || true
  exit 1
else
  echo "[OK] SSRF payload did not expose internal flag."
  exit 0
fi
