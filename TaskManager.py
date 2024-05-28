import json
import tkinter as tk
from tkinter import messagebox, simpledialog

class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "Completada" if self.completed else "Pendiente"
        return f"{self.description} - {status}"

    def to_dict(self):
        return {"description": self.description, "completed": self.completed}

    @classmethod
    def from_dict(cls, task_dict):
        return cls(task_dict["description"], task_dict["completed"])

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def add_task(self, description):
        new_task = Task(description)
        self.tasks.append(new_task)
        self.save_tasks()

    def mark_task_as_completed(self, position):
        try:
            self.tasks[position].completed = True
            self.save_tasks()
        except IndexError:
            print("Error: posición de tarea no válida.")

    def delete_task(self, position):
        try:
            self.tasks.pop(position)
            self.save_tasks()
        except IndexError:
            print("Error: posición de tarea no válida.")

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            tasks_dict = [task.to_dict() for task in self.tasks]
            json.dump(tasks_dict, file, indent=4)

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                tasks_dict = json.load(file)
                return [Task.from_dict(task) for task in tasks_dict]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

class TaskApp:
    def __init__(self, root, task_manager):
        self.root = root
        self.root.title("Task Manager")
        self.task_manager = task_manager

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.task_listbox.pack(side=tk.LEFT, padx=10)
        self.update_task_listbox()

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_button = tk.Button(root, text="Agregar Tarea", command=self.add_task)
        self.add_button.pack(pady=5)

        self.complete_button = tk.Button(root, text="Marcar como Completada", command=self.complete_task)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Eliminar Tarea", command=self.delete_task)
        self.delete_button.pack(pady=5)

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.task_manager.tasks):
            self.task_listbox.insert(tk.END, f"{idx}. {task}")

    def add_task(self):
        description = simpledialog.askstring("Agregar Tarea", "Describe la nueva tarea:")
        if description:
            self.task_manager.add_task(description)
            self.update_task_listbox()

    def complete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.task_manager.mark_task_as_completed(selected_index)
            self.update_task_listbox()
        except IndexError:
            messagebox.showerror("Error", "Por favor selecciona una tarea.")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.task_manager.delete_task(selected_index)
            self.update_task_listbox()
        except IndexError:
            messagebox.showerror("Error", "Por favor selecciona una tarea.")

def main():
    task_manager = TaskManager()
    root = tk.Tk()
    app = TaskApp(root, task_manager)
    root.mainloop()

if __name__ == "__main__":
    main()
