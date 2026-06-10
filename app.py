import random

print("Adivina el número (1-100)")
secreto = random.randint(1, 100)
intentos = 0
a = 15
while True:
    try:
        n = int(input("Tu número: "))
        intentos += 1
        if n < secreto:
            print("Más alto")
        elif n > secreto:
            print("Más bajo")
        else:
            print(f"Ganaste en {intentos} intento(s)")
            break
    except ValueError:
        print("Número inválido")
