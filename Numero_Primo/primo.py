def es_primo(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


numero = int(input("Ingresa un numero entero: "))

if es_primo(numero):
    print(f"{numero} es primo")
else:
    print(f"{numero} no es primo")
