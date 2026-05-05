from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'uaz_software_key'

def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    # Usamos SUM y GROUP BY para consolidar el inventario por código
    productos = conn.execute('''
        SELECT id, id_proveedor, nombre_producto, codigo, SUM(num_producto) as num_producto 
        FROM productos 
        GROUP BY codigo 
        ORDER BY id DESC
    ''').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/guardar', methods=['POST'])
def guardar():
    id_prov = request.form['id_proveedor']
    nombre = request.form['nombre_producto']
    codigo = request.form['codigo']
    cantidad_nueva = int(request.form['num_producto'])

    conn = get_db_connection()
    producto_existente = conn.execute('SELECT * FROM productos WHERE codigo = ?', (codigo,)).fetchone()

    if producto_existente:
        # Validación de integridad
        if producto_existente['id_proveedor'] != id_prov or producto_existente['nombre_producto'].lower() != nombre.lower():
            conn.close()
            return f"""
                <div style="background:#1e293b; color:white; padding:20px; font-family:sans-serif; border-radius:15px; text-align:center;">
                    <h1 style="color:#ef4444;">⚠️ ERROR DE VALIDACIÓN</h1>
                    <p>El código <b>{codigo}</b> ya pertenece a otro producto o proveedor.</p>
                    <a href="/" style="color:#00d2ff; text-decoration:none;">[ Volver ]</a>
                </div>
            """, 400
        
        total = producto_existente['num_producto'] + cantidad_nueva
        conn.execute('UPDATE productos SET num_producto = ? WHERE codigo = ?', (total, codigo))
    else:
        conn.execute('INSERT INTO productos (id_proveedor, nombre_producto, codigo, num_producto) VALUES (?, ?, ?, ?)',
                     (id_prov, nombre, codigo, cantidad_nueva))
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    # CORRECCIÓN: Capturamos los 4 campos del formulario
    id_prov = request.form['nuevo_id_prov']
    nombre = request.form['nuevo_nombre']
    codigo = request.form['nuevo_codigo']
    cantidad = int(request.form['nueva_cantidad'])
    
    conn = get_db_connection()
    # Actualizamos todo usando el ID único como ancla
    conn.execute('''
        UPDATE productos 
        SET id_proveedor = ?, nombre_producto = ?, codigo = ?, num_producto = ? 
        WHERE id = ?
    ''', (id_prov, nombre, codigo, cantidad, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)