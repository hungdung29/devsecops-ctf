#!/bin/bash

# security_regression_tests.sh
# Mục tiêu:
# - Chạy toàn bộ security regression tests
# - Nếu bất kỳ test nào khai thác được lỗi, pipeline sẽ FAIL

set +e

echo "========================================"
echo " Running DevSecOps Security Tests"
echo "========================================"

failed=0

echo ""
echo "[1/2] SQL Injection test"
./scripts/test_sqli.sh
sqli_result=$?

if [ $sqli_result -ne 0 ]; then
  echo "[FAIL] SQL Injection vulnerability detected."
  failed=1
else
  echo "[PASS] SQL Injection test passed."
fi

echo ""
echo "[2/2] SSRF test"
./scripts/test_ssrf.sh
ssrf_result=$?

if [ $ssrf_result -ne 0 ]; then
  echo "[FAIL] SSRF vulnerability detected."
  failed=1
else
  echo "[PASS] SSRF test passed."
fi

echo ""
echo "========================================"

if [ $failed -ne 0 ]; then
  echo "Security regression tests FAILED."
  echo "At least one vulnerability is still exploitable."
  exit 1
else
  echo "Security regression tests PASSED."
  echo "No tested vulnerability was exploitable."
  exit 0
fi
