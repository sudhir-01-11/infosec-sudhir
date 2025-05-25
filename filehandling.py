import json
import os

DATA_FILE = "todo.json"

def load_tasks():
    if not os.path.isfile(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def create_user(tasks):
    username = input("Enter username to add: ").strip()
    if username in tasks:
        print("This user already exists!")
    else:
        tasks[username] = []
        print(f"User '{username}' has been created.")
        save_tasks(tasks)

def add_new_task(tasks):
    username = input("Enter username: ").strip()
    if username not in tasks:
        print("User not found.")
        return
    task_desc = input("Describe the task: ").strip()
    tasks[username].append({"task": task_desc, "completed": False})
    print("New task added successfully.")
    save_tasks(tasks)

def display_tasks(tasks):
    username = input("Enter username to view tasks: ").strip()
    if username not in tasks:
        print("No such user found.")
        return
    if not tasks[username]:
        print("No tasks assigned.")
        return
    print(f"\nTasks for {username}:")
    completed_count = 0
    for idx, item in enumerate(tasks[username], 1):
        status = "Completed" if item['completed'] else "Pending"
        if item['completed']:
            completed_count += 1
        print(f"{idx}. {item['task']} [{status}]")
    print(f"Completed {completed_count} out of {len(tasks[username])} tasks.")

def mark_task_completed(tasks):
    username = input("Enter username: ").strip()
    if username not in tasks:
        print("User not found.")
        return
    if not tasks[username]:
        print("No tasks available to update.")
        return
    print("\nCurrent tasks:")
    for i, task in enumerate(tasks[username], 1):
        status = "Completed" if task['completed'] else "Pending"
        print(f"{i}. {task['task']} [{status}]")
    try:
        choice = int(input("Select task number to mark as completed: "))
        if 1 <= choice <= len(tasks[username]):
            tasks[username][choice - 1]['completed'] = True
            print("Task updated to completed.")
            save_tasks(tasks)
        else:
            print("Selection out of range.")
    except ValueError:
        print("Please enter a valid number.")

def remove_task(tasks):
    username = input("Enter username: ").strip()
    if username not in tasks:
        print("User not found.")
        return
    if not tasks[username]:
        print("No tasks to remove.")
        return
    print("\nTasks list:")
    for idx, task in enumerate(tasks[username], 1):
        status = "Completed" if task['completed'] else "Pending"
        print(f"{idx}. {task['task']} [{status}]")
    try:
        task_no = int(input("Enter task number to delete: "))
        if 1 <= task_no <= len(tasks[username]):
            removed_task = tasks[username].pop(task_no - 1)
            print(f"Task '{removed_task['task']}' has been removed.")
            save_tasks(tasks)
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input, enter a number.")

def main():
    tasks = load_tasks()

    while True:
        print("\n===== To-Do Application Menu =====")
        print("1. Create User")
        print("2. Add Task")
        print("3. View Tasks")
        print("4. Mark Task Completed")
        print("5. Delete Task")
        print("6. Exit")
        option = input("Select an option: ").strip()

        if option == '1':
            create_user(tasks)
        elif option == '2':
            add_new_task(tasks)
        elif option == '3':
            display_tasks(tasks)
        elif option == '4':
            mark_task_completed(tasks)
        elif option == '5':
            remove_task(tasks)
        elif option == '6':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
