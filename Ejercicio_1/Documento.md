# Entorno Virtual en Python (Explicación Paso a Paso)

Este documento explica el código necesario para crear, activar y usar un entorno virtual en Python, detallando qué hace cada comando.

---

## 1. Verificar que Python esté instalado

Antes de crear un entorno virtual, es importante comprobar que Python está instalado en el sistema.

```bash
python --version
```

### Explicación
- `python` ejecuta el intérprete de Python.
- `--version` muestra la versión instalada.
- Si aparece una versión, Python está correctamente instalado.

---

## 2. Crear el entorno virtual

```bash
python -m venv venv
```

### Explicación
- `python`: ejecuta Python.
- `-m`: indica que se ejecuta un módulo.
- `venv`: módulo para crear entornos virtuales.
- `venv`: nombre de la carpeta del entorno virtual.

Este comando crea una carpeta llamada `venv` con un entorno aislado.

---

## 3. Activar el entorno virtual

### En Windows

```bash
venv\Scripts\activate
```

### En macOS o Linux

```bash
source venv/bin/activate
```

### Explicación
- Activa el entorno virtual.
- Al activarse, aparece `(venv)` en la terminal.

---

## 4. Instalar paquetes

```bash
pip install numpy
```

### Explicación
- `pip`: gestor de paquetes.
- `install`: indica instalación.
- `numpy`: paquete a instalar.

El paquete se instala solo en el entorno virtual.

---

## 5. Ver paquetes instalados

```bash
pip list
```

Muestra las librerías instaladas en el entorno activo.

---

## 6. Desactivar el entorno virtual

```bash
deactivate
```

Cierra el entorno virtual.

---

## 7. Eliminar el entorno virtual

Para eliminarlo, borra la carpeta `venv`.

---

## Conclusión

Los entornos virtuales permiten trabajar con proyectos de Python de forma ordenada y sin conflictos entre librerías.
