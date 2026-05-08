import re
from collections import Counter


class ContadorDePalabras:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo

    def leer_archivo(self):
        with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
            return archivo.read()

    def contar_palabras(self, texto):
        palabras = re.findall(r"\w+", texto.lower())
        total_palabras = len(palabras)
        frecuencias = Counter(palabras)
        return total_palabras, frecuencias


if __name__ == "__main__":
    ruta = input("Ingrese la ruta del archivo de texto: ")
    contador = ContadorDePalabras(ruta)

    try:
        contenido = contador.leer_archivo()
        total, frecuencias = contador.contar_palabras(contenido)
    except FileNotFoundError:
        print("El archivo especificado no existe.")
    except Exception as e:
        print(f"Ocurrio un error al procesar el archivo: {e}")
    else:
        print(f"Total palabras: {total}")
        print("Palabras más frecuentes:")
        for palabra, freq in frecuencias.most_common(10):
            print(f"{palabra}: {freq}")