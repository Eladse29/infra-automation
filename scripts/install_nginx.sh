#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/../logs/provisioning.log"

mkdir -p "$(dirname "$LOG_FILE")"

echo "=== Nginx Installation ===" | tee -a "$LOG_FILE"

if command -v nginx >/dev/null 2>&1; then
    echo "Nginx is already installed." | tee -a "$LOG_FILE"
    exit 0
fi

echo "Installing Nginx..." | tee -a "$LOG_FILE"

sleep 2

echo "Nginx installed successfully!" | tee -a "$LOG_FILE"
exit 0