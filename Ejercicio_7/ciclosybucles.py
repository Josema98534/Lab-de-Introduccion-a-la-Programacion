def ejercicio_1():
    print("Este es el ejercicio 1")
    palabra = input("Ingresa la palabra a repetir: ")

    for i in range(10):
        print(palabra)


def ejercicio_2():
    print("Este es el ejercicio 2")
    
    edad = int(input("¿Cuál es su edad? "))

    for ano in range(1, edad + 1):
        print("Has cumplido", ano, "años")

def ejercicio_3():
    print("Este es el ejercicio 3")
    numero = int(input("Introduce un número entero positivo: "))

    for i in range(1, numero + 1):
        if i % 2 != 0:
            print(i, end=", ")

def ejercicio_4():
    print("Este es el ejercicio 4")
    numero = int(input("Introduce un número entero positivo: "))

    for i in range(numero, -1, -1):
        print(i, end=", ")



def ejercicio_5():
    inversion = float(input("Cantidad a invertir: "))
    interes = float(input("Interés anual (%): "))
    años = int(input("Número de años: "))

    capital = inversion

    for año in range(1, años + 1):
        capital += capital * interes / 100
        print(f"Año {año}: {capital:.2f}")



def ejercicio_6():
    print("Este es el ejercicio 6")
    altura = int(input("Introduce la altura del triángulo: "))
    
    for i in range(1, altura + 1):
        print("*" * i)


def ejercicio_7():
    print("Este es el ejercicio 7")
    for numero in range(1, 11):
        print(f"Tabla del {numero}:")
    
        for multiplicador in range(1, 11):
            resultado = numero * multiplicador
            print(f"{numero} x {multiplicador} = {resultado}")
    
    print()


def ejercicio_8():
    print("Este es el ejercicio 8")
    altura = int(input("Introduce la altura del triángulo: "))

    for fila in range(1, altura + 1):
        impar = 2 * fila - 1
        for i in range(fila):
            print(impar, end=" ")
            impar -= 2
        print()


def ejercicio_9():
    print("Este es el ejercicio 9")
    contraseña = "12345"
    usuario = ""

    while usuario != contraseña:
        usuario = input("Introduce la contraseña: ")
    print("Contraseña correcta")


def ejercicio_10():
    print("Este es el ejercicio 10")
    numero = int(input("Introduce un número: "))

    if numero < 2:
        print("No es primo")
    else:
        es_primo = True
        for i in range(2, int(numero ** 0.5) + 1):
            if numero % i == 0:
                es_primo = False
                break
        if es_primo:
            print("Es primo")
        else:
            print("No es primo")

def ejercicio_11():
    print("Este es el ejercicio 11")
    palabra = input("Introduce una palabra: ")

    for letra in palabra[::-1]:
        print(letra)


def ejercicio_12():
    print("Este es el ejercicio 12")
    frase = input("Introduce una frase: ")
    letra = input("Introduce la letra a buscar: ")

    contador = 0
    for l in frase:
        if l == letra:
            contador += 1

    print("La letra aparece", contador, "veces")


def ejercicio_13():
    print("Este es el ejercicio 13")
    while True:
        texto = input("Introduce algo: ")
        if texto.lower() == "salir":
            break
        print(texto)



ejercicios = {
    1: ejercicio_1,
    2: ejercicio_2,
    3: ejercicio_3,
    4: ejercicio_4,
    5: ejercicio_5,
    6: ejercicio_6,
    7: ejercicio_7,
    8: ejercicio_8,
    9: ejercicio_9,
    10: ejercicio_10,
    11: ejercicio_11,
    12: ejercicio_12,
    13: ejercicio_13
}



while True:
    print("\n--- MENU DE EJERCICIOS ---")
    print("1 al 13 para ejecutar ejercicios")
    print("0 para salir")

    opcion = int(input("Elige un ejercicio: "))

    if opcion == 0:
        print("Programa terminado")
        break

    elif opcion in ejercicios:
        ejercicios[opcion]()

    else:
        print("Opción no válida")