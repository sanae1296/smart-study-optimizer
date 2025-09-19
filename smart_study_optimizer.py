import json
import random
from datetime import datetime
from pathlib import Path
try:
    from plyer import notification
except ImportError:
    print("plyer not installed. Run: pip install plyer")
    notification = None

# ---------- Data File ----------
DATA_FILE = "user_data.json"

# Create data file if it doesn't exist
if not Path(DATA_FILE).exists():
    with open(DATA_FILE, "w") as f:
        json.dump({"tasks": [], "logs": []}, f, indent=4)

# ---------- Logger ----------
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_task(task_name, duration_minutes):
    data = load_data()
    log_entry = {
        "task": task_name,
        "duration": duration_minutes,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data["logs"].append(log_entry)
    save_data(data)

# ---------- Study Scheduler ----------
def load_tasks():
    return load_data()["tasks"]

def add_task(task_name, estimated_minutes):
    data = load_data()
    data["tasks"].append({"name": task_name, "estimated_minutes": estimated_minutes})
    save_data(data)

def suggest_task(energy_level):
    tasks = load_tasks()
    if not tasks:
        return None
    tasks.sort(key=lambda t: t["estimated_minutes"])
    if energy_level <= 5:
        suitable_tasks = [t for t in tasks if t["estimated_minutes"] <= 20]
    else:
        suitable_tasks = tasks
    return random.choice(suitable_tasks) if suitable_tasks else random.choice(tasks)

# ---------- Notifier ----------
def send_notification(title, message):
    if notification:
        notification.notify(title=title, message=message, timeout=10)

# ---------- Main Program ----------
def main():
    print("=== Smart Study Optimizer ===")
    while True:
        print("\n1. Add a new task")
        print("2. Get a task suggestion")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Task name: ")
            duration = int(input("Estimated duration (minutes): "))
            add_task(name, duration)
            print(f"Task '{name}' added!")

        elif choice == "2":
            energy = int(input("Your energy level (1-10): "))
            task = suggest_task(energy)
            if task:
                print(f"Suggested task: {task['name']} ({task['estimated_minutes']} mins)")
                start = input("Start this task? (y/n): ").lower()
                if start == "y":
                    print("Task started... Press Enter when done")
                    input()
                    log_task(task["name"], task["estimated_minutes"])
                    send_notification("Task Completed!", f"You finished '{task['name']}'")
            else:
                print("No tasks available. Add some first!")

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
