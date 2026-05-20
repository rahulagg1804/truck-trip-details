#!/usr/bin/env bash
# Configure PythonAnywhere from your machine (needs API token).
# Usage:
#   export PA_API_TOKEN='your-token-from-pythonanywhere-account-page'
#   ./deploy/pa-remote-setup.sh

set -euo pipefail

USERNAME="${PA_USERNAME:-rahulagg1804}"
HOST="${PA_HOST:-www.pythonanywhere.com}"
DOMAIN="${PA_DOMAIN:-${USERNAME}.pythonanywhere.com}"
TOKEN="${PA_API_TOKEN:-}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -z "$TOKEN" ]]; then
  echo "Set PA_API_TOKEN from https://www.pythonanywhere.com/account/#api_token"
  exit 1
fi

API="https://${HOST}/api/v0/user/${USERNAME}"
AUTH=(-H "Authorization: Token ${TOKEN}")

api() {
  local method=$1 path=$2
  shift 2
  curl -fsS -X "$method" "${API}${path}" "${AUTH[@]}" "$@"
}

echo "==> Cloning repo and installing dependencies (always-on task, ~2 min)"
SETUP_CMD="cd ~ && ([ -d truck-trip-details ] || git clone https://github.com/rahulagg1804/truck-trip-details.git) && cd truck-trip-details && git pull origin main && cd backend && python3.10 -m venv venv && . venv/bin/activate && pip install -q --upgrade pip && pip install -q -r requirements.txt"
TASK_JSON=$(SETUP_CMD="$SETUP_CMD" python3 <<'PY'
import json, os
print(json.dumps({
    "command": f"bash -lc {json.dumps(os.environ['SETUP_CMD'])}",
    "description": "truck-trip-setup",
    "enabled": True,
}))
PY
)
TASK_ID=$(api POST /always_on/ -H "Content-Type: application/json" -d "$TASK_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "    Task id=${TASK_ID}, waiting for virtualenv..."
VENV_MARK="/home/${USERNAME}/truck-trip-details/backend/venv/bin/python"
for _ in $(seq 1 36); do
  sleep 10
  if api GET "/files/path${VENV_MARK}" >/dev/null 2>&1; then
    echo "    Setup finished."
    break
  fi
done
api DELETE "/always_on/${TASK_ID}/" >/dev/null 2>&1 || true

echo "==> Creating web app (manual config) if missing"
if ! api GET "/webapps/${DOMAIN}/" >/dev/null 2>&1; then
  api POST /webapps/ -F "domain_name=${DOMAIN}" -F "python_version=python310"
fi

echo "==> Configuring virtualenv"
api PATCH "/webapps/${DOMAIN}/" \
  -F "virtualenv_path=/home/${USERNAME}/truck-trip-details/backend/venv"

echo "==> Uploading WSGI file"
WSGI_PATH="/var/www/${USERNAME}_pythonanywhere_com_wsgi.py"
curl -fsS -X POST "${API}/files/path${WSGI_PATH}" "${AUTH[@]}" \
  -F "content=@${REPO_ROOT}/deploy/pythonanywhere_wsgi.py"

echo "==> Reloading web app"
api POST "/webapps/${DOMAIN}/reload/"

echo ""
echo "Done. Verify:"
echo "  curl -s https://${DOMAIN}/api/health/"
echo "  curl -sI -X OPTIONS https://${DOMAIN}/api/plan-trip/ -H 'Origin: https://rahulagg1804.github.io' -H 'Access-Control-Request-Method: POST' | grep -i access-control"
