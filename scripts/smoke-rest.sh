#!/usr/bin/env bash
# Live CRUD smoke test: output is intentionally printed for assignment evidence.
set -euo pipefail

python server.py > /tmp/accounts-service.log 2>&1 &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT

for attempt in $(seq 1 20); do
  if curl -fsS http://127.0.0.1:8080/api/health >/dev/null; then
    break
  fi
  sleep 1
done
curl -fsS http://127.0.0.1:8080/api/health >/dev/null

echo
echo '=== CREATE ==='
echo '$ curl -sS -X POST http://127.0.0.1:8080/api/accounts -H "Content-Type: application/json" -d {"name":"Asha Patil","email":"asha@example.com"}'
CREATE_RESPONSE=$(curl -sS -w $'\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8080/api/accounts \
  -H 'Content-Type: application/json' \
  -d '{"name":"Asha Patil","email":"asha@example.com"}')
printf '%s\n' "$CREATE_RESPONSE"
ACCOUNT_ID=$(printf '%s\n' "$CREATE_RESPONSE" | sed '$d' | python -c 'import json,sys; print(json.load(sys.stdin)["id"])')

echo
echo '=== LIST ==='
echo '$ curl -sS http://127.0.0.1:8080/api/accounts'
curl -sS -w $'\nHTTP_STATUS:%{http_code}\n' http://127.0.0.1:8080/api/accounts

echo
echo '=== READ ==='
echo "$ curl -sS http://127.0.0.1:8080/api/accounts/$ACCOUNT_ID"
curl -sS -w $'\nHTTP_STATUS:%{http_code}\n' "http://127.0.0.1:8080/api/accounts/$ACCOUNT_ID"

echo
echo '=== UPDATE ==='
echo "$ curl -sS -X PUT http://127.0.0.1:8080/api/accounts/$ACCOUNT_ID -H Content-Type:application/json -d {\"name\":\"Asha P.\",\"email\":\"asha.p@example.com\"}"
curl -sS -w $'\nHTTP_STATUS:%{http_code}\n' -X PUT "http://127.0.0.1:8080/api/accounts/$ACCOUNT_ID" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Asha P.","email":"asha.p@example.com"}'

echo
echo '=== DELETE ==='
echo "$ curl -sS -X DELETE http://127.0.0.1:8080/api/accounts/$ACCOUNT_ID"
curl -sS -w $'\nHTTP_STATUS:%{http_code}\n' -X DELETE "http://127.0.0.1:8080/api/accounts/$ACCOUNT_ID"
