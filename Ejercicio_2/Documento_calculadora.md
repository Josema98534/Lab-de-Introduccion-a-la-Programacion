# Explicación relax del programa 😎

Este programita básicamente agarra un número entero que tú escribes y lo
traduce a:

-   Binario (base 2)
-   Octal (base 8)
-   Hexadecimal (base 16)

Nada mágico, pura matemática básica y divisiones.

------------------------------------------------------------------------

## 🟢 Paso 1 -- Pedir el número

``` python
n = int(input("Introduce un número entero: "))
original = n
```

Aquí solo le dices a Python:

"Oye, pídele algo al usuario y conviértelo a entero".

Luego guardamos una copia en `original` porque después vamos a destruir
`n` en los cálculos.

------------------------------------------------------------------------

## 🔵 Conversión a BINARIO (base 2)

La idea es simple:

Dividir entre 2 hasta que ya no se pueda.

``` python
while n > 0:
    r = n % 2
    bin_decimal = str(r) + bin_decimal
    n = n // 2
```

¿Qué está pasando?

-   `n % 2` → saca el residuo (0 o 1)
-   Ese residuo es un dígito binario
-   Lo vamos pegando al inicio del string
-   `n // 2` → reduce el número

Esto se repite hasta llegar a 0.

------------------------------------------------------------------------

## 🟡 Conversión a OCTAL (base 8)

Exactamente la misma lógica... pero ahora entre 8.

``` python
r1 = n % 8
n = n // 8
```

El residuo ahora va de 0 a 7.

------------------------------------------------------------------------

## 🔴 Conversión a HEXADECIMAL (base 16)

Misma historia... PERO aquí aparece algo interesante:

``` python
caracteres_hexa = "0123456789ABCDEF"
```

Hexadecimal usa letras después del 9:

-   10 → A
-   11 → B
-   12 → C
-   etc.

Entonces hacemos esto:

``` python
bin_hexa = caracteres_hexa[r2] + bin_hexa
```

Aquí `r2` es un número entre 0 y 15.

Lo usamos como índice dentro del string.

Ejemplo:

-   Si r2 = 10 → caracteres_hexa\[10\] = 'A'

------------------------------------------------------------------------

## ⚠️ El error que te salió

Si escribes:

``` python
caracteres_hexa(r2)
```

Python cree que intentas **llamar una función**.

Pero eso es un string, no una función → BOOM 💥 error.

La forma correcta es:

``` python
caracteres_hexa[r2]
```

Corchetes = acceder a posición\
Paréntesis = ejecutar función

------------------------------------------------------------------------

## ✅ Resumen ultra rápido

El programa:

1.  Toma un número
2.  Lo divide repetidamente
3.  Usa residuos como dígitos
4.  Construye strings desde atrás hacia adelante

Y listo, conversiones de bases hechas a mano como en examen de
programación 😏
