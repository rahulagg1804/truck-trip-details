#!/bin/bash
# Run in PythonAnywhere → Consoles → Bash

set -e
USERNAME="${PA_USERNAME:-rahulagg1804}"
REPO="https://github.com/rahulagg1804/truck-trip-details.git"

cd ~
if [ ! -d truck-trip-details ]; then
  git clone "$REPO"
fi
cd truck-trip-details
git pull origin main

cd backend
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Next steps in the Web tab:"
echo "1. Add web app → Manual config → Python 3.10"
echo "2. Virtualenv: /home/$USERNAME/truck-trip-details/backend/venv"
echo "3. WSGI: copy deploy/pythonanywhere_wsgi.py (set YOUR_USERNAME=$USERNAME)"
echo "4. Reload"
echo ""
echo "API: https://$USERNAME.pythonanywhere.com"
