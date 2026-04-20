
import random
from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super_market_v2"

# ==============================
# 🛒 BASE DE PRODUCTOS (MEJORADA)
# ==============================
PRODUCTOS = {
    "127846005981": {"nombre": "🥛 Leche Premium 1L", "precio": 1.80, "categoria": "Lácteos"},
    "456": {"nombre": "🍎 Manzana Orgánica", "precio": 3.50, "categoria": "Frutas"},
    "789": {"nombre": "🐟 Salmón Noruego", "precio": 18.90, "categoria": "Carnes"},
    "101": {"nombre": "🥖 Pan Artesanal", "precio": 4.25, "categoria": "Panadería"},
    "202": {"nombre": "🧴 Detergente Bio", "precio": 8.50, "categoria": "Limpieza"}
}

# ==============================
# 🔧 FUNCIONES AUXILIARES
# ==============================
def obtener_carrito():
    if "carrito" not in session:
        session["carrito"] = []
    return session["carrito"]

def calcular_totales(items):
    subtotal = sum(p["precio"] for p in items)
    iva = subtotal * 0.16
    total = subtotal + iva
    return subtotal, iva, total

def generar_producto_fake(codigo):
    precio = round(random.uniform(5, 100), 2)
    return {
        "nombre": f"❓ Producto X-{codigo[-3:]}",
        "precio": precio,
        "categoria": "Desconocido"
    }

# ==============================
# 🌐 RUTAS
# ==============================
@app.route("/")
def inicio():
    return redirect(url_for("vista_escaneo"))

@app.route("/escaneo")
def vista_escaneo():
    return render_template("escaneo.html")

@app.route("/catalogo")
def vista_catalogo():
    return render_template("catalogo.html", productos=PRODUCTOS)

@app.route("/agregar/<codigo>")
def agregar_producto(codigo):
    carrito = obtener_carrito()

    producto = PRODUCTOS.get(codigo, generar_producto_fake(codigo))

    carrito.append(producto)
    session.modified = True

    return redirect(url_for("ver_carrito"))

@app.route("/carrito")
def ver_carrito():
    items = obtener_carrito()
    subtotal, iva, total = calcular_totales(items)

    return render_template(
        "carrito.html",
        items=items,
        subtotal=subtotal,
        iva=iva,
        total=total
    )

@app.route("/pago-exitoso")
def pago_exitoso():
    items = obtener_carrito()

    if not items:
        return redirect(url_for("vista_escaneo"))

    subtotal, iva, total = calcular_totales(items)

    session.pop("carrito", None)

    return render_template(
        "exito.html",
        items=items,
        subtotal=subtotal,
        iva=iva,
        total=total
    )

# ==============================
# 🚀 EJECUCIÓN
# ==============================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
