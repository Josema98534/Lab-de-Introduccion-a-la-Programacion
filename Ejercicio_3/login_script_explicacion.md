# Explicación del Script de Login

Este script es un sistema básico de login que valida usuario y contraseña con varias reglas. Aquí te explico paso a paso cómo funciona:

---

## 1. Contador de intentos
```python
intentos = 0
```
Se inicializa un contador de intentos en cero. Esto permite controlar cuántas veces el usuario puede intentar entrar antes de que el sistema se bloquee.

---

## 2. Ciclo principal
```python
while intentos < 3:
```
El `while` permite que el usuario intente ingresar hasta **3 veces**. Si supera los 3 intentos, el sistema se bloquea.

---

## 3. Pedir usuario y contraseña
```python
usuario = input("Usuario: ")
clave = input("Contraseña: ")
```
Se solicitan los datos al usuario.

- Si el **usuario está vacío**: muestra un error.
- Si el **usuario tiene espacios**: muestra un error.

---

## 4. Validación de contraseña
- La contraseña debe tener **mínimo 8 caracteres**.
- Debe contener **al menos una letra**.
- Debe contener **al menos un número**.

Si no cumple alguna de estas reglas, se muestra el error correspondiente y se vuelve a pedir la información.

---

## 5. Verificación de acceso
```python
if usuario == "admin" and clave == "admin2026":
```
Solo el usuario `admin` con la contraseña `admin2026` puede ingresar. Si las credenciales son correctas:

- Se muestra `¡Acceso concedido!`
- Se rompe el ciclo (`break`) y se restablecen los intentos.

---

## 6. Manejo de intentos fallidos
Si los datos son incorrectos:

- Se suma 1 al contador de intentos.
- Se informa al usuario cuántos intentos le quedan.

```python
intentos = intentos + 1
print("Te quedan", 3 - intentos, "intentos.")
```

---

## 7. Bloqueo del sistema
Si el usuario falla **3 veces seguidas**, el sistema se bloquea:

```python
if intentos == 3:
    print("SISTEMA BLOQUEADO")
```

---

## Resumen
- Limita el número de intentos a 3.
- Valida usuario y contraseña con reglas básicas.
- Solo permite el acceso a `admin` con `admin2026`.
- Informa errores claros sobre usuario vacío, espacios o contraseñas débiles.
- Bloquea el sistema después de 3 intentos fallidos.

Este script es sencillo pero efectivo para entender **cómo manejar login, validaciones y control de intentos** en Python.
