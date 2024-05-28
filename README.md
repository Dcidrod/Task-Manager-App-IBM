# Gestor de Tareas

Este proyecto es un gestor de tareas pendientes implementado en Python utilizando la biblioteca Tkinter para la interfaz gráfica de usuario. Permite al usuario agregar, marcar como completadas, y eliminar tareas, con todas las tareas almacenadas en un archivo JSON.

## Características

- **Agregar Tarea**: Permite al usuario agregar una nueva tarea a la lista.
- **Marcar como Completada**: Permite al usuario marcar una tarea como completada.
- **Eliminar Tarea**: Permite al usuario eliminar una tarea de la lista.
- **Mostrar Tareas**: Muestra las tareas pendientes y completadas en listas separadas.
- **Persistencia de Datos**: Las tareas se guardan en un archivo JSON para su persistencia entre sesiones.

## Requisitos

- Python 3.x
- Tkinter (incluido en la mayoría de las instalaciones de Python)
  
## Instalación

1. Clona este repositorio o descarga el archivo ZIP y extráelo en tu directorio deseado.

    ```bash
    git clone https://github.com/tuusuario/gestor-de-tareas.git
    ```

2. Navega al directorio del proyecto.

    ```bash
    cd gestor-de-tareas
    ```

3. Asegúrate de tener Tkinter instalado. Tkinter viene preinstalado con la mayoría de las distribuciones de Python. Si no lo tienes, puedes instalarlo con:

    ```bash
    sudo apt-get install python3-tk
    ```

## Uso

1. Ejecuta el script `task_manager_gui.py`.

    ```bash
    python task_manager_gui.py
    ```

2. Interactúa con la interfaz gráfica para agregar, marcar como completadas o eliminar tareas.

## Estructura del Proyecto

- `task_manager_gui.py`: Archivo principal que contiene la lógica de la aplicación y la interfaz gráfica.
- `tasks.json`: Archivo donde se almacenan las tareas.

## Ejemplo de Uso

### Agregar una Tarea

1. Ingresa la descripción de la tarea en el campo "Indique la tarea".
2. Haz clic en "Agregar Tarea".

### Marcar una Tarea como Completada

1. Selecciona una tarea pendiente de la lista de "Tareas Pendientes".
2. Haz clic en "Marcar como Completada".

### Eliminar una Tarea

1. Ingresa el ID de la tarea que deseas eliminar en el campo "ID de tarea a eliminar".
2. Haz clic en "Eliminar Tarea".

## Manejo de Errores

El programa maneja varias situaciones de error, como la selección de tareas no válidas, entradas vacías y IDs inexistentes. Los mensajes de error se muestran al usuario a través de cuadros de diálogo.

## Contribución

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y commitea (`git commit -am 'Agrega nueva característica'`).
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request.

