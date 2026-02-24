intentos = 0

while intentos < 3:
    usuario = input("Usuario: ")
    clave = input("Contraseña: ")

    if usuario == "":
        print("Error: Usuario vacío.")
        continue
    
    elif " " in usuario:
        print("Error: El usuario no puede tener espacios.")
        continue

    elif len(clave) < 8:
        print("Error: La contraseña es muy corta (mínimo 8).")
        continue

    if not any(c.isalpha() for c in clave):
        print("La contraseña debe contener al menos una letra.")
        continue

    if not any(c.isdigit() for c in clave):
        print("La contraseña debe contener al menos un numero.")
        continue

    if usuario == "admin" and clave == "admin2026":
        print("¡Acceso concedido!")

        acceso = 1
        while acceso == 1:

            print("\n--- MENU ---")
            print("1. Clasificar numero")
            print("2. Categoria de edad y permisos")
            print("3. Calcular tarifa final")
            print("4. Cerrar sesión")
            print("5. Salir del programa")

            opcion = input("Selecciona una opcion (1-5): ")

            if opcion == "1":
                print("Clasificar numero")

            elif opcion == "2":
                print("Categoria de edad y permisos")

            elif opcion == "3":
                print("Calcular tarifa final")
            
            elif opcion == "4":
                print("¡¡Sesion cerrada!!")
                acceso = 0

            elif opcion == "5":
                print("¡¡Saliste del programa!!")
                acceso = -1
            
            else:
                print("Opcion Invalida")

        if acceso == -1:
            break

    else:
        intentos += 1
        print("Datos incorrectos.")
        print("Te quedan", 3 - intentos, "intentos.")

if intentos == 3:
    print("SISTEMA BLOQUEADO")