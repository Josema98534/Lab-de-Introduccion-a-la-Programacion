intentos = 0

while intentos < 3:
    usuario = input("Usuario: ")
    clave = input("Contraseña: ")

    if usuario == "":
        print("Error: Usuario vacío.")
    
    elif " " in usuario:
        print("Error: El usuario no puede tener espacios.")

    elif len(clave) < 8:
        print("Error: La contraseña es muy corta (mínimo 8).")
        continue

    for letra in clave:
        if letra.isdigit():
            print("La contraseña debe contener al menos una letra.")
            break

        elif letra.isalpha():
            print("La contraseña debe contener al menos un numero.")
            break

    else:
        continue
    if usuario == "admin" and clave == "admin2026":
            print("¡Acceso concedido!")
            intentos = 0 
            break 
    else:
        intentos = intentos + 1
        print("Datos incorrectos.")
        
        print("Te quedan", 3 - intentos, "intentos.")

if intentos == 3:
    print("SISTEMA BLOQUEADO")
    