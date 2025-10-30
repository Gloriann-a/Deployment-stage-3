import os
import time
import re
import json
import requests
from collections import deque

# --- Load environment variables ---
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ERROR_RATE_THRESHOLD = float(os.getenv("ERROR_RATE_THRESHOLD", 2))
WINDOW_SIZE = int(os.getenv("WINDOW_SIZE", 200))
ALERT_COOLDOWN_SEC = int(os.getenv("ALERT_COOLDOWN_SEC", 300))
LOG_PATH = os.getenv("LOG_PATH", "/var/log/nginx/access.log")
MAINTENANCE_MODE = os.getenv("MAINTENANCE_MODE", "false").lower() == "true"

# --- State tracking ---
last_alert_time = 0
last_active_pool = None
recent_statuses = deque(maxlen=WINDOW_SIZE)

def post_to_slack(message: str):
    """Send alert message to Slack."""
    payload = {"text": message}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"[WARN] Failed to send Slack message: {e}")

def detect_failover(pool):
    """Detects change in pool (blue ↔ green)."""
    global last_active_pool
    if last_active_pool and pool != last_active_pool:
        post_to_slack(f":arrows_counterclockwise: Failover detected! {last_active_pool} → {pool}")
    last_active_pool = pool

def detect_high_error_rate():
    """Calculates rolling error rate and alerts if threshold exceeded."""
    global last_alert_time
    if not recent_statuses:
        return
    total = len(recent_statuses)
    errors = sum(1 for s in recent_statuses if s.startswith("5"))
    error_rate = (errors / total) * 100

    if error_rate > ERROR_RATE_THRESHOLD:
        now = time.time()
        if now - last_alert_time > ALERT_COOLDOWN_SEC:
            post_to_slack(f":rotating_light: High error rate detected! ({error_rate:.2f}% over last {total} requests)")
            last_alert_time = now

def tail_log():
    """Tails Nginx log file and monitors entries."""
    print(f"[INFO] Watching log file: {LOG_PATH}")
    with open(LOG_PATH, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue

            # Example log line fields (adjust regex if needed)
            match = re.search(r'pool=(\w+).*status=(\d+)', line)
            if match:
                pool, status = match.groups()
                detect_failover(pool)
                recent_statuses.append(status)
                detect_high_error_rate()

if __name__ == "__main__":
    if MAINTENANCE_MODE:
        print("[INFO] Maintenance mode active. Alerts suppressed.")
    else:
        print("[INFO] Starting log watcher...")
        tail_log()