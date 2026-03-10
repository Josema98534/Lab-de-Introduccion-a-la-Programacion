def pedir_usuario_clave():
    """Pide usuario y clave y valida formato."""
    while True:
        usuario = input("Usuario: ").strip()
        clave = input("Contraseña: ").strip()

        if not usuario:
            print("Error: Usuario vacío.")
        elif " " in usuario:
            print("Error: El usuario no puede tener espacios.")
        elif len(clave) < 8:
            print("Error: La contraseña es muy corta (mínimo 8).")
        elif not any(c.isalpha() for c in clave):
            print("La contraseña debe contener al menos una letra.")
        elif not any(c.isdigit() for c in clave):
            print("La contraseña debe contener al menos un número.")
        else:
            return usuario, clave


def clasificar_numero():
    try:
        numero = int(input("¿Qué número quieres clasificar?: "))
    except ValueError:
        print("Error: Debes ingresar un número entero válido.")
        return
    print("Cero" if numero == 0 else ("Positivo" if numero > 0 else "Negativo"))
    if numero != 0:
        print("Par" if numero % 2 == 0 else "Impar")


def categoria_edad():
    try:
        edad = int(input("Ingresa tu edad: "))
    except ValueError:
        print("Error: Edad inválida.")
        return
    print("Niñez" if edad < 13 else "Adolescencia" if edad < 18 else "Adultez")


def calcular_tarifa():
    base = 200
    try:
        edad = int(input("Ingresa tu edad (0-120): "))
        dia = int(input("Día de la semana (1=Lun ... 7=Dom): "))
    except ValueError:
        print("Error: Edad o día inválidos.")
        return

    es_estudiante = input("¿Es estudiante? (Si/No): ").strip().lower() == "si"
    es_miembro = input("¿Es miembro? (Si/No): ").strip().lower() == "si"
    metodo_pago = input("Método de pago: E (efectivo) o T (tarjeta): ").strip().upper()

    recargo = base * 0.10 if dia in [6, 7] else 0
    descuentos = [
        50 if edad <= 12 else 20 if edad <= 17 else 30 if edad >= 65 else 0,
        15 if es_estudiante and edad >= 13 else 0,
        10 if es_miembro else 0,
        5 if metodo_pago == "E" else 0
    ]
    total_descuento = min(sum(descuentos), 60)
    total_final = base + recargo - (base * total_descuento / 100)

    print("----------------------------")
    print(f"Precio Base: ${base}")
    print(f"Recargos: ${recargo}")
    print(f"Descuento aplicado total: {total_descuento}%")
    print(f"TOTAL FINAL: ${total_final}")
    print("----------------------------")


def main():
    intentos = 0
    while intentos < 3:
        usuario, clave = pedir_usuario_clave()
        if usuario == "admin" and clave == "admin2026":
            print("¡Acceso concedido!")
            # Diccionario de opciones del menú
            menu = {
                "1": clasificar_numero,
                "2": categoria_edad,
                "3": calcular_tarifa,
                "4": lambda: "cerrar_sesion",
                "5": lambda: "salir_programa"
            }
            acceso = True
            while acceso:
                print("\n--- MENU ---")
                print("1. Clasificar numero\n2. Categoria de edad y permisos\n3. Calcular tarifa final (Pase Diario)\n4. Cerrar sesión\n5. Salir del programa")
                opcion = input("Selecciona una opcion (1-5): ")
                accion = menu.get(opcion)
                if accion:
                    resultado = accion()
                    if resultado == "cerrar_sesion":
                        print("¡¡Sesión cerrada!!")
                        acceso = False
                    elif resultado == "salir_programa":
                        print("¡¡Saliste del programa!!")
                        return
                else:
                    print("Opción inválida")
        else:
            intentos += 1
            print(f"Datos incorrectos. Te quedan {3 - intentos} intentos.")
    print("SISTEMA BLOQUEADO")


if __name__ == "__main__":
    main()