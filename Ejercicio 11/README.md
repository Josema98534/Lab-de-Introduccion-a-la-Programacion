# 🚀 Escáner PRO Mejorado --- QR & Código de Barras

Aplicación web optimizada para escanear códigos QR y de barras
directamente desde tu navegador con mayor rendimiento, mejor interfaz y
nuevas funcionalidades.

------------------------------------------------------------------------

# ✨ Nuevas mejoras

-   🚀 Interfaz más moderna y limpia
-   ⚡ Mejor rendimiento en escaneo continuo
-   🔒 Validación de URLs antes de abrirlas
-   🧾 Registro básico de últimos escaneos
-   🎯 Indicador visual al detectar código
-   🔕 Opción para desactivar sonido

------------------------------------------------------------------------

# 📷 Características

-   Acceso a cámara en tiempo real
-   Compatible con móvil y PC
-   Soporte para múltiples formatos:
    -   QR Code
    -   EAN
    -   CODE128
-   Detección automática de enlaces
-   Evita duplicados

------------------------------------------------------------------------

# 🧠 Tecnologías

-   Backend: Flask (Python)
-   Frontend: HTML5, CSS3, JavaScript
-   Librería: ZXing

------------------------------------------------------------------------

# 📦 Instalación rápida

``` bash
git clone <repo>
cd proyecto
pip install flask
```

------------------------------------------------------------------------

# ▶️ Ejecutar

``` bash
python app.py
```

Abrir en navegador: http://localhost:5000

------------------------------------------------------------------------

# 📱 Uso en celular

Para usar cámara en móvil necesitas HTTPS.

## Opción rápida con ngrok

``` bash
pip install flask-ngrok
```

Agregar en tu código:

``` python
from flask_ngrok import run_with_ngrok
run_with_ngrok(app)
```

------------------------------------------------------------------------

# 🧩 Estructura

-   app.py → servidor Flask
-   HTML embebido → interfaz
-   JS → lógica de escaneo

------------------------------------------------------------------------

# 🐞 Problemas comunes

## Cámara no funciona

→ Usa HTTPS (ngrok)

## No escanea bien

→ Mejora iluminación

------------------------------------------------------------------------

# 🚀 Futuras mejoras

-   Base de datos de productos
-   Exportar historial
-   Login de usuarios
-   Versión app móvil

------------------------------------------------------------------------

# 📄 Licencia

Uso libre para aprendizaje y proyectos personales.

------------------------------------------------------------------------

# 💡 Nota

Este proyecto es ideal como base para sistemas reales como inventarios o
apps comerciales.
