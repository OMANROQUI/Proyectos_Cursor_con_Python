print("hola, cursor")
# Este bucle imprime los números del 0 al 4 en la consola
for i in range(5):
    print(i)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)



def suma_lista(lista: list[int]) -> int:
    if len(lista) == 0:
        return 0
    else:
        return lista[0] + suma_lista(lista[1:])


print(suma_lista([1, 2, 3, 4, 5]))
print(factorial(5))