# 📝 Gestor de Tareas

![Flask](https://img.shields.io/badge/Flask-3.1.3-green?style=flat-square&logo=flask)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

Aplicación web sencilla para gestionar tareas pendientes (to-do list) desarrollada con Flask, plantillas Jinja2 y persistencia en JSON.

---

## 🌟 Características

- ✅ **Agregar tareas** - Formulario simple para crear nuevas tareas
- ☑️ **Marcar completadas** - Toggle con un solo clic en el checkbox
- 🗑️ **Eliminar tareas** - Confirmación antes de eliminar
- 💾 **Persistencia** - Los datos se guardan automáticamente en `tareas.json`
- 📊 **Estadísticas** - Resumen de tareas pendientes y completadas
- 🎨 **Diseño moderno** - Interfaz responsive con degradado personalizable
- 🔄 **Ordenamiento inteligente** - Tareas pendientes aparecen primero

---

## 🛠️ Tecnologías utilizadas

- **Backend**: Flask 3.1.3
- **Frontend**: HTML5, CSS3, JavaScript
- **Template Engine**: Jinja2
- **Persistencia**: JSON

---

## 📋 Requisitos previos

- **Python 3.9 o superior**
- **pip** (gestor de paquetes de Python)
- **Git** (para clonar el repositorio)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/gestor-tareas-flask.git
cd gestor-tareas-flask
```

### 2. Crear entorno virtual

**En Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## ▶️ Uso

### 1. Iniciar la aplicación

```bash
python app.py
```

Deberías ver algo como:
```
==================================================
🚀 Iniciando Gestor de Tareas
==================================================
✅ Datos cargados: 0 tareas
📊 Servidor corriendo en http://127.0.0.1:5000
💡 Presiona CTRL+C para detener
==================================================
```

### 2. Abrir en el navegador

- **Local**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Otra máquina en la red**: `http://TU_IP:5000`

### 3. Usar la aplicación

- **Agregar tarea**: Escribe en el campo de texto y presiona "➕ Agregar"
- **Completar/Descompletar**: Haz clic en el checkbox junto a la tarea
- **Eliminar**: Haz clic en el icono 🗑️ y confirma

---

## 📁 Estructura del proyecto

```
gestor-tareas-flask/
│
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Documentación (este archivo)
├── .gitignore            # Archivos a ignorar en Git
│
├── templates/            # Plantillas HTML
│   └── index.html        # Vista principal
│
├── static/              # Archivos estáticos
│   └── style.css         # Estilos personalizados
│
└── tareas.json          # Base de datos (generado automáticamente)
```

---

## 🛣️ Rutas de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Muestra la lista de tareas |
| `POST` | `/agregar` | Crea una nueva tarea |
| `GET` | `/completar/<id>` | Marca/desmarca una tarea como completada |
| `GET` | `/eliminar/<id>` | Elimina una tarea específica |

---

## 🎨 Personalización

### Cambiar colores

Edita `static/style.css`. Las variables CSS principales están al inicio:

```css
:root {
  --color-primary: #2563eb;        /* Color principal (azul) */
  --color-primary-hover: #1d4ed8;  /* Hover del botón */
  --color-danger: #991b1b;         /* Color de eliminar (rojo) */
}
```

### Cambiar el degradado del fondo

En `static/style.css`, busca la regla `body`:

```css
body {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* Cambia los colores del degradado aquí */
}
```

---

## 🔒 Seguridad

⚠️ **Importante**: Este proyecto es para aprendizaje y desarrollo local.

Para producción, considera:
- Usar variables de entorno para `SECRET_KEY`
- Implementar autenticación de usuarios
- Migrar a una base de datos real (SQLite, PostgreSQL)
- Configurar HTTPS
- Validar y sanitizar entradas del usuario

---

## 🐛 Solución de problemas

### Error: `ModuleNotFoundError: No module named 'flask'`

**Causa**: Flask no está instalado o el entorno virtual no está activado.

**Solución**:
```bash
source venv/bin/activate  # Activar entorno virtual
pip install -r requirements.txt
```

### Error: `Address already in use` (puerto 5000 ocupado)

**Causa**: Otro proceso está usando el puerto 5000.

**Solución**: Cambia el puerto en `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

### Las tareas no se guardan

**Causa**: Falta de permisos de escritura.

**Solución**: Verifica que tienes permisos en la carpeta del proyecto:
```bash
ls -la
```

---

## 🚀 Mejoras futuras

- [ ] Categorías y etiquetas para tareas
- [ ] Fechas límite con notificaciones
- [ ] Sistema de prioridades (Alta, Media, Baja)
- [ ] Búsqueda y filtros avanzados
- [ ] Exportar tareas a CSV/PDF
- [ ] Modo oscuro (dark mode)
- [ ] API REST completa
- [ ] Autenticación de usuarios
- [ ] Base de datos SQL (SQLite/PostgreSQL)
- [ ] Despliegue en la nube (Render, Railway, Heroku)

---

## 📝 Licencia

Este proyecto está bajo la [Licencia MIT](https://opensource.org/licenses/MIT).

---

## 👨‍💻 Autor

**Omar Rodríguez**

- GitHub: [OMANROQUI]
- Email: omanroqui@gmail.com

---

## 🙏 Agradecimientos

Proyecto desarrollado como parte del aprendizaje de desarrollo web con Flask.

---

## 📚 Recursos útiles

- [Documentación oficial de Flask](https://flask.palletsprojects.com/)
- [Documentación de Jinja2](https://jinja.palletsprojects.com/)
- [Tutorial de Python](https://docs.python.org/3/tutorial/)

---

<div align="center">

**¿Te gustó el proyecto? ¡Dale una ⭐ en GitHub!**

Hecho con ❤️ y Python

</div>