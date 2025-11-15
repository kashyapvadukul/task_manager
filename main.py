import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Failed to read tasks file: {e}")
        return []


def save_tasks(tasks):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"⚠️  Failed to save tasks file: {e}")
        return False


def display_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    print("\nCurrent Tasks:")
    print("-" * 70)
    for t in tasks:
        print(f"Index : {t['index']}")
        print(f"Title : {t['title']}")
        print(f"Desc  : {t.get('description','')}")
        print(f"Priority: {t.get('priority','Medium')}")
        print(f"Status: {t.get('status','pending')}")
        print(f"Due   : {t.get('due_date','N/A')}")
        print("-" * 70)
    print()


def get_next_index(tasks):
    if not tasks:
        return 1
    return max(t["index"] for t in tasks) + 1


def validate_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty. Try again.")


def input_date(prompt):
    while True:
        s = input(prompt + " (YYYY-MM-DD) or leave empty: ").strip()
        if s == "":
            return ""
        try:
            datetime.strptime(s, "%Y-%m-%d")
            return s
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def input_priority():
    while True:
        priority = input("Priority (High/Medium/Low): ").strip().capitalize()
        if priority in ("High", "Medium", "Low"):
            return priority
        print("Invalid priority. Please enter High, Medium, or Low.")


def add_task(tasks):
    print("\n==============================")
    print("        ADD NEW TASK")
    print("==============================")
    title = validate_nonempty("Task Name: ")
    description = input("Description: ").strip()
    priority = input_priority()
    due_date = input_date("Due Date")

    task = {
        "index": get_next_index(tasks),
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }

    tasks.append(task)
    if save_tasks(tasks):
        print("✅ Task added and saved.")
    else:
        print("❌ Failed to save task.")


def find_task_by_index(tasks, idx):
    for t in tasks:
        if t["index"] == idx:
            return t
    return None


def input_index(tasks, action_name="select"):
    if not tasks:
        print("No tasks available.")
        return None
    while True:
        try:
            s = input(f"Enter task index to {action_name} (or 'c' to cancel): ").strip()
            if s.lower() == "c":
                return None
            idx = int(s)
            task = find_task_by_index(tasks, idx)
            if task:
                return task
            print("Invalid index. Try again.")
        except ValueError:
            print("Please enter a numeric index.")


def update_task(tasks):
    print("\nUpdate Task")
    display_tasks(tasks)
    task = input_index(tasks, "update")
    if not task:
        print("Update canceled.")
        return
    print(f"Updating Task #{task['index']} - {task['title']}")
    new_title = input(f"New title (leave empty to keep: {task['title']}): ").strip()
    if new_title:
        task["title"] = new_title
    new_desc = input(f"New description (leave empty to keep): ").strip()
    if new_desc:
        task["description"] = new_desc
    new_priority = input(f"New priority (High/Medium/Low) [current: {task.get('priority','Medium')}]: ").strip().capitalize()
    if new_priority in ("High", "Medium", "Low"):
        task["priority"] = new_priority
    new_due = input_date(f"New due date (current: {task.get('due_date','N/A')})")
    if new_due != "":
        task["due_date"] = new_due
    new_status = input(f"New status [pending/done] (current: {task.get('status','pending')}): ").strip().lower()
    if new_status in ("pending", "done"):
        task["status"] = new_status
    if save_tasks(tasks):
        print("✅ Task updated and saved.")
    else:
        print("❌ Failed to save updates.")


def delete_task(tasks):
    print("\nDelete Task")
    display_tasks(tasks)
    task = input_index(tasks, "delete")
    if not task:
        print("Delete canceled.")
        return
    confirm = input(f"Are you sure you want to delete task #{task['index']}? (y/N): ").strip().lower()
    if confirm == "y":
        tasks.remove(task)
        if save_tasks(tasks):
            print("✅ Task removed and saved.")
        else:
            print("❌ Failed to save after deletion.")
    else:
        print("Deletion aborted.")


def view_tasks(tasks):
    print("\nView Tasks")
    display_tasks(tasks)


def show_menu():
    print("\n" + "=" * 40)
    print("Task Manager")
    print("=" * 40)
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")
    print("=" * 40)


def main():
    tasks = load_tasks()
    while True:
        show_menu()
        choice = input("Select an option [1-5]: ").strip()
        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            update_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Exiting application. Goodbye 👋")
            break
        else:
            print("Invalid choice. Choose between 1 and 5.")


if __name__ == "__main__":
    main()
