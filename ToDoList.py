#!/usr/bin/env python
import sys
import tty
import termios
import json

to_do_list = []

class Task:
    def __init__(self, number: int, name: str, priority: int, due_date: str):
        self.number=number
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.data_dict = self.make_json_entry()

    def describe(self):
        return f"({self.number}) Task: {self.name} | Due: {self.due_date} | Priority: {self.priority}"

    def make_json_entry(self):
        data_dict = {"number": self.number, "name": self.name, "priority": self.priority, "due date": self.due_date}
        return data_dict

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def write_to_json():
    with open("data.json", "wt") as fh:
        entries = [task.data_dict for task in to_do_list]
        json.dump(entries, fh, indent=4)
    fh.close()

def read_from_json():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            for item in data:
                task = Task(number=item['number'], name=item['name'], due_date=item['due date'], priority=item['priority'])
                to_do_list.append(task)
    except FileNotFoundError:
        print("Error: File not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")

def get_optional_input(prompt: str, current_value: str):
    """
    If the user hits the return key, keep the current value for the task attribute.
    """
    new_value = input(str(prompt + "(current value is " + str(current_value) + ") :"))
    if new_value == '':
        return current_value
    else:
        return new_value

if __name__ == "__main__":
    read_from_json()
    running = True
    while running:
        print("Press the appropriate key\n" \
        "       (A) Add new task\n" \
        "       (E) Edit existing task\n" \
        "       (L) List all existing tasks\n" \
        "       (D) Delete existing task\n"\
        "       (Q) Save list and quit program\n"
        "       (X) Quit program without saving.")

        key = getch().lower()

        if key == "a":
            print("-----Add task-----")
            name = input("Add task name: ")
            due_date = input("Add task due date: ")
            priority = input("Add task priority (1-5): ")
            number = len(to_do_list) + 1
            task = Task(number, name, int(priority), due_date)
            to_do_list.append(task)
            print(f"{name} has been added to your To Do list.")

        elif key == "e":
            print("----Enter the # task to edit----")
            for task in to_do_list:
                print(task.describe())
            task_num = int(input("Task #: "))
            item_found = False
            for task in to_do_list:
                if task.number == task_num:
                    item_found = True
                    print(task.describe())
                    print("-----Edit task-----")
                    print("Hit RETURN to maintain current value")
                    task.name = get_optional_input("Edit task name: ", task.name)
                    task.due_date = get_optional_input("Edit task due date: ", task.due_date)
                    task.priority = get_optional_input("Edit task priority (1-5): ", task.priority)
                    break
            if item_found == False:
                print(f"Item {task_num} not found in list.")

        elif key == "l":
            print("-----To Do List-----")
            for task in to_do_list:
                print(task.describe())

        elif key == "d":
            print("----Enter the # task to delete----")
            for task in to_do_list:
                print(task.describe())
            task_num = int(input("Task #: "))
            item_deleted = False
            for task in to_do_list:
                if task.number == task_num:
                    to_do_list.remove(task)
                    item_deleted = True
                    break
            if item_deleted == False:
                print(f"Item {task_num} not found in list.")
            else:
                print("You have successfully deleted the task.")
            
        elif key == "q":
            # call write to JSON file
            write_to_json()
            running = False
        elif key == "x":
            running = False
        else:
            print("Invalid character entered")

