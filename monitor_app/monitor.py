import psutil
import time
import logging

# Configure logging to act as our Alerting mechanism for this demonstration
# In a full production environment, this would integrate with smtplib (Email) or webhooks (Slack/PagerDuty)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler("cpu_alerts.log"),
        logging.StreamHandler()  # Output to console as well
    ]
)

CPU_THRESHOLD = 80.0
CHECK_INTERVAL_SECONDS = 5


def monitor_cpu():
    logging.info(f"Starting CPU Monitor. Alert threshold set to {CPU_THRESHOLD}%")
    logging.info("Press CTRL+C to stop.")

    try:
        while True:
            # interval=1 blocks for 1 second to calculate the actual average usage
            cpu_usage = psutil.cpu_percent(interval=1)

            if cpu_usage > CPU_THRESHOLD:
                # Trigger alert
                logging.warning(f"CRITICAL ALERT: CPU usage exceeded threshold! Current usage: {cpu_usage}%")
            else:
                logging.info(f"CPU usage normal: {cpu_usage}%")

            time.sleep(CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")


if __name__ == "__main__":
    monitor_cpu()