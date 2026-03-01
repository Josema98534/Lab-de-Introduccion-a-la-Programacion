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
        print("La contraseña debe contener al menos un número.")
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

            # Clasificacion de un numero
            if opcion == "1":
                print("Clasificar numero")

                entrada = input("¿Qué número quieres clasificar?: ")

                if not entrada.lstrip("-").isdigit():
                    print("Error: Debes ingresar un número entero válido.")
                else:
                    numero_entero = int(entrada)

                    if numero_entero == 0:
                        print("El numero es cero")
                    else:
                        if numero_entero < 0:
                            print("El numero es negativo")
                        else:
                            print("El numero es positivo")

                        if numero_entero % 2 == 0:
                            print("El numero es par")
                        else:
                            print("El numero es impar")

            elif opcion == "2":
                print("Categoria de edad y permisos")

                edad_input = input("Ingresa tu edad: ")

                if not edad_input.isdigit():
                    print("Error: Debes ingresar una edad válida.")
                    continue

                edad = int(edad_input)

                # Clasificación de edad
                if edad < 13:
                    print("Clasificación: Niñez")
                elif edad < 18:
                    print("Clasificación: Adolescencia")
                else:
                    print("Clasificación: Adultez")

                if edad >= 13:
                    print("Puede registrarse")
                else:
                    print("No puede registrarse, necesita ser mayor o igual a 13 años")
                    # Recordatorio del continue

                identificacion = input("¿Cuenta con identificacion? (si/no): ")

                if identificacion == "si":
                    print("Usted si puede realizar la compra")

                elif identificacion == "no":
                    tutor = input("¿Cuenta con un tutor mayor de 18 años? (si/no): ")

                    if tutor == "si":
                        print("Sí puede realizar la compra con su tutor mayor de edad.")
                    elif tutor == "no":
                        print("No puede realizar la compra ya que es menor de edad y requiere un tutor mayor de edad.")
                    else:
                        print("Respuesta invalida sobre el tutor.")
                else:
                    print("Respuesta invalida en identificacion")

                licencia = input("¿Cuenta con licencia? (si/no): ")

                while licencia != "si" and licencia != "no":
                    print("Error, escribe solo si o no")
                    licencia = input("¿Cuenta con licencia? (si/no): ")

                if licencia == "si":
                    print("Perfecto, usted si puede conducir")
                else:
                    print("¡No puede conducir, es necesario tener una licencia!")

            #Calcular tarifa final
            elif opcion == "3":
                print("Calcular tarifa final")
            
            #cerrar sesion
            elif opcion == "4":
                print("¡¡Sesion cerrada!!")
                acceso = 0

            #salir
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