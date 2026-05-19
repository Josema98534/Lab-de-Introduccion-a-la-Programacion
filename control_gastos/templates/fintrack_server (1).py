#!/usr/bin/env python3
"""
============================================================
FINTRACK – Servidor Local (Python)
============================================================
Descripción  : Lanza un servidor HTTP local para servir fintrack.html
               y exponer una API REST mínima para exportar PDF.
               Ahora incluye sistema de LOGIN con base de datos SQLite.
               El servidor abre login.html primero; solo puede acceder
               a fintrack.html quien tenga sesión activa.

Paradigma    : Programación Estructurada y Funcional básica.
Lenguaje     : Python 3.8+
IDE          : VS Code
IA           : Claude (Anthropic) — apoyo en optimización y documentación

Uso          :
  python fintrack_server.py

Requisitos   :
  - Python 3.8+
  - (Opcional) reportlab para exportación PDF:
      pip install reportlab

Puerto por defecto : 5000
Accede en         : http://localhost:5000
============================================================
"""

# ── Librerías estándar de Python (sin librerías externas avanzadas) ──────────
import http.server
import socketserver
import webbrowser
import os
import json
import sys
import io
import sqlite3        # ← NUEVO: base de datos local
import hashlib        # ← NUEVO: para hashear contraseñas
import secrets        # ← NUEVO: para generar tokens de sesión
from pathlib import Path
from urllib.parse import urlparse, parse_qs


# ── SECCIÓN 1: CONFIGURACIÓN GLOBAL ─────────────────────────────────────────

PUERTO        = 5000
ARCHIVO_HTML  = "fintrack.html"
ARCHIVO_LOGIN = "login.html"             # ← NUEVO: login como página de entrada
DIRECTORIO    = Path(__file__).parent
DB_PATH       = DIRECTORIO / "fintrack.db"  # ← NUEVO: ruta de la base de datos

# Diccionario en memoria para sesiones activas: { token: user_id }
sesiones_activas = {}


# ── SECCIÓN 2: VERIFICACIÓN DE DEPENDENCIA OPCIONAL (reportlab) ─────────────

PDF_DISPONIBLE = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import cm
    PDF_DISPONIBLE = True
except ImportError:
    pass


# ── SECCIÓN 3 (NUEVA): BASE DE DATOS Y AUTENTICACIÓN ────────────────────────

def inicializar_bd():
    """
    Crea la base de datos SQLite y las tablas si no existen.
    Inserta los usuarios predeterminados (morgan y chagouaz).
    """
    conexion = sqlite3.connect(str(DB_PATH))
    cursor   = conexion.cursor()

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT    UNIQUE NOT NULL,
            email      TEXT,
            password   TEXT    NOT NULL,
            role       TEXT    DEFAULT 'student',
            created_at TEXT    DEFAULT (datetime('now'))
        )
    """)

    # Tabla de actividad (registro de acciones por usuario)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            action     TEXT    NOT NULL,
            detail     TEXT,
            timestamp  TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Insertar usuarios predeterminados si no existen
    usuarios_default = [
        ('morgan',   'morgan@fintrack.com',   _hashear('morgan123'),   'admin'),
        ('chagouaz', 'chagouaz@fintrack.com', _hashear('chagouaz123'), 'admin'),
    ]
    for username, email, password, role in usuarios_default:
        cursor.execute(
            "INSERT OR IGNORE INTO users (username, email, password, role) VALUES (?,?,?,?)",
            (username, email, password, role)
        )

    conexion.commit()
    conexion.close()


def _hashear(password):
    """Aplica SHA-256 a la contraseña. Siempre usar esta función."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def registrar_usuario(username, email, password):
    """
    Registra un nuevo usuario en la base de datos.
    Retorna (True, user_id) si tuvo éxito, o (False, mensaje_error).
    """
    if not username or not password:
        return False, "Usuario y contraseña son obligatorios."

    conexion = sqlite3.connect(str(DB_PATH))
    cursor   = conexion.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?,?,?)",
            (username, email or '', _hashear(password))
        )
        user_id = cursor.lastrowid
        # Registrar acción
        cursor.execute(
            "INSERT INTO activity (user_id, action, detail) VALUES (?,?,?)",
            (user_id, 'register', 'Nuevo usuario registrado')
        )
        conexion.commit()
        return True, user_id

    except sqlite3.IntegrityError:
        return False, "Ese nombre de usuario ya existe."

    finally:
        conexion.close()


def autenticar_usuario(username, password):
    """
    Verifica las credenciales del usuario.
    Retorna (True, user_id, role) si son correctas, o (False, None, None).
    """
    conexion = sqlite3.connect(str(DB_PATH))
    cursor   = conexion.cursor()

    cursor.execute(
        "SELECT id, role FROM users WHERE username=? AND password=?",
        (username, _hashear(password))
    )
    fila = cursor.fetchone()
    conexion.close()

    if fila:
        return True, fila[0], fila[1]
    return False, None, None


def crear_sesion(user_id, username):
    """
    Genera un token de sesión único y lo almacena en el diccionario en memoria.
    Registra el login en la tabla activity.
    Retorna el token generado.
    """
    token = secrets.token_hex(32)   # 64 caracteres hexadecimales aleatorios
    sesiones_activas[token] = {'user_id': user_id, 'username': username}

    # Guardar evento en la base de datos
    conexion = sqlite3.connect(str(DB_PATH))
    cursor   = conexion.cursor()
    cursor.execute(
        "INSERT INTO activity (user_id, action, detail) VALUES (?,?,?)",
        (user_id, 'login', 'Inicio de sesión exitoso')
    )
    conexion.commit()
    conexion.close()

    return token


def sesion_valida(token):
    """
    Verifica si un token de sesión existe y es válido.
    Retorna True si la sesión es activa, False en caso contrario.
    """
    if not token:
        return False
    return token in sesiones_activas


def cerrar_sesion(token):
    """
    Elimina el token de sesión del diccionario en memoria.
    Registra el logout en la base de datos.
    """
    if token in sesiones_activas:
        user_id = sesiones_activas[token]['user_id']

        conexion = sqlite3.connect(str(DB_PATH))
        cursor   = conexion.cursor()
        cursor.execute(
            "INSERT INTO activity (user_id, action) VALUES (?,?)",
            (user_id, 'logout')
        )
        conexion.commit()
        conexion.close()

        del sesiones_activas[token]


def obtener_token_de_cookie(headers):
    """
    Extrae el token de sesión de la cabecera Cookie.
    Busca el par 'session=TOKEN'.
    Retorna el token como string, o None si no existe.
    """
    cookie_header = headers.get('Cookie', '')
    for parte in cookie_header.split(';'):
        parte = parte.strip()
        if parte.startswith('session='):
            return parte[len('session='):]
    return None


# ── SECCIÓN 4: FUNCIONES DE NEGOCIO (LÓGICA FINANCIERA) ─────────────────────

def calcular_totales(transacciones):
    """
    Recibe la lista de transacciones y calcula:
      - total de gastos (type == 'expense')
      - total de ingresos (type == 'income')
    Retorna una tupla (gastos, ingresos) usando un bucle for.
    """
    gastos   = 0.0
    ingresos = 0.0

    for tx in transacciones:
        tipo  = tx.get('type', '')
        monto = tx.get('amount', 0.0)

        if tipo == 'expense':
            gastos   += monto
        elif tipo == 'income':
            ingresos += monto

    return gastos, ingresos


def ordenar_por_fecha(transacciones):
    """
    Ordena una lista de transacciones por fecha de forma descendente
    usando el algoritmo de selección con for.
    """
    lista = transacciones[:]
    n = len(lista)

    for i in range(n - 1):
        max_idx = i
        for j in range(i + 1, n):
            if lista[j].get('date', '') > lista[max_idx].get('date', ''):
                max_idx = j
        if max_idx != i:
            lista[i], lista[max_idx] = lista[max_idx], lista[i]

    return lista


def validar_datos_pdf(datos):
    """Verifica que el cuerpo de la petición tenga la estructura esperada."""
    if 'transactions' not in datos:
        return False
    if not isinstance(datos['transactions'], list):
        return False
    return True


# ── SECCIÓN 5: FUNCIONES DE GENERACIÓN DE PDF ───────────────────────────────

def construir_tabla_resumen(story, estilos, saldo_inicial, gastos, ingresos):
    """Agrega al 'story' la tabla de resumen financiero."""
    saldo_final = saldo_inicial + ingresos - gastos

    datos_tabla = [
        ["Concepto",       "Monto"],
        ["Saldo Inicial",  "€{:,.2f}".format(saldo_inicial)],
        ["Total Ingresos", "€{:,.2f}".format(ingresos)],
        ["Total Gastos",   "€{:,.2f}".format(gastos)],
        ["Saldo Actual",   "€{:,.2f}".format(saldo_final)],
    ]

    tabla = Table(datos_tabla, colWidths=[8 * cm, 6 * cm])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1C2463')),
        ('TEXTCOLOR',  (0, 0), (-1, 0), colors.white),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 10),
        ('ALIGN',      (1, 0), (1, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8F9FB'), colors.white]),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E6ED')),
        ('PADDING',    (0, 0), (-1, -1), 8),
    ]))

    story.append(tabla)
    story.append(Spacer(1, 0.8 * cm))


def construir_tabla_transacciones(story, estilos, transacciones_ordenadas):
    """Agrega al 'story' la tabla detallada de transacciones."""
    story.append(Paragraph("Listado de Transacciones", estilos['Heading2']))
    story.append(Spacer(1, 0.2 * cm))

    if len(transacciones_ordenadas) == 0:
        story.append(Paragraph("No hay transacciones registradas.", estilos['Normal']))
        return

    datos_tabla = [["Fecha", "Descripción", "Categoría", "Tipo", "Monto"]]

    for tx in transacciones_ordenadas:
        tipo  = "Ingreso" if tx.get('type') == 'income' else "Gasto"
        monto = "€{:,.2f}".format(tx.get('amount', 0.0))
        datos_tabla.append([
            tx.get('date',     '—'),
            tx.get('desc',     '—'),
            tx.get('category', '—'),
            tipo,
            monto,
        ])

    tabla = Table(
        datos_tabla,
        colWidths=[2.8 * cm, 5.5 * cm, 3 * cm, 2.2 * cm, 3 * cm],
        repeatRows=1
    )
    tabla.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), colors.HexColor('#1C2463')),
        ('TEXTCOLOR',     (0, 0), (-1, 0), colors.white),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 9),
        ('ALIGN',         (4, 0), (4, -1), 'RIGHT'),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [colors.HexColor('#F8F9FB'), colors.white]),
        ('GRID',          (0, 0), (-1, -1), 0.3, colors.HexColor('#E2E6ED')),
        ('PADDING',       (0, 0), (-1, -1), 6),
    ]))
    story.append(tabla)


def generar_pdf(buffer, transacciones, saldo_inicial):
    """Función principal de generación de PDF."""
    gastos, ingresos = calcular_totales(transacciones)
    transacciones_ordenadas = ordenar_por_fecha(transacciones)

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm, leftMargin=2 * cm,
        topMargin=2 * cm,   bottomMargin=2 * cm,
        title="FinTrack – Informe Financiero"
    )

    estilos = getSampleStyleSheet()
    story   = []

    estilo_titulo = ParagraphStyle(
        'FinTitle',
        parent=estilos['Title'],
        fontSize=24,
        textColor=colors.HexColor('#1C2463'),
        spaceAfter=6,
    )
    story.append(Paragraph("FinTrack", estilo_titulo))
    story.append(Paragraph("Informe Financiero Detallado", estilos['Normal']))
    story.append(Spacer(1, 0.5 * cm))

    construir_tabla_resumen(story, estilos, saldo_inicial, gastos, ingresos)
    construir_tabla_transacciones(story, estilos, transacciones_ordenadas)

    story.append(Spacer(1, 1 * cm))
    estilo_pie = ParagraphStyle(
        'pie',
        parent=estilos['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    story.append(Paragraph("© 2024 FinTrack. Todos los derechos reservados.", estilo_pie))
    documento.build(story)


# ── SECCIÓN 6: FUNCIONES DE RESPUESTA HTTP ───────────────────────────────────

def enviar_respuesta_json(manejador, codigo, datos):
    """Envía una respuesta HTTP con cuerpo en formato JSON."""
    cuerpo = json.dumps(datos, ensure_ascii=False).encode('utf-8')

    manejador.send_response(codigo)
    manejador.send_header("Content-Type", "application/json; charset=utf-8")
    manejador.send_header("Content-Length", str(len(cuerpo)))
    manejador.send_header("Access-Control-Allow-Origin", "*")
    manejador.end_headers()
    manejador.wfile.write(cuerpo)


def manejar_estado(manejador):
    """Responde a GET /api/status con el estado actual del servidor."""
    datos = {
        "status":         "ok",
        "pdf_disponible": PDF_DISPONIBLE,
        "version":        "3.0",
        "sesiones":       len(sesiones_activas)
    }
    enviar_respuesta_json(manejador, 200, datos)


def manejar_exportar_pdf(manejador):
    """
    Recibe un POST con JSON de transacciones y responde con un archivo PDF.
    Requiere sesión activa.
    """
    # Verificar sesión antes de generar PDF
    token = obtener_token_de_cookie(manejador.headers)
    if not sesion_valida(token):
        enviar_respuesta_json(manejador, 401, {"error": "Sesión no válida. Inicia sesión primero."})
        return

    if not PDF_DISPONIBLE:
        enviar_respuesta_json(manejador, 503, {
            "error": "reportlab no instalado. Ejecuta: pip install reportlab"
        })
        return

    longitud = int(manejador.headers.get('Content-Length', 0))
    cuerpo   = manejador.rfile.read(longitud)

    try:
        datos = json.loads(cuerpo)
    except json.JSONDecodeError:
        enviar_respuesta_json(manejador, 400, {"error": "JSON inválido en el cuerpo de la petición"})
        return

    if not validar_datos_pdf(datos):
        enviar_respuesta_json(manejador, 400, {"error": "Estructura de datos incorrecta"})
        return

    transacciones = datos.get("transactions", [])
    saldo_inicial = datos.get("saldoInicial", 0.0)

    buffer = io.BytesIO()
    generar_pdf(buffer, transacciones, saldo_inicial)
    bytes_pdf = buffer.getvalue()

    manejador.send_response(200)
    manejador.send_header("Content-Type", "application/pdf")
    manejador.send_header("Content-Disposition", 'attachment; filename="fintrack_informe.pdf"')
    manejador.send_header("Content-Length", str(len(bytes_pdf)))
    manejador.send_header("Access-Control-Allow-Origin", "*")
    manejador.end_headers()
    manejador.wfile.write(bytes_pdf)


# ── SECCIÓN 7 (NUEVA): MANEJADORES DE AUTENTICACIÓN ─────────────────────────

def manejar_login(manejador):
    """
    POST /api/login
    Body JSON esperado: { "username": "...", "password": "..." }
    Si las credenciales son correctas, responde con el token de sesión
    y lo establece como cookie.
    """
    longitud = int(manejador.headers.get('Content-Length', 0))
    cuerpo   = manejador.rfile.read(longitud)

    try:
        datos = json.loads(cuerpo)
    except json.JSONDecodeError:
        enviar_respuesta_json(manejador, 400, {"error": "JSON inválido"})
        return

    username = datos.get('username', '').strip()
    password = datos.get('password', '').strip()

    ok, user_id, role = autenticar_usuario(username, password)

    if ok:
        token = crear_sesion(user_id, username)
        cuerpo_resp = json.dumps({
            "ok":       True,
            "username": username,
            "role":     role,
            "token":    token
        }, ensure_ascii=False).encode('utf-8')

        manejador.send_response(200)
        manejador.send_header("Content-Type", "application/json; charset=utf-8")
        manejador.send_header("Content-Length", str(len(cuerpo_resp)))
        manejador.send_header("Access-Control-Allow-Origin", "*")
        # Cookie de sesión (HttpOnly — no accesible por JS)
        manejador.send_header("Set-Cookie", "session={}; Path=/; HttpOnly".format(token))
        # Cookie con el nombre de usuario (legible por JS en fintrack.html
        # para separar el localStorage de cada usuario con clave única)
        manejador.send_header("Set-Cookie", "ft_user={}; Path=/".format(username))
        manejador.end_headers()
        manejador.wfile.write(cuerpo_resp)
    else:
        enviar_respuesta_json(manejador, 401, {"ok": False, "error": "Usuario o contraseña incorrectos."})


def manejar_registro(manejador):
    """
    POST /api/register
    Body JSON esperado: { "username": "...", "email": "...", "password": "..." }
    Crea un nuevo usuario y lo deja listo para iniciar sesión.
    """
    longitud = int(manejador.headers.get('Content-Length', 0))
    cuerpo   = manejador.rfile.read(longitud)

    try:
        datos = json.loads(cuerpo)
    except json.JSONDecodeError:
        enviar_respuesta_json(manejador, 400, {"error": "JSON inválido"})
        return

    username = datos.get('username', '').strip()
    email    = datos.get('email',    '').strip()
    password = datos.get('password', '').strip()

    ok, resultado = registrar_usuario(username, email, password)

    if ok:
        enviar_respuesta_json(manejador, 201, {
            "ok":      True,
            "mensaje": "Usuario '{}' creado correctamente.".format(username)
        })
    else:
        enviar_respuesta_json(manejador, 400, {"ok": False, "error": resultado})


def manejar_logout(manejador):
    """
    POST /api/logout
    Elimina la sesión activa y borra la cookie.
    """
    token = obtener_token_de_cookie(manejador.headers)
    cerrar_sesion(token)

    cuerpo_resp = json.dumps({"ok": True, "mensaje": "Sesión cerrada."}).encode('utf-8')
    manejador.send_response(200)
    manejador.send_header("Content-Type", "application/json; charset=utf-8")
    manejador.send_header("Content-Length", str(len(cuerpo_resp)))
    manejador.send_header("Access-Control-Allow-Origin", "*")
    # Borrar ambas cookies
    manejador.send_header("Set-Cookie", "session=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT")
    manejador.send_header("Set-Cookie", "ft_user=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT")
    manejador.end_headers()
    manejador.wfile.write(cuerpo_resp)


def manejar_verificar_sesion(manejador):
    """
    GET /api/session
    Responde si el token de la cookie es válido o no.
    Usado por fintrack.html al cargar para saber si el usuario está autenticado.
    """
    token = obtener_token_de_cookie(manejador.headers)
    if sesion_valida(token):
        info = sesiones_activas[token]
        enviar_respuesta_json(manejador, 200, {
            "ok":       True,
            "username": info['username']
        })
    else:
        enviar_respuesta_json(manejador, 401, {"ok": False})


# ── SECCIÓN 8: MANEJADOR HTTP ────────────────────────────────────────────────

class ManejadorFinTrack(http.server.SimpleHTTPRequestHandler):
    """
    Manejador HTTP personalizado de FinTrack.

    Rutas disponibles:
      GET  /                  → login.html  (página de entrada)
      GET  /fintrack.html     → fintrack.html (solo con sesión activa)
      GET  /api/status        → JSON de estado del servidor
      GET  /api/session       → Verificar sesión activa
      POST /api/login         → Autenticar usuario
      POST /api/register      → Registrar nuevo usuario
      POST /api/logout        → Cerrar sesión
      POST /api/export-pdf    → Generar PDF (requiere sesión)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORIO), **kwargs)

    def log_message(self, formato, *args):
        print("  [{}] {}".format(self.address_string(), formato % args))

    def do_GET(self):
        ruta = urlparse(self.path).path

        # Raíz → redirigir siempre al login
        if ruta in ('/', ''):
            self.path = '/' + ARCHIVO_LOGIN
            super().do_GET()
            return

        # fintrack.html solo con sesión activa
        if ruta == '/' + ARCHIVO_HTML or ruta == '/' + ARCHIVO_HTML.replace('.html', ''):
            token = obtener_token_de_cookie(self.headers)
            if not sesion_valida(token):
                # Sin sesión: redirigir al login
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
                return
            # Con sesión: servir el archivo normalmente
            super().do_GET()
            return

        # API de estado
        if ruta == '/api/status':
            manejar_estado(self)
            return

        # API de sesión
        if ruta == '/api/session':
            manejar_verificar_sesion(self)
            return

        # Cualquier otro archivo estático (CSS, JS, imágenes, etc.)
        super().do_GET()

    def do_POST(self):
        ruta = urlparse(self.path).path

        if ruta == '/api/login':
            manejar_login(self)
        elif ruta == '/api/register':
            manejar_registro(self)
        elif ruta == '/api/logout':
            manejar_logout(self)
        elif ruta == '/api/export-pdf':
            manejar_exportar_pdf(self)
        else:
            enviar_respuesta_json(self, 404, {"error": "Ruta no encontrada: " + ruta})

    def do_OPTIONS(self):
        """Maneja preflight requests de CORS."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


# ── SECCIÓN 9: FUNCIÓN PRINCIPAL ────────────────────────────────────────────

def verificar_archivos_html():
    """
    Verifica que tanto login.html como fintrack.html existan.
    Si falta alguno, muestra un error y termina el programa.
    """
    for archivo in [ARCHIVO_LOGIN, ARCHIVO_HTML]:
        ruta = DIRECTORIO / archivo
        if not ruta.exists():
            print("=" * 60)
            print("  ERROR: No se encontró '{}'".format(archivo))
            print("  Directorio buscado: {}".format(DIRECTORIO))
            print("  Asegúrate de que {} esté en la misma carpeta.".format(archivo))
            print("=" * 60)
            sys.exit(1)


def mostrar_banner():
    """Imprime la información de inicio del servidor en la consola."""
    estado_pdf = "✅ Disponible" if PDF_DISPONIBLE else "⚠️  No disponible (pip install reportlab)"

    print("=" * 60)
    print("  FinTrack – Servidor Local v3.0  (con Login + SQLite)")
    print("=" * 60)
    print("  Directorio  : {}".format(DIRECTORIO))
    print("  Base de datos: {}".format(DB_PATH))
    print("  Puerto      : {}".format(PUERTO))
    print("  PDF Export  : {}".format(estado_pdf))
    print("-" * 60)
    print("  🌐 Abre en tu navegador: http://localhost:{}".format(PUERTO))
    print()
    print("  Usuarios predeterminados:")
    print("    morgan   /  morgan123   (admin)")
    print("    chagouaz /  chagouaz123 (admin)")
    print()
    print("  Presiona Ctrl+C para detener el servidor.")
    print("=" * 60)


def iniciar_servidor():
    """Configura el servidor TCP y lo arranca en bucle indefinido."""
    servidor = socketserver.TCPServer(("", PUERTO), ManejadorFinTrack)
    servidor.allow_reuse_address = True

    # Abrir navegador apuntando al login
    webbrowser.open("http://localhost:{}".format(PUERTO))

    try:
        print("  Servidor activo. Esperando conexiones...\n")
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  👋 Servidor detenido. ¡Hasta pronto!")
        servidor.shutdown()
        sys.exit(0)


# ── PUNTO DE ENTRADA ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    inicializar_bd()          # Paso 1: crear/verificar base de datos SQLite
    verificar_archivos_html() # Paso 2: comprobar que existen login.html y fintrack.html
    mostrar_banner()          # Paso 3: mostrar información de inicio
    iniciar_servidor()        # Paso 4: arrancar el servidor en bucle