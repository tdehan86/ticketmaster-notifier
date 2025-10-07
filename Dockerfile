FROM python:3.11-slim

# Install system dependencies (including cron)
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create log file
RUN touch /var/log/notif-show.log

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY main.py .
COPY .env .

# Copy and configure crontab
COPY crontab /etc/cron.d/notif-show-cron
RUN chmod 0644 /etc/cron.d/notif-show-cron && \
    crontab /etc/cron.d/notif-show-cron

# Copy entry script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run entry script
CMD ["/entrypoint.sh"]
