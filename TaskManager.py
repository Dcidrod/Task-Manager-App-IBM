import json

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
        print(f"Tarea '{description}' agregada.")
        self.save_tasks()

    def mark_task_as_completed(self, position):
        try:
            self.tasks[position].completed = True
            print(f"Tarea '{self.tasks[position].description}' marcada como completada.")
            self.save_tasks()
        except IndexError:
            print("Error: posición de tarea no válida.")

    def show_all_tasks(self):
        if not self.tasks:
            print("No hay tareas en la lista.")
        else:
            for idx, task in enumerate(self.tasks):
                print(f"{idx}. {task}")

    def delete_task(self, position):
        try:
            removed_task = self.tasks.pop(position)
            print(f"Tarea '{removed_task.description}' eliminada.")
            self.save_tasks()
        except IndexError:
            print("Error: posición de tarea no válida.")

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            tasks_dict = [task.to_dict() for task in self.tasks]
            json.dump(tasks_dict, file, indent=4)
        print("Tareas guardadas en el archivo.")

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                tasks_dict = json.load(file)
                return [Task.from_dict(task) for task in tasks_dict]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

def main():
    task_manager = TaskManager()

    while True:
        print("\nOpciones:")
        print("1. Agregar una nueva tarea")
        print("2. Marcar una tarea como completada")
        print("3. Mostrar todas las tareas")
        print("4. Eliminar una tarea")
        print("5. Salir")
        
        try:
            option = int(input("Selecciona una opción: "))
        except ValueError:
            print("Error: por favor ingresa un número válido.")
            continue

        if option == 1:
            description = input("Describe la nueva tarea: ")
            task_manager.add_task(description)
        elif option == 2:
            try:
                position = int(input("Ingresa la posición de la tarea a marcar como completada: "))
                task_manager.mark_task_as_completed(position)
            except ValueError:
                print("Error: por favor ingresa un número válido.")
        elif option == 3:
            task_manager.show_all_tasks()
        elif option == 4:
            try:
                position = int(input("Ingresa la posición de la tarea a eliminar: "))
                task_manager.delete_task(position)
            except ValueError:
                print("Error: por favor ingresa un número válido.")
        elif option == 5:
            print("Saliendo del programa. ¡Adiós!")
            break
        else:
            print("Error: opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
