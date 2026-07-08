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

## Project Structure

```
todo_app/
├── app.py             # Main application
├── requirements.txt   # Dependencies
├── tasks.json         # Auto-created storage file (ignored in git)
└── README.md
```
