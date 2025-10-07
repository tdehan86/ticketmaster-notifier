#!/bin/bash

# Load environment variables into cron
printenv | grep -v "no_proxy" >> /etc/environment

# Start cron in the background
cron

# Display startup information
echo "Container started - Cron configured to run daily at 12:00 PM"
echo "Logs available at /var/log/notif-show.log"

# Initial execution on startup (optional - comment out if not desired)
echo "Initial execution..."
cd /app && python main.py

# Keep container alive by tailing the logs
tail -f /var/log/notif-show.log
