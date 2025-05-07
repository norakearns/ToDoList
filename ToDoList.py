#!/usr/bin/env python
import sys
import tty
import termios
import json

class Task:
    def __init__(self, name: str, due_date: str, priority: int):
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.data_dict = self.make_json_entry()

    def describe(self):
        return f"Priority {self.priority}: {self.name}, Due: {self.due_date}"

    def make_json_entry(self):
        data_dict = {"name": self.name, "priority": self.priority, "due date": self.due_date}
        return data_dict

task1 = Task("sweep", "today", 1)
task2 = Task("mow", "tomorrow",3)

to_do_list = [task1, task2]
# Nora’s List Options: (A) add (D) delete (E) edit (L) list

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
    with open("data.json", "rt") as fh:
        data = json.load(fh)
        print(data)
        
if __name__ == "__main__":
    # read_from_json()
    running = True
    while running:
        print("Press the appropriate key\n" \
        "       (A) Add new task\n" \
        "       (E) Edit existing task\n" \
        "       (L) List all existing tasks\n" \
        "       (D) Delete existing task\n"\
        "       (Q) Quit program.")

        key = getch().lower()

        if key == "a":
            print("-----Add task-----")
            name = input("Add task name: ")
            due_date = input("Add task due date: ")
            priority = input("Add task priority (1-5): ")
            task = Task(name, due_date, int(priority))
            to_do_list.append(task)
            print(f"{name} has been added to your To Do list.")

        elif key == "e":
            print("Edit task:")

        elif key == "l":
            print("-----To Do List-----")
            for task in to_do_list:
                print(task.describe())

        elif key == "d":
            print("Delete task:")
            
        elif key == "q":
            # call write to JSON file
            write_to_json()
            running = False

        else:
            print("Invalid character entered")

