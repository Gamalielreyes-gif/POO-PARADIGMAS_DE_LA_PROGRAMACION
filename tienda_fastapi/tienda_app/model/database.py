"""
Conexión a SQLite. En Vercel solo /tmp es escribible por lo que la BD se
crea ahí y se reinicia entre cold starts. En local funciona igual.
"""
import sqlite3
import os

# /tmp es la única ruta escribible en Vercel (serverless)
DB_PATH = os.environ.get("TIENDA_DB_PATH", "/tmp/tienda.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    # ====== Inventario ======
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
            id_producto    INTEGER PRIMARY KEY,
            nombre         TEXT NOT NULL,
            categoria      TEXT,
            codigo_barras  INTEGER UNIQUE,
            precio_compra  REAL,
            precio_venta   REAL,
            stock          REAL NOT NULL
        )
    """)

    # ====== Cliente ======
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre     TEXT NOT NULL,
            telefono   TEXT,
            puntos     INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def seed_demo():
    """Carga datos demo si la tabla está vacía."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM inventario")
    if cur.fetchone()[0] == 0:
        productos_demo = [
            # (id, nombre, categoria, codigo_barras, p_compra, p_venta, stock)
            (101, "Leche Entera 1L",  "Lacteos",   7501001110, 18.0, 26.0, 30),
            (102, "Refresco Cola",    "Bebidas",   7501001111, 12.0, 22.0, 50),
            (103, "Galletas Maria",   "Abarrotes", 7501001112,  8.5, 15.0, 40),
            (104, "Detergente 1kg",   "Limpieza",  7501001113, 32.0, 49.0, 20),
            (201, "Arroz Granel",     "Granos",    7501002201,  9.0, 18.0, 12.5),
            (202, "Frijol Negro",     "Granos",    7501002202, 15.0, 28.0,  8.0),
            (203, "Azucar Estandar",  "Abarrotes", 7501002203, 11.0, 19.0,  5.5),
        ]
        cur.executemany(
            "INSERT INTO inventario VALUES (?,?,?,?,?,?,?)",
            productos_demo,
        )

    cur.execute("SELECT COUNT(*) FROM cliente")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO cliente (nombre, telefono, puntos) VALUES (?,?,?)",
            [
                ("Juan Perez",   "5551234567", 0),
                ("Maria Lopez",  "5559876543", 0),
            ],
        )

    conn.commit()
    conn.close()


def init_db():
    crear_tablas()
    seed_demo()


if __name__ == "__main__":
    init_db()
    print(f"DB inicializada en {DB_PATH}")
