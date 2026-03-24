#!/bin/bash

LOG_FILE="../logs/provisioning.log"

echo "=== Installing Nginx ===" | tee -a $LOG_FILE

# בדיקה אם Nginx כבר מותקן
if command -v nginx > /dev/null 2>&1; then
    echo "Nginx is already installed." | tee -a $LOG_FILE
    exit 0
fi

# סימולציה של התקנה
echo "Simulating installation of Nginx..." | tee -a $LOG_FILE
sleep 2
echo "Nginx installed successfully!" | tee -a $LOG_FILE
exit 0