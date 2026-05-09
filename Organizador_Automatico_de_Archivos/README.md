<div align="center">

# 📁 Organizador Automático de Archivos

### *Dile adiós al caos digital* ✨

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/OMANROQUI/Proyectos_Cursor_con_Python/graphs/commit-activity)

[Características](#-características) •
[Instalación](#-instalación) •
[Uso](#-uso) •
[Ejemplos](#-ejemplos) •
[Contribuir](#-contribuir)

![Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=Demo+Organizador+de+Archivos)

</div>

---

## 🎯 ¿Qué es esto?

**Organizador Automático de Archivos** es un script inteligente en Python que transforma el caos de tu carpeta de Descargas (o cualquier directorio) en un sistema organizado y eficiente. Con solo un comando, los archivos del **primer nivel** de esa carpeta se clasifican automáticamente en subcarpetas según su extensión.

### 💡 El Problema

```text
Downloads/
├── foto_vacaciones.jpg
├── documento_importante.pdf
├── cancion.mp3
├── proyecto.zip
├── video.mp4
├── script.py
└── ... 😵 (100 archivos más desordenados)
```

### ✨ La Solución

```text
Downloads/
├── 📸 Imagenes/
│   └── foto_vacaciones.jpg
├── 📄 Documentos/
│   └── documento_importante.pdf
├── 🎵 Musica/
│   └── cancion.mp3
├── 📦 Comprimidos/
│   └── proyecto.zip
├── 🎬 Videos/
│   └── video.mp4
└── 💻 Codigo/
    └── script.py
```

> En disco, los nombres de carpeta coinciden con las claves del script (`Imagenes`, `Musica`, `Codigo`, etc., sin tildes en `Codigo`).

---

## 🚀 Características

<table>
<tr>
<td>

### 🎨 Interfaz Amigable
Menú interactivo fácil de usar, no necesitas ser un experto en terminal

</td>
<td>

### ⚡ Super Rápido
Organiza cientos de archivos en segundos

</td>
</tr>
<tr>
<td>

### 🔍 Vista Previa
Muestra qué va a hacer antes de mover nada (resumen por categoría)

</td>
<td>

### 🛡️ Seguro
Maneja duplicados renombrando con sufijo `_1`, `_2`, … y pide confirmación salvo que indiques lo contrario

</td>
</tr>
<tr>
<td>

### 🎯 Personalizable
7 categorías predefinidas + carpeta **Otros** para el resto

</td>
<td>

### 🤖 Automatizable
Ejecución por línea de comandos con `--yes` o `-y` para scripts y tareas programadas

</td>
</tr>
</table>

---

## 📦 Instalación

### Requisitos Previos

- Python 3.6 o superior (solo biblioteca estándar: `pathlib`, sin `pip install`)
- Sistema operativo: Windows, macOS o Linux

### Pasos de Instalación

1. **Descarga** solo el archivo [`organizar.py`](https://github.com/OMANROQUI/Proyectos_Cursor_con_Python/blob/main/Organizador_Automático_de_Archivos/organizar.py) desde el repositorio [`Proyectos_Cursor_con_Python`](https://github.com/OMANROQUI/Proyectos_Cursor_con_Python/tree/main/): abre el enlace y pulsa **Raw**, luego guarda la página como `organizar.py` (o usa *Save link as…* sobre **Raw**).
2. **Colócalo** donde quieras (por ejemplo una carpeta `scripts` o tu Escritorio).
3. **Abre una terminal** en esa carpeta y ejecuta `python3 organizar.py` (o `python organizar.py` en Windows).

No hace falta clonar el repositorio ni instalar dependencias: el script usa solo la biblioteca estándar de Python.

**Descarga rápida con terminal** (Linux / macOS / Git Bash en Windows):

```bash
curl -fsSL -o organizar.py "https://raw.githubusercontent.com/OMANROQUI/Proyectos_Cursor_con_Python/main/Organizador_Automático_de_Archivos/organizar.py"
```

---

## 💻 Uso

### Modo Interactivo (Recomendado para principiantes)

```bash
python3 organizar.py
```

Se mostrará un menú como este:

```text
============================================================
📁 ORGANIZADOR AUTOMÁTICO DE ARCHIVOS
============================================================

¿Qué carpeta deseas organizar?

1. Carpeta actual (donde está el script)
2. Carpeta de Descargas
3. Especificar otra carpeta
4. Salir

------------------------------------------------------------

Elige una opción (1-4):
```

> **Nota:** La opción **1** usa el **directorio de trabajo actual** (`cwd`), es decir, la carpeta desde la que ejecutas el comando, no necesariamente la ubicación del archivo `organizar.py`.

### Modo Línea de Comandos (Para usuarios avanzados)

```bash
# Organizar una carpeta específica
python3 organizar.py /ruta/a/carpeta

# Organizar la carpeta actual
python3 organizar.py .

# Organizar sin confirmación (para automatización)
python3 organizar.py ~/Downloads --yes
# equivalente:
python3 organizar.py ~/Downloads -y
```

---

## 📂 Categorías Soportadas

| Categoría | Extensiones |
|-----------|-------------|
| 📸 **Imagenes** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`, `.ico` |
| 📄 **Documentos** | `.pdf`, `.docx`, `.txt`, `.xlsx`, `.pptx`, `.doc`, `.odt`, `.csv` |
| 🎬 **Videos** | `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm` |
| 🎵 **Musica** | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a` |
| 📦 **Comprimidos** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2` |
| 💻 **Programas** | `.exe`, `.msi`, `.dmg`, `.deb`, `.apk`, `.appimage` |
| 🔧 **Codigo** | `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.sh` |
| 📁 **Otros** | Todo lo demás |

---

## 🎬 Ejemplos

### Ejemplo 1: Organizar Descargas

```bash
python3 organizar.py ~/Downloads
```

**Salida (ilustrativa):**

```text
📂 Se encontraron 15 archivos para organizar:
------------------------------------------------------------

📁 Documentos (5 archivos):
   • informe_2024.pdf
   • presupuesto.xlsx
   • notas.txt
   ... y 2 más

📁 Imagenes (3 archivos):
   • foto1.jpg
   • screenshot.png
   • logo.svg
============================================================

¿Deseas continuar con la organización? (s/n): s

📂 Organizando archivos...

✅ informe_2024.pdf                      → Documentos/
✅ foto1.jpg                             → Imagenes/
✅ cancion.mp3                           → Musica/

🎉 ¡Completado! 15 archivos organizados
```

### Ejemplo 2: Crear Alias

Para ejecutar desde cualquier lugar:

```bash
# Agrega a tu ~/.bashrc o ~/.zshrc
echo "alias organizar='python3 /ruta/completa/organizar.py'" >> ~/.bashrc
source ~/.bashrc

# Ahora puedes usar:
cd ~/Downloads
organizar .
```

---

## 🛠️ Características Técnicas

### Manejo Inteligente de Duplicados

Si un archivo con el mismo nombre ya existe en la carpeta destino:

```text
documento.pdf  →  Documentos/documento.pdf
documento.pdf  →  Documentos/documento_1.pdf
documento.pdf  →  Documentos/documento_2.pdf
```

### Validaciones y Comportamiento

- Verifica que la ruta exista y sea un directorio
- No mueve el propio script: se excluyen `organizar.py` y `organizar_mejorado.py` si están en esa carpeta
- Ignora archivos ocultos (nombre que empieza por `.`)
- Ignora subcarpetas: **solo organiza archivos sueltos en la raíz de la carpeta elegida** (no es recursivo)
- Pide confirmación antes de mover, salvo `--yes` / `-y`
- Respuestas aceptadas para confirmar: `s`, `si`, `sí`, `y`, `yes`
- Errores inesperados se muestran en consola; `Ctrl+C` cancela de forma limpia

### Carpeta «Descargas» en el menú

La opción 2 usa `Path.home() / "Downloads"`. En muchos sistemas en español (p. ej. Windows) la carpeta puede llamarse **Descargas**. En ese caso usa la **opción 3** y escribe la ruta completa, o pasa la ruta por argumento: `python3 organizar.py "%USERPROFILE%\Downloads"` (o la ruta que corresponda).

---

## 🎨 Personalización

### Agregar Nuevas Categorías

Edita el diccionario `CATEGORIAS` en `organizar.py`:

```python
CATEGORIAS = {
    "Imagenes": [".jpg", ".png", ...],
    "Documentos": [".pdf", ".docx", ...],
    # Agrega tu nueva categoría aquí
    "Ebooks": [".epub", ".mobi", ".azw3"],
    "Fuentes": [".ttf", ".otf", ".woff"],
}
```

### Cambiar Rutas del Menú

Modifica `obtener_carpeta_usuario()` (y, si hace falta, la rama de la opción 2) para adaptar rutas por defecto a tu sistema.

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar este proyecto:

1. 🍴 Haz un fork del proyecto
2. 🔨 Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. 💾 Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push a la rama (`git push origin feature/AmazingFeature`)
5. 🎉 Abre un Pull Request

### Ideas para Contribuir

- [ ] Interfaz gráfica (GUI) con Tkinter
- [ ] Configuración mediante archivo JSON
- [ ] Organización por fecha además de tipo
- [ ] Modo `--dry-run` que no mueva archivos (hoy la vista previa ya muestra el plan antes de confirmar)
- [ ] Función de deshacer última organización
- [ ] Soporte para reglas personalizadas
- [ ] Logging / historial de cambios

---


## 👨‍💻 Autor

<div align="center">

### **OMANROQUI**

[![GitHub](https://img.shields.io/badge/GitHub-OMANROQUI-181717?style=for-the-badge&logo=github)](https://github.com/OMANROQUI)
[![Email](https://img.shields.io/badge/Email-omanroqui@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:omanroqui@gmail.com)

*"Automatizando el caos, un archivo a la vez"* 🚀

</div>

---

## 🙏 Agradecimientos

- A la comunidad de Python por las excelentes herramientas
- A todos los que contribuyan con ideas y mejoras
- A ti, por usar este proyecto ❤️

---

## ⭐ Dale una Estrella

Si este proyecto te fue útil, ¡considera darle una estrella! ⭐

Es gratis y motiva a seguir creando herramientas útiles para la comunidad.

---

<div align="center">

**[⬆ Volver arriba](#-organizador-automático-de-archivos)**

Hecho con ❤️ y ☕ por [OMANROQUI](https://github.com/OMANROQUI)

</div>
