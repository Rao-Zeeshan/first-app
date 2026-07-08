# Simple Todo List CLI App

A minimal command-line Todo List manager built in Python, using the `rich` library for nice terminal output. Tasks are stored locally in `tasks.json`.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Add a new task
python app.py add "Buy groceries"

# List all tasks
python app.py list

# Mark a task as done
python app.py done 1

# Delete a task
python app.py delete 1
```

## Background Reminder Daemon

`reminder_daemon.py` runs continuously in the background and periodically
checks `tasks.json` for pending tasks, sending a desktop notification
(or a console/log message if notifications aren't available).

```bash
# Run in foreground (for testing), checks every 60 seconds
python reminder_daemon.py --interval 60

# Default interval is 1800 seconds (30 minutes)
python reminder_daemon.py
```

### Running it in the background

**Linux / macOS (quick way, using nohup):**
```bash
nohup python3 reminder_daemon.py --interval 1800 > /dev/null 2>&1 &
```
Stop it later with:
```bash
pkill -f reminder_daemon.py
```

**Linux (proper way, using systemd — runs on boot, auto-restarts):**
1. Edit `todo-reminder.service` and replace `/path/to/todo_app` with your actual project path.
2. Copy it and enable the service:
```bash
sudo cp todo-reminder.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now todo-reminder.service
sudo systemctl status todo-reminder.service
```

**Windows (background, no terminal window):**
```bash
pythonw reminder_daemon.py --interval 1800
```
`pythonw` runs without opening a console window. To stop it, use Task Manager
and end the `pythonw.exe` process, or check `reminder.log` for activity.

Logs are always written to `reminder.log` in the project folder, so you can
confirm it's running even without notifications enabled.

## Project Structure

```
todo_app/
├── app.py                  # Main todo CLI application
├── reminder_daemon.py      # Background reminder daemon
├── todo-reminder.service   # systemd service file (Linux)
├── requirements.txt        # Dependencies
├── tasks.json              # Auto-created storage file (ignored in git)
├── reminder.log            # Auto-created log file (ignored in git)
└── README.md
```
