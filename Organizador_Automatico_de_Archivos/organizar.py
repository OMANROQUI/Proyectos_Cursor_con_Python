from pathlib import Path
import sys

# ========== CONFIGURACIÓN ==========
CATEGORIAS = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".doc", ".odt", ".csv"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
    "Musica": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Programas": [".exe", ".msi", ".dmg", ".deb", ".apk", ".appimage"],
    "Codigo": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".sh"],
}

# Crear mapeo inverso
extension_a_categoria = {}
for categoria, extensiones in CATEGORIAS.items():
    for ext in extensiones:
        extension_a_categoria[ext.lower()] = categoria


# ========== FUNCIÓN PRINCIPAL ==========
def organizar_archivos(carpeta_objetivo, modo_silencioso=False):
    """
    Organiza archivos en subcarpetas según su extensión
    
    Args:
        carpeta_objetivo: Ruta de la carpeta a organizar
        modo_silencioso: Si es True, no pide confirmación
    """
    carpeta_objetivo = Path(carpeta_objetivo).resolve()
    
    # Validar que la carpeta existe
    if not carpeta_objetivo.exists():
        print(f"❌ Error: La carpeta '{carpeta_objetivo}' no existe")
        return False
    
    if not carpeta_objetivo.is_dir():
        print(f"❌ Error: '{carpeta_objetivo}' no es una carpeta")
        return False
    
    # Listar solo archivos (excluir directorios y archivos ocultos)
    archivos = [
        f for f in carpeta_objetivo.iterdir() 
        if f.is_file() and not f.name.startswith('.')
    ]
    
    # Excluir el script mismo
    archivos = [f for f in archivos if f.name not in ['organizar.py', 'organizar_mejorado.py']]
    
    if not archivos:
        print("📭 No hay archivos para organizar en esta carpeta")
        return False
    
    # Mostrar vista previa
    print(f"\n📂 Se encontraron {len(archivos)} archivos para organizar:")
    print("-" * 60)
    
    # Agrupar por categoría para vista previa
    preview = {}
    for archivo in archivos:
        extension = archivo.suffix.lower()
        categoria = extension_a_categoria.get(extension, "Otros")
        
        if categoria not in preview:
            preview[categoria] = []
        preview[categoria].append(archivo.name)
    
    # Mostrar resumen por categoría
    for categoria, nombres in sorted(preview.items()):
        print(f"\n📁 {categoria} ({len(nombres)} archivos):")
        for nombre in nombres[:3]:  # Mostrar solo los primeros 3
            print(f"   • {nombre}")
        if len(nombres) > 3:
            print(f"   ... y {len(nombres) - 3} más")
    
    print("\n" + "=" * 60)
    
    # Pedir confirmación (a menos que esté en modo silencioso)
    if not modo_silencioso:
        respuesta = input("\n¿Deseas continuar con la organización? (s/n): ").strip().lower()
        if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Operación cancelada")
            return False
    
    # Proceder con la organización
    print(f"\n📂 Organizando archivos...\n")
    archivos_movidos = 0
    
    for archivo in archivos:
        extension = archivo.suffix.lower()
        categoria = extension_a_categoria.get(extension, "Otros")
        
        # Crear carpeta destino
        carpeta_destino = carpeta_objetivo / categoria
        carpeta_destino.mkdir(exist_ok=True)
        
        # Manejar duplicados
        ruta_destino = carpeta_destino / archivo.name
        if ruta_destino.exists():
            contador = 1
            nombre_base = archivo.stem
            while ruta_destino.exists():
                nuevo_nombre = f"{nombre_base}_{contador}{extension}"
                ruta_destino = carpeta_destino / nuevo_nombre
                contador += 1
        
        # Mover archivo
        archivo.rename(ruta_destino)
        archivos_movidos += 1
        print(f"✅ {archivo.name:40} → {categoria}/")
    
    print(f"\n🎉 ¡Completado! {archivos_movidos} archivos organizados")
    return True


# ========== MENÚ INTERACTIVO ==========
def mostrar_menu():
    """Muestra menú de opciones"""
    print("\n" + "=" * 60)
    print("📁 ORGANIZADOR AUTOMÁTICO DE ARCHIVOS")
    print("=" * 60)
    print("\n¿Qué carpeta deseas organizar?")
    print("\n1. Carpeta actual (donde está el script)")
    print("2. Carpeta de Descargas")
    print("3. Especificar otra carpeta")
    print("4. Salir")
    print("\n" + "-" * 60)


def obtener_carpeta_usuario():
    """Obtiene la carpeta que el usuario quiere organizar"""
    while True:
        mostrar_menu()
        opcion = input("\nElige una opción (1-4): ").strip()
        
        if opcion == "1":
            return Path.cwd()  # Carpeta actual
        
        elif opcion == "2":
            return Path.home() / "Downloads"
        
        elif opcion == "3":
            ruta = input("\nEscribe la ruta de la carpeta: ").strip()
            # Eliminar comillas si el usuario las puso
            ruta = ruta.strip('"').strip("'")
            return Path(ruta)
        
        elif opcion == "4":
            print("\n👋 ¡Hasta luego!")
            sys.exit(0)
        
        else:
            print("❌ Opción inválida. Intenta de nuevo.")


# ========== EJECUCIÓN ==========
if __name__ == "__main__":
    try:
        # Verificar si se pasó una carpeta como argumento
        if len(sys.argv) > 1:
            # Modo línea de comandos
            carpeta = Path(sys.argv[1])
            modo_silencioso = "--yes" in sys.argv or "-y" in sys.argv
            organizar_archivos(carpeta, modo_silencioso)
        else:
            # Modo interactivo
            carpeta = obtener_carpeta_usuario()
            organizar_archivos(carpeta, modo_silencioso=False)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)