import tkinter as tk  # Importa el módulo tkinter
from tkinter import messagebox  # Importa messagebox de tkinter
from tkinter import ttk  # Importa ttk de tkinter
import json  # Importa el módulo json
import os  # Importa el módulo os

TASKS_FILE = "tasks.json"  # Nombre del archivo donde se guardan las tareas

class Task:
    """
    Representa una tarea con una descripción y un estado de completada o pendiente.
    """
    def __init__(self, description, completed=False, task_id=None):  # Inicializa una nueva tarea
        self.description = description  # Asigna la descripción de la tarea
        self.completed = completed  # Asigna el estado de completada
        self.task_id = task_id  # Asigna el ID de la tarea

    def __str__(self):  # Representación en cadena de una tarea
        status = "Completada" if self.completed else "Pendiente"  # Define el estado como cadena
        return f"{self.task_id}. {self.description} - {status}"  # Devuelve la representación en cadena

    def to_dict(self):  # Convierte la tarea a un diccionario
        return {"description": self.description, "completed": self.completed, "task_id": self.task_id}  # Devuelve el diccionario

    @staticmethod
    def from_dict(data):  # Crea una tarea a partir de un diccionario
        return Task(data["description"], data["completed"], data["task_id"])  # Devuelve una instancia de Task

class TaskManager:
    """
    Gestiona una lista de tareas pendientes.
    """
    def __init__(self):  # Inicializa el gestor de tareas
        self.tasks = []  # Inicializa la lista de tareas
        self.load_tasks()  # Carga las tareas desde el archivo
        self.next_id = len(self.tasks) + 1  # Define el próximo ID disponible

    def add_task(self, description):  # Añade una nueva tarea a la lista
        new_task = Task(description, task_id=self.next_id)  # Crea una nueva tarea
        self.tasks.append(new_task)  # Añade la nueva tarea a la lista
        self.next_id += 1  # Incrementa el próximo ID disponible
        self.save_tasks()  # Guarda las tareas en el archivo

    def mark_task_as_completed(self, task_id):  # Marca una tarea como completada
        for task in self.tasks:  # Itera sobre las tareas
            if task.task_id == task_id:  # Busca la tarea por ID
                if not task.completed:  # Verifica si no está completada
                    task.completed = True  # Marca la tarea como completada
                    self.save_tasks()  # Guarda las tareas en el archivo
                    return True  # Devuelve True si se completó
                else:
                    raise ValueError("La tarea ya está completada.")  # Lanza una excepción si ya estaba completada
        raise ValueError("ID de tarea no válido.")  # Lanza una excepción si el ID no es válido

    def delete_task(self, task_id):  # Elimina una tarea de la lista
        for i, task in enumerate(self.tasks):  # Itera sobre las tareas con su índice
            if task.task_id == task_id:  # Busca la tarea por ID
                del self.tasks[i]  # Elimina la tarea de la lista
                self.save_tasks()  # Guarda las tareas en el archivo
                return True  # Devuelve True si se eliminó
        raise ValueError("ID de tarea no válido.")  # Lanza una excepción si el ID no es válido

    def get_tasks(self):  # Devuelve la lista de tareas
        return self.tasks 

    def save_tasks(self):  # Guarda las tareas en un archivo JSON
        with open(TASKS_FILE, "w") as f:  # Abre el archivo para escritura
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)  # Guarda las tareas en formato JSON

    def load_tasks(self):  # Carga las tareas desde un archivo JSON
        if os.path.exists(TASKS_FILE):  # Verifica si el archivo existe
            with open(TASKS_FILE, "r") as f:  # Abre el archivo para lectura
                tasks_data = json.load(f)  # Carga los datos desde el archivo
                self.tasks = [Task.from_dict(data) for data in tasks_data]  # Crea instancias de Task desde los datos
                if self.tasks:  # Si hay tareas cargadas
                    self.next_id = max(task.task_id for task in self.tasks) + 1  # Define el próximo ID
                else:
                    self.next_id = 1  # Si no hay tareas, el próximo ID es 1

class TaskManagerApp:
    """
    Interfaz gráfica de usuario para gestionar tareas mediante el TaskManager.
    """
    def __init__(self, root):  # Inicializa la aplicación
        self.task_manager = TaskManager()  # Crea una instancia de TaskManager
        self.root = root  # Asigna la ventana raíz
        self.root.title("Gestor de Tareas")  # Establece el título de la ventana
        self.create_widgets()  # Crea los widgets

    def create_widgets(self):  # Crea los widgets de la interfaz
        self.main_frame = ttk.Frame(self.root, padding="10")  # Crea el marco principal
        self.main_frame.pack(fill=tk.BOTH, expand=True)  # Empaqueta el marco principal

        self.pending_frame = ttk.LabelFrame(self.main_frame, text="Tareas Pendientes", padding="10")  # Crea el marco de tareas pendientes
        self.pending_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Posiciona el marco de tareas pendientes

        self.completed_frame = ttk.LabelFrame(self.main_frame, text="Tareas Completadas", padding="10")  # Crea el marco de tareas completadas
        self.completed_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Posiciona el marco de tareas completadas

        self.task_listbox_pending = tk.Listbox(self.pending_frame, width=50, height=15)  # Crea la lista de tareas pendientes
        self.task_listbox_pending.pack(pady=5)  # Empaqueta la lista de tareas pendientes

        self.task_listbox_completed = tk.Listbox(self.completed_frame, width=50, height=15)  # Crea la lista de tareas completadas
        self.task_listbox_completed.pack(pady=5)  # Empaqueta la lista de tareas completadas

        self.entry_frame = ttk.Frame(self.main_frame, padding="10")  # Crea el marco para la entrada de tareas
        self.entry_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")  # Posiciona el marco de entrada de tareas

        self.entry_label = ttk.Label(self.entry_frame, text="Indique la tarea:")  # Crea la etiqueta para la entrada de tareas
        self.entry_label.pack(side=tk.LEFT, padx=5)  # Empaqueta la etiqueta

        self.entry = ttk.Entry(self.entry_frame, width=50)  # Crea el campo de entrada de tareas
        self.entry.pack(side=tk.LEFT, padx=5)  # Empaqueta el campo de entrada

        self.add_button = ttk.Button(self.entry_frame, text="Agregar Tarea", command=self.add_task)  # Crea el botón para agregar tareas
        self.add_button.pack(side=tk.LEFT, padx=5)  # Empaqueta el botón de agregar tareas

        self.complete_button = ttk.Button(self.main_frame, text="Marcar como Completada", command=self.mark_task_as_completed)  # Crea el botón para marcar tareas como completadas
        self.complete_button.grid(row=2, column=0, pady=10)  # Posiciona el botón de marcar como completada

        self.delete_frame = ttk.Frame(self.main_frame, padding="10")  # Crea el marco para eliminar tareas
        self.delete_frame.grid(row=2, column=1, pady=10, sticky="ew")  # Posiciona el marco de eliminar tareas

        self.delete_label = ttk.Label(self.delete_frame, text="ID de tarea a eliminar:")  # Crea la etiqueta para eliminar tareas
        self.delete_label.pack(side=tk.LEFT, padx=5)  # Empaqueta la etiqueta de eliminar tareas

        self.delete_entry = ttk.Entry(self.delete_frame, width=10)  # Crea el campo de entrada del ID de la tarea a eliminar
        self.delete_entry.pack(side=tk.LEFT, padx=5)  # Empaqueta el campo de entrada del ID

        self.delete_button = ttk.Button(self.delete_frame, text="Eliminar Tarea", command=self.delete_task)  # Crea el botón para eliminar tareas
        self.delete_button.pack(side=tk.LEFT, padx=5)  # Empaqueta el botón de eliminar tareas

        self.exit_button = ttk.Button(self.main_frame, text="Salir", command=self.root.quit)  # Crea el botón para salir de la aplicación
        self.exit_button.grid(row=3, column=0, columnspan=2, pady=10)  # Posiciona el botón de salir

        self.update_task_list()  # Actualiza la lista de tareas

    def update_task_list(self):  # Actualiza la lista de tareas en los Listbox
        self.task_listbox_pending.delete(0, tk.END)  # Limpia la lista de tareas pendientes
        self.task_listbox_completed.delete(0, tk.END)  # Limpia la lista de tareas completadas

        for task in self.task_manager.get_tasks():  # Itera sobre las tareas
            if task.completed:  # Si la tarea está completada
                self.task_listbox_completed.insert(tk.END, str(task))  # Añade la tarea a la lista de completadas
            else:
                self.task_listbox_pending.insert(tk.END, str(task))  # Añade la tarea a la lista de pendientes

    def add_task(self):  # Añade una nueva tarea desde la entrada de texto
        description = self.entry.get()  # Obtiene la descripción de la tarea
        if description:  # Si la descripción no está vacía
            try:
                self.task_manager.add_task(description)  # Añade la tarea al gestor
                self.entry.delete(0, tk.END)  # Limpia el campo de entrada
                self.update_task_list()  # Actualiza la lista de tareas
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la tarea: {e}")  # Muestra un mensaje de error
        else:
            messagebox.showwarning("Advertencia", "La descripción de la tarea no puede estar vacía.")  # Muestra una advertencia

    def mark_task_as_completed(self):  # Marca la tarea seleccionada como completada
        try:
            selected_index = self.task_listbox_pending.curselection()[0]  # Obtiene el índice de la tarea seleccionada
            task_id = int(self.task_listbox_pending.get(selected_index).split('.')[0])  # Obtiene el ID de la tarea
            try:
                self.task_manager.mark_task_as_completed(task_id)  # Marca la tarea como completada
                self.update_task_list()  # Actualiza la lista de tareas
            except ValueError as e:
                messagebox.showerror("Error", str(e))  # Muestra un mensaje de error
        except IndexError:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea pendiente.")  # Muestra una advertencia
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")  # Muestra un mensaje de error

    def delete_task(self):  # Elimina la tarea seleccionada
        try:
            task_id = int(self.delete_entry.get())  # Obtiene el ID de la tarea a eliminar
            try:
                self.task_manager.delete_task(task_id)  # Elimina la tarea del gestor
                self.delete_entry.delete(0, tk.END)  # Limpia el campo de entrada
                self.update_task_list()  # Actualiza la lista de tareas
            except ValueError as e:
                messagebox.showerror("Error", str(e))  # Muestra un mensaje de error
        except ValueError:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un ID de tarea válido.")  # Muestra una advertencia
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")  # Muestra un mensaje de error

if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal de la aplicación
    app = TaskManagerApp(root)  # Crea una instancia de la aplicación
    root.mainloop()  # Inicia el bucle principal de la aplicación
