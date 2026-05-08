"""Aplicación web sencilla de gestión de tareas.

Este módulo define una pequeña app Flask que permite:
- Crear tareas.
- Marcarlas como completadas o pendientes.
- Eliminarlas.

Las tareas se almacenan en un archivo JSON local (`tareas.json`) para
mantener los datos entre reinicios de la aplicación.
"""

from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Configuración básica de Flask. La `SECRET_KEY` se utilizará en el futuro
# para características como sesiones seguras, mensajes flash, etc.
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

# ===== ESTADO GLOBAL DE LA APLICACIÓN =====
# `tareas` mantiene todas las tareas en memoria mientras la app está corriendo.
# Cada tarea es un diccionario con la forma:
# {
#   "id": int,         # identificador único incremental
#   "texto": str,      # descripción de la tarea
#   "hecho": bool      # True si está completada, False si está pendiente
# }
tareas: list[dict] = []

# `siguiente_id` lleva el control del próximo identificador disponible para
# asignar a una nueva tarea. Se incrementa cada vez que se crea una tarea.
siguiente_id: int = 1

# ===== FUNCIONES DE PERSISTENCIA =====
def cargar_datos():
    """Carga las tareas y el contador de IDs desde el archivo JSON.

    Si el archivo `tareas.json` no existe, o se produce un error al leerlo,
    se inicializan las estructuras en memoria con valores por defecto
    (lista vacía de tareas y `siguiente_id = 1`).
    """
    global siguiente_id, tareas
    try:
        if os.path.exists('tareas.json'):
            # Abrimos el archivo de persistencia y reconstruimos el estado
            # global de la aplicación a partir del JSON.
            with open('tareas.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                tareas = data.get('tareas', [])
                siguiente_id = data.get('siguiente_id', 1)
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        tareas = []
        # En caso de error, partimos de un estado limpio en memoria.
        siguiente_id = 1

def guardar_datos():
    """Persiste el estado actual de la aplicación en el archivo JSON.

    Escribe tanto la lista de tareas como el valor de `siguiente_id`
    para que, al reiniciar la aplicación, se conserve la información.
    """
    try:
        with open('tareas.json', 'w', encoding='utf-8') as f:
            json.dump(
                {
                    'siguiente_id': siguiente_id,
                    'tareas': tareas,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )
    except Exception as e:
        print(f"Error al guardar datos: {e}")

# ===== FUNCIONES DE LÓGICA =====
def agregar_tarea(texto):
    """Añade una nueva tarea a la lista y la guarda en disco.

    Parámetros
    ----------
    texto : str
        Descripción de la tarea introducida por el usuario.
        Se recortan los espacios en blanco al principio y al final.
    """
    global siguiente_id
    tareas.append({
        'id': siguiente_id, 
        'texto': texto.strip(), 
        'hecho': False
    })
    siguiente_id += 1
    guardar_datos()

def completar_tarea(id):
    """Alterna el estado de completado de una tarea.

    Parámetros
    ----------
    id : int
        Identificador único de la tarea a actualizar.

    Comportamiento
    --------------
    Si la tarea está pendiente (`hecho == False`), pasa a completada.
    Si ya estaba completada (`hecho == True`), vuelve a pendiente.
    """
    for tarea in tareas:
        if tarea['id'] == id:
            tarea['hecho'] = not tarea['hecho']  # Toggle (mejor UX)
            break
    guardar_datos()

def eliminar_tarea(id):
    """Elimina de la lista la tarea cuyo identificador coincida con `id`.

    Parámetros
    ----------
    id : int
        Identificador único de la tarea que se desea eliminar.
    """
    global tareas
    tareas = [t for t in tareas if t['id'] != id]
    guardar_datos()

# ===== RUTAS (CONTROLADORES HTTP) =====
@app.route('/')
def index():
    """Página principal.

    Recupera todas las tareas en memoria, las ordena para mostrar primero
    las pendientes y después las completadas, y renderiza la plantilla
    `index.html`.
    """
    # Ordenamos las tareas: las pendientes (hecho == False) aparecen al inicio.
    tareas_ordenadas = sorted(tareas, key=lambda t: t['hecho'])
    return render_template('index.html', tareas=tareas_ordenadas)

@app.route('/agregar', methods=['POST'])
def agregar():
    """Procesa el formulario de creación de una nueva tarea.

    Lee el campo `texto_tarea` enviado por el formulario HTML. Si el texto no
    está vacío después de recortar espacios, se crea una nueva tarea mediante
    `agregar_tarea`. Finalmente, redirige de vuelta a la vista principal.
    """
    texto_tarea = request.form.get('texto_tarea', '').strip()
    if texto_tarea:  # Solo agregar si no está vacío
        agregar_tarea(texto_tarea)
    return redirect(url_for('index'))  # Mejor que redirect('/')

@app.route('/completar/<int:id>')
def completar(id):
    """Marca o desmarca una tarea como completada.

    Esta ruta se invoca normalmente desde un enlace o botón asociado a una
    tarea concreta en la interfaz. Tras actualizar el estado, se redirige
    a la página de inicio.
    """
    completar_tarea(id)
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    """Elimina una tarea específica y vuelve a la página principal.

    La tarea a eliminar se determina a partir del `id` recibido en la URL.
    """
    eliminar_tarea(id)
    return redirect(url_for('index'))

# ===== PUNTO DE ENTRADA DE LA APLICACIÓN =====
if __name__ == '__main__':
    # Cargamos del disco el estado previo (si existe) antes de arrancar
    # el servidor de desarrollo de Flask.
    cargar_datos()
    app.run(debug=True, host='0.0.0.0', port=5000)