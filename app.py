"""
Todo Reminder Background Daemon
Periodically checks tasks.json for pending tasks and sends a desktop
notification (or logs to console/file if notifications aren't available).

Usage:
    python reminder_daemon.py               # checks every 30 minutes (default)
    python reminder_daemon.py --interval 60 # checks every 60 seconds
"""

import json
import os
import sys
import time
import signal
import logging
import argparse
from datetime import datetime

try:
    from plyer import notification
    HAS_NOTIFY = True
except ImportError:
    HAS_NOTIFY = False

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "reminder.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

running = True


def handle_stop(signum, frame):
    global running
    running = False
    logging.info("Stop signal received. Shutting down reminder daemon.")
    print("\nStopping reminder daemon...")


signal.signal(signal.SIGINT, handle_stop)
signal.signal(signal.SIGTERM, handle_stop)


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def send_notification(title, message):
    if HAS_NOTIFY:
        try:
            notification.notify(title=title, message=message, timeout=10)
            return
        except Exception as e:
            logging.warning(f"Desktop notification failed: {e}")

    # Fallback: print to console
    print(f"[REMINDER] {title}: {message}")


def check_tasks():
    tasks = load_tasks()
    pending = [t for t in tasks if not t.get("done")]

    if not pending:
        logging.info("No pending tasks.")
        return

    count = len(pending)
    titles = ", ".join(t["title"] for t in pending[:5])
    message = f"You have {count} pending task(s): {titles}"
    if count > 5:
        message += f" ...and {count - 5} more"

    send_notification("Todo Reminder", message)
    logging.info(f"Notified about {count} pending task(s).")


def main():
    parser = argparse.ArgumentParser(description="Todo Reminder Background Daemon")
    parser.add_argument(
        "--interval", type=int, default=1800,
        help="Check interval in seconds (default: 1800 = 30 minutes)"
    )
    args = parser.parse_args()

    logging.info(f"Reminder daemon started. Checking every {args.interval} seconds.")
    print(f"Reminder daemon running (interval: {args.interval}s). Press Ctrl+C to stop.")
    print(f"Logs are being written to: {LOG_FILE}")

    if not HAS_NOTIFY:
        print("Note: 'plyer' not installed, falling back to console-only reminders.")

    while running:
        check_tasks()
        # Sleep in small chunks so Ctrl+C is responsive
        slept = 0
        while slept < args.interval and running:
            time.sleep(min(1, args.interval - slept))
            slept += 1

    logging.info("Reminder daemon stopped.")
    print("Reminder daemon stopped.")


if __name__ == "__main__":
    main()
