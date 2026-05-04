import sys
import json
import os
args = sys.argv

# load tasks and create json file if it does not exist
def load_tasks():
    if not os.path.exists('tasks.json'):
        return []

    with open('tasks.json', 'r') as f:
        return json.load(f)
    

# save 
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        #serialize a python object into json format
        json.dump(tasks, f, indent=4) 


# adding tasks 
def add_task(description):
    tasks = load_tasks()

    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo"
    }

    tasks.append(new_task)
    save_tasks(tasks)

    print("Task added!")

# list my tasks 
def list_tasks(filter_status=None):
    tasks = load_tasks()

    for task in tasks:
        if filter_status and task["status"] != filter_status:
            continue

        print(f'{task["id"]}. {task["description"]} [{task["status"]}]')

# update my tasks 
def update_task(task_id, new_desc):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_desc

    save_tasks(tasks)

# delete tasks 
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]

    save_tasks(tasks)

# change task status 
def mark_status(task_id, status):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status

    save_tasks(tasks)

if __name__ == "__main__":
    command = sys.argv[1]

    if len(sys.argv) < 2:
        print("Please provide a command")

    if command == "add":
        add_task(sys.argv[2])

    elif command == "list":
        if len(sys.argv) > 2:
            list_tasks(sys.argv[2])
        else:
            list_tasks()

    elif command == "update":
        update_task(int(sys.argv[2]), sys.argv[3])

    elif command == "delete":
        delete_task(int(sys.argv[2]))

    elif command == "done":
        mark_status(int(sys.argv[2]), "done")

    elif command == "progress":
        mark_status(int(sys.argv[2]), "in-progress")



