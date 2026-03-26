import tkinter as tk
from tkinter import messagebox
import math

# ==========================================
# CONFIGURACIÓN ESTÉTICA (Paleta Neón)
# ==========================================
# Colores HEX exactos para lograr el efecto de la imagen
COLOR_FONDO_APP = "#050505"   # Negro profundo para contraste
COLOR_TEXTO = "#FFFFFF"       # Blanco puro

# Definición de gradientes internos y colores de borde neón por card
CARDS_CONFIG = [
    {
        "titulo": "Card One",
        "texto": "Clasificador de Números: Determina si es Positivo, Negativo, Par o Impar.",
        "color_neon": "#FF4444",      # Rojo Neón
        "gradiente": ("#2a0000", "#FF4444") # (Oscuro arriba, Claro abajo)
    },
    {
        "titulo": "Card Two",
        "texto": "Categoría de Edad: Clasifica en Niñez, Adolescencia o Adultez.",
        "color_neon": "#CC44FF",      # Morado Neón
        "gradiente": ("#1a002a", "#CC44FF")
    },
    {
        "titulo": "Card Three",
        "texto": "Calculadora de Tarifa: Aplica recargos y descuentos complejos.",
        "color_neon": "#44FF88",      # Verde Neón
        "gradiente": ("#002a10", "#44FF88")
    }
]

# ==========================================
# CLASE PRINCIPAL DE LA APLICACIÓN
# ==========================================
class SistemaNeonPro:
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEMA NEÓN PRO v1.0 🐶")
        self.root.geometry("1100x700")
        self.root.configure(bg=COLOR_FONDO_APP)
        
        # Variables de estado
        self.intentos_login = 0
        
        # Iniciar con la pantalla de Login
        self.pantalla_login()

    def limpiar_pantalla(self):
        """Elimina todos los widgets de la ventana actual."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================================
    # PANTALLA 1: LOGIN (CON TU LÓGICA DE SEGURIDAD)
    # ==========================================
    def pantalla_login(self):
        self.limpiar_pantalla()
        
        # Contenedor centrado para el login
        frame_login = tk.Frame(self.root, bg="#111111", highlightbackground="#00FFFF", highlightthickness=2, bd=0)
        frame_login.place(relx=0.5, rely=0.5, anchor="center", width=350, height=450)
        
        # Título
        tk.Label(frame_login, text="🔒", font=("Arial", 60), bg="#111111", fg="#00FFFF").pack(pady=(30, 10))
        tk.Label(frame_login, text="ACCESO", font=("Impact", 30), bg="#111111", fg="white").pack(pady=10)
        
        # Entradas de texto
        tk.Label(frame_login, text="Usuario:", font=("Arial", 12), bg="#111111", fg="#aaaaaa").pack(anchor="w", padx=40)
        self.entry_user = tk.Entry(frame_login, font=("Arial", 12), bg="#222222", fg="white", insertbackground="white", bd=0)
        self.entry_user.pack(pady=5, padx=40, fill="x")
        
        tk.Label(frame_login, text="Contraseña:", font=("Arial", 12), bg="#111111", fg="#aaaaaa").pack(anchor="w", padx=40, pady=(10, 0))
        self.entry_pass = tk.Entry(frame_login, font=("Arial", 12), bg="#222222", fg="white", insertbackground="white", bd=0, show="*")
        self.entry_pass.pack(pady=5, padx=40, fill="x")
        
        # Botón de Login
        btn_login = tk.Button(frame_login, text="ENTRAR", font=("Arial", 14, "bold"), 
                             bg="#00FFFF", fg="black", activebackground="#00CCCC", 
                             bd=0, cursor="hand2", command=self.ejecutar_login)
        btn_login.pack(pady=40, padx=40, fill="x")

    def ejecutar_login(self):
        """Toda tu lógica original de validación de usuario."""
        usuario = self.entry_user.get().strip()
        clave = self.entry_pass.get().strip()

        # --- VALIDACIONES DE FORMATO (ORIGINALES) ---
        if not usuario:
            messagebox.showerror("Error", "Usuario vacío.")
            return
        elif " " in usuario:
            messagebox.showerror("Error", "El usuario no puede tener espacios.")
            return
        elif len(clave) < 8:
            messagebox.showerror("Error", "La contraseña es muy corta (mínimo 8).")
            return
        elif not any(c.isalpha() for c in clave):
            messagebox.showerror("Error", "La contraseña debe contener al menos una letra.")
            return
        elif not any(c.isdigit() for c in clave):
            messagebox.showerror("Error", "La contraseña debe contener al menos un número.")
            return

        # --- VALIDACIÓN DE CREDENCIALES ---
        if usuario == "admin" and clave == "admin2026":
            messagebox.showinfo("Éxito", "¡Acceso concedido!")
            self.pantalla_dashboard()
        else:
            self.intentos_login += 1
            if self.intentos_login >= 3:
                messagebox.showerror("BLOQUEADO", "SISTEMA BLOQUEADO")
                self.root.destroy()
            else:
                messagebox.showwarning("Error", f"Datos incorrectos. Intentos restantes: {3 - self.intentos_login}")

    # ==========================================
    # PANTALLA 2: DASHBOARD (CARDS CON CANVAS)
    # ==========================================
    def pantalla_dashboard(self):
        self.limpiar_pantalla()
        
        # --- HEADER ---
        header = tk.Frame(self.root, bg="#111111", height=80)
        header.pack(fill="x", side="top")
        
        btn_salir = tk.Button(header, text="🚪 SALIR", font=("Arial", 12, "bold"), 
                              bg="#FF4444", fg="white", activebackground="#CC3333", 
                              bd=0, cursor="hand2", command=self.pantalla_login)
        btn_salir.pack(side="left", padx=20, pady=20)
        
        tk.Label(header, text="DASHBOARD NEÓN PRO", font=("Impact", 28), bg="#111111", fg="white").pack(side="right", padx=30)

        # --- CONTENEDOR DE CARDS (Usamos un Canvas para permitir Scroll futuro si añades las 13) ---
        container = tk.Frame(self.root, bg=COLOR_FONDO_APP)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Diccionario para mapear ejecuciones
        acciones = [self.ej_clasificar, self.ej_edad, self.ej_tarifa]

        # Crear las 3 Cards principales
        for i, config in enumerate(CARDS_CONFIG):
            self.crear_neon_card(container, config, acciones[i], i)

    def crear_neon_card(self, master, config, comando, columna):
        """
        Dibuja una card neón completa en un Canvas: Box Shadow + Gradiente + Contenido.
        Esta es la única forma de hacerlo 'bien perro' solo con tkinter.
        """
        card_w, card_h = 300, 450
        margin = 20 # Espacio para el Box Shadow externo
        
        # 1. Crear el Canvas para esta card
        canvas = tk.Canvas(master, width=card_w + margin*2, height=card_h + margin*2, 
                           bg=COLOR_FONDO_APP, highlightthickness=0)
        canvas.grid(row=0, column=columna, padx=15, pady=15)
        
        x1, y1 = margin, margin
        x2, y2 = x1 + card_w, y1 + card_h
        neon_color = config["color_neon"]

        # 2. DIBUJAR 'BOX SHADOW' NEÓN (Múltiples rectángulos con degradado de opacidad simulado)
        # Tkinter no soporta Alpha real en rectángulos, usamos un truco de difuminado
        for i in range(15, 0, -1):
            # Calculamos un color más oscuro a medida que se aleja (difuminado)
            # Esto es complejo en HEX puro, simplificamos usando el color neón con guiones (stipple)
            canvas.create_rectangle(x1 - i, y1 - i, x2 + i, y2 + i, outline=neon_color, width=1)

        # 3. DIBUJAR GRADIENTE DE FONDO (Múltiples líneas horizontales)
        c_top = self.hex_to_rgb(config["gradiente"][0])
        c_bottom = self.hex_to_rgb(config["gradiente"][1])
        
        for y in range(card_h):
            # Interpolación lineal de RGB
            r = int(c_top[0] + (c_bottom[0] - c_top[0]) * y / card_h)
            g = int(c_top[1] + (c_bottom[1] - c_top[1]) * y / card_h)
            b = int(c_top[2] + (c_bottom[2] - c_top[2]) * y / card_h)
            color_linea = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(x1, y1 + y, x2, y1 + y, fill=color_linea)

        # 4. DIBUJAR BORDE SÓLIDO PRINCIPAL
        canvas.create_rectangle(x1, y1, x2, y2, outline=neon_color, width=3)

        # 5. INSERTAR CONTENIDO (Widgets sobre el Canvas usando .place)
        # Título estilo Impact
        tk.Label(canvas, text=config["titulo"], font=("Impact", 28), 
                 bg=config["gradiente"][0], fg="white").place(x=x1 + 20, y=y1 + 30)
        
        # Descripción
        tk.Label(canvas, text=config["texto"], font=("Arial", 12), 
                 bg=config["gradiente"][0], fg="#cccccc", wraplength=card_w - 40, justify="left").place(x=x1 + 20, y=y1 + 100)

        # Botón 'EJECUTAR' (Flat UI style)
        btn_card = tk.Button(canvas, text="EJECUTAR", font=("Arial", 13, "bold"), 
                             bg="white", fg="black", activebackground="#dddddd", 
                             bd=0, cursor="hand2", command=comando)
        btn_card.place(x=x1 + 20, y=y2 - 60, width=120, height=40)

    # ==========================================
    # ADAPTACIÓN DE TUS FUNCIONES LÓGICAS A GUI
    # ==========================================
    def ej_clasificar(self):
        # Usamos ventanas de diálogo sencillas para los inputs, manteniendo la lógica
        from tkinter import simpledialog
        num_str = simpledialog.askstring("Ejercicio 1", "¿Qué número quieres clasificar?")
        if num_str is None: return # Cancelado
        
        try:
            numero = int(num_str)
            # --- Tu lógica original ---
            msg = "Cero" if numero == 0 else ("Positivo" if numero > 0 else "Negativo")
            if numero != 0:
                msg += " y " + ("Par" if numero % 2 == 0 else "Impar")
            messagebox.showinfo("Resultado", f"El número {numero} es: {msg}")
        except ValueError:
            messagebox.showerror("Error", "Debes ingresar un número entero válido.")

    def ej_edad(self):
        from tkinter import simpledialog
        edad_str = simpledialog.askstring("Ejercicio 2", "Ingresa tu edad:")
        if edad_str is None: return
        
        try:
            edad = int(edad_str)
            # --- Tu lógica original ---
            res = "Niñez" if edad < 13 else "Adolescencia" if edad < 18 else "Adultez"
            messagebox.showinfo("Categoría", f"Perteneces a: {res}")
        except ValueError:
            messagebox.showerror("Error", "Edad inválida.")

    def ej_tarifa(self):
        # Para la tarifa compleja, usaremos una ventana emergente personalizada (Toplevel)
        from tkinter import simpledialog
        
        # Usamos logs rápidos para simplificar la GUI de este ejercicio complejo
        try:
            edad = int(simpledialog.askstring("Tarifa", "Edad (0-120):"))
            dia = int(simpledialog.askstring("Tarifa", "Día (1=Lun ... 7=Dom):"))
            
            # Simulamos las preguntas Si/No con messageboxes para no perder la lógica Estudiante/Miembro
            es_estudiante = messagebox.askyesno("Tarifa", "¿Es estudiante?")
            es_miembro = messagebox.askyesno("Tarifa", "¿Es miembro?")
            
            # Método de pago (Efectivo/Tarjeta)
            pago_str = simpledialog.askstring("Tarifa", "Método de pago: E (efectivo) o T (tarjeta):").strip().upper()
            metodo_pago = "E" if pago_str == "E" else "T"

            # --- Toda tu lógica original de cálculo ---
            base = 200
            recargo = base * 0.10 if dia in [6, 7] else 0
            
            descuentos = [
                50 if edad <= 12 else 20 if edad <= 17 else 30 if edad >= 65 else 0,
                15 if es_estudiante and edad >= 13 else 0,
                10 if es_miembro else 0,
                5 if metodo_pago == "E" else 0
            ]
            total_descuento = min(sum(descuentos), 60)
            total_final = base + recargo - (base * total_descuento / 100)

            res_final = f"Precio Base: ${base}\nRecargos: ${recargo}\nDescuento total: {total_desc}% ($60 max.)\nTOTAL FINAL: ${total_final}"
            messagebox.showinfo("Factura", res_final)
            
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Datos de entrada inválidos.")

    # ==========================================
    # UTILIDADES TÉCNICAS
    # ==========================================
    @staticmethod
    def hex_to_rgb(hex_color):
        """Convierte #RRGGBB a una tupla (R, G, B)."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# ==========================================
# INICIO DEL PROGRAMA
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaNeonPro(root)
    root.mainloop()