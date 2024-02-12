import tkinter as tk
from tkinter import messagebox
import json

# Load existing tasks from file (if any)
try:
    with open("tasks.json", "r") as file:
        tasks = json.load(file)
except FileNotFoundError:
    tasks = []

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

def add_task():
    task_name = entry.get()
    if task_name:
        tasks.append({"name": task_name, "completed": False})
        listbox.insert(tk.END, task_name)
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Empty Task", "Task name cannot be empty!")

def mark_task_complete():
    selected_index = listbox.curselection()
    if selected_index:
        task_text = listbox.get(selected_index)
        if task_text.startswith("✓ "):
            task_text = task_text[2:]
        else:
            task_text = "✓ " + task_text
        listbox.delete(selected_index)
        listbox.insert(selected_index, task_text)
        task_number = selected_index[0]
        tasks[task_number]["completed"] = True
        listbox.itemconfig(task_number, {"bg": "#C0C0C0"})
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as complete.")

def delete_task():
    selected_index = listbox.curselection()
    if selected_index:
        task_number = selected_index[0]
        del tasks[task_number]
        listbox.delete(task_number)
        save_tasks()
        messagebox.showwarning("Warning", "Please select a task to delete.")
def select_day():
    selected_index = listbox.curselection()
    if selected_index:
        task_number = selected_index[0]
        task_text = listbox.get(task_number)
        if task_text.startswith("✓ "):
            task_text = task_text[2:]
        else:
            task_text = "✓ " + task_text
        listbox.delete(task_number)
        listbox.insert(task_number, task_text)
        tasks[task_number]["completed"] = not tasks[task_number]["completed"]
        listbox.itemconfig(task_number, {"bg": "#C0C0C0" if tasks[task_number]["completed"] else ""})
        save_tasks()
        days_button.pack_forget()
        days_button.pack(padx=30, pady=15)
        days_button.configure(state="normal")
        days_button.bind("<Button-1>", days)

def days(event):
    yl = [today_button, tomorrow_button, yesterday_button]
    today_button.pack_forget()
    today_button.pack(padx=30, pady=15)
    tomorrow_button.pack_forget()
    tomorrow_button.pack(padx=30, pady=15)
    yesterday_button.pack_forget()
    yesterday_button.pack(padx=30, pady=15)
    days_button.configure(state="enabled")
    days_button.insert(tk.END, "Today")
    
def switch_to_yesterday(event, days):
    save_tasks()

    # Clear the listbox and tasks for today
    listbox.delete(0, tk.END)
    tasks = []

    # Load tasks for yesterday
    load_tasks("yesterday.json")

    # Display tasks for yesterday
    display_tasks()
    
# Create main window
root = tk.Tk()
root.title("To-Do List")

# Create GUI elements
label = tk.Label(root, text="Task:")
label.pack(padx=10)

entry = tk.Entry(root, width=40)
entry.pack(padx=30, pady=15)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=4)

mark_button = tk.Button(root, text="Mark as Complete", command=mark_task_complete)
mark_button.pack(pady=4)

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack(pady=4)

day_button = tk.Button(root, text="Select day", command=select_day)
day_button.pack(padx=30, pady=15)

today_button = tk.Button(root, text="Today", command=days)
today_button.pack(padx=40, pady=60)
tomorrow_button = tk.Button(root, text="Tomorrow", command=days)
tomorrow_button.pack(padx=40, pady=60)
yesterday_button = tk.Button(root, text="Yesterday", command=days)
yesterday_button.pack(padx=40, pady=60)

listbox = tk.Listbox(root, selectbackground="#00C000", activestyle="none", width=80, height=30)
listbox.pack(padx=30, pady=15)

# Populate the listbox with existing tasks
for task in tasks:
    listbox.insert(tk.END, task["name"])
    if task["completed"]:
        listbox.itemconfig(listbox.size() - 1, {"bg": "#C0C0C0"})

root.mainloop()