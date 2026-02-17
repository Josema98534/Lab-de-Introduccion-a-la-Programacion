# Explicación del programa

Este programa toma un número entero ingresado por el usuario y lo
convierte a diferentes sistemas numéricos:

-   Binario (base 2)
-   Octal (base 8)
-   Hexadecimal (base 16)

Las conversiones se realizan usando divisiones sucesivas y residuos.

------------------------------------------------------------------------

## Paso 1 -- Entrada del número

``` python
n = int(input("Introduce un número entero: "))
original = n
```

En esta parte se solicita al usuario un número.\
La función `input()` recibe el valor como texto, por lo que se usa
`int()` para convertirlo a entero.

Se guarda una copia en la variable `original` porque el valor de `n` se
modificará durante los cálculos.

------------------------------------------------------------------------

## Conversión a binario (base 2)

La conversión se basa en dividir el número entre 2 repetidamente.

``` python
while n > 0:
    r = n % 2
    bin_decimal = str(r) + bin_decimal
    n = n // 2
```

Proceso:

-   `n % 2` obtiene el residuo (0 o 1)
-   El residuo representa un dígito binario
-   Se concatena al inicio del resultado
-   `n // 2` reduce el número

El ciclo continúa hasta que `n` sea 0.

------------------------------------------------------------------------

## Conversión a octal (base 8)

Se aplica el mismo procedimiento, pero dividiendo entre 8.

``` python
r1 = n % 8
n = n // 8
```

Los residuos en este caso van de 0 a 7.

------------------------------------------------------------------------

## Conversión a hexadecimal (base 16)

En hexadecimal se utilizan números y letras.

``` python
caracteres_hexa = "0123456789ABCDEF"
```

Los valores mayores a 9 se representan con letras:

-   10 → A
-   11 → B
-   12 → C
-   etc.

Para obtener el carácter correcto:

``` python
bin_hexa = caracteres_hexa[r2] + bin_hexa
```

Aquí `r2` es un valor entre 0 y 15.\
Se usa como índice dentro del string.

Ejemplo:

Si `r2 = 10`, entonces:

``` python
caracteres_hexa[10] = 'A'
```

------------------------------------------------------------------------

## Error común

Si se escribe:

``` python
caracteres_hexa(r2)
```

Python interpreta que se intenta ejecutar una función.\
Sin embargo, `caracteres_hexa` es un string, no una función.

La forma correcta es:

``` python
caracteres_hexa[r2]
```

-   Corchetes → acceder a una posición
-   Paréntesis → llamar una función

------------------------------------------------------------------------

## Resumen

El programa:

1.  Recibe un número entero
2.  Aplica divisiones sucesivas
3.  Usa los residuos como dígitos
4.  Construye los resultados como cadenas

Este método permite realizar conversiones de bases de manera manual.
