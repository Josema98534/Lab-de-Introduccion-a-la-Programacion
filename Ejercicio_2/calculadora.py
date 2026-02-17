n = int(input("Introduce un número entero: "))
original = n

# BINARIO
bin_decimal = ""
if n == 0:
    bin_decimal = "0"

while n > 0:
    r = n % 2
    bin_decimal = str(r) + bin_decimal
    n = n // 2

# OCTAL
n = original
bin_octal = ""
if n == 0:
    bin_octal = "0"

while n > 0:
    r1 = n % 8
    bin_octal = str(r1) + bin_octal
    n = n // 8

# HEXADECIMAL
n = original
bin_hexa = ""
caracteres_hexa = "0123456789ABCDEF"

if n == 0:
    bin_hexa = "0"

while n > 0:
    r2 = n % 16
    bin_hexa = caracteres_hexa[r2] + bin_hexa
    n //= 16

print("Resultado en binario:", bin_decimal)
print("Resultado en octal:", bin_octal)
print("Resultado en hexa:", bin_hexa)
