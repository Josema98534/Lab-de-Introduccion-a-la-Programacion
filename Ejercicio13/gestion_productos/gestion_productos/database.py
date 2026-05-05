import sqlite3

def init_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_proveedor TEXT NOT NULL,
            nombre_producto TEXT NOT NULL,
            codigo TEXT NOT NULL,
            num_producto INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()