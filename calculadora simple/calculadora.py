def sumar(a, b):
    return a + b


def restar(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ZeroDivisionError("No se puede dividir entre cero.")
    return a / b


def pedir_numero(mensaje):
    while True:
        entrada = input(mensaje).strip()
        try:
            return float(entrada)
        except ValueError:
            print("Entrada invalida. Escribe un numero (ejemplo: 10, 3.5, -2).")


def main():
    operaciones = {
        "suma": sumar,
        "resta": restar,
        "multiplicacion": multiplicar,
        "división": dividir,
        "division": dividir,
    }

    print("Calculadora interactiva")
    print("Operaciones disponibles: suma, resta, multiplicacion, division")
    print('Escribe "salir" para terminar.\n')

    while True:
        operacion = input("Operacion: ").strip().lower()

        if operacion == "salir":
            print("Hasta luego.")
            break

        if operacion not in operaciones:
            print("Operacion no valida. Intenta de nuevo.\n")
            continue

        numero_1 = pedir_numero("Primer numero: ")
        numero_2 = pedir_numero("Segundo numero: ")

        try:
            resultado = operaciones[operacion](numero_1, numero_2)
            print(f"Resultado: {resultado}\n")
        except ZeroDivisionError as error:
            print(f"Error: {error}\n")


if __name__ == "__main__":
    main()
