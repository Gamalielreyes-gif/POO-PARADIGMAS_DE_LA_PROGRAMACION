"""
Inventario: capa de acceso a la tabla `inventario` (SQLite).
Implementa Singleton para que toda la app comparta la misma instancia.
Soporta el patron Observer (notifica bajo stock).
"""
from tienda_app.model.database import get_connection


class Inventario:
    _instancia = None
    UMBRAL_BAJO_STOCK = 5

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._observers = []
        return cls._instancia

    # =========================
    # Observer
    # =========================
    def agregar_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def quitar_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def _notificar_bajo_stock(self, id_producto, nombre, stock):
        for obs in self._observers:
            obs.notificar_bajo_stock(id_producto, nombre, stock)

    # =========================
    # CRUD
    # =========================
    def agregar_productos(self, tupla_productos: list):
        conn = get_connection()
        cur = conn.cursor()
        cur.executemany(
            "INSERT OR REPLACE INTO inventario VALUES (?,?,?,?,?,?,?)",
            tupla_productos,
        )
        conn.commit()
        conn.close()

    def eliminar_productos_id(self, ids: list[int]):
        conn = get_connection()
        cur = conn.cursor()
        for _id in ids:
            if not isinstance(_id, int):
                raise TypeError("Id del producto invalido")
            cur.execute("DELETE FROM inventario WHERE id_producto = ?", (_id,))
        conn.commit()
        conn.close()

    def eliminar_productos_nombre(self, nombres: list[str]):
        conn = get_connection()
        cur = conn.cursor()
        for n in nombres:
            if not isinstance(n, str):
                raise TypeError("El nombre debe ser texto")
            cur.execute(
                "DELETE FROM inventario WHERE LOWER(nombre)=LOWER(?)", (n,)
            )
        conn.commit()
        conn.close()

    def actualizar_columnas_textos(self, id_producto: int, columna: str,
                                   dato: str):
        if columna not in ("nombre", "categoria"):
            raise ValueError("Columna invalida")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            f"UPDATE inventario SET {columna} = ? WHERE id_producto = ?",
            (dato, id_producto),
        )
        conn.commit()
        conn.close()

    def actualizar_precio_venta(self, id_producto: int, precio: float):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE inventario SET precio_venta = ? WHERE id_producto = ?",
            (precio, id_producto),
        )
        conn.commit()
        conn.close()

    def rellenar_stock(self, ids: list[int]):
        conn = get_connection()
        cur = conn.cursor()
        for _id in ids:
            cur.execute(
                "UPDATE inventario SET stock = 20 WHERE id_producto = ?",
                (_id,),
            )
        conn.commit()
        conn.close()

    def aumentar_stock(self, ids: list[int], cantidades: list[float]):
        if len(ids) != len(cantidades):
            raise ValueError("Listas de diferente tamano")

        conn = get_connection()
        cur = conn.cursor()
        for _id, cant in zip(ids, cantidades):
            id_str = str(_id)
            if id_str.startswith("10"):
                cant = int(cant)
            elif id_str.startswith("20"):
                cant = float(cant)
            cur.execute(
                "UPDATE inventario SET stock = stock + ? WHERE id_producto=?",
                (cant, _id),
            )
        conn.commit()

        # check bajo stock y notificar
        for _id in ids:
            cur.execute(
                "SELECT id_producto, nombre, stock FROM inventario "
                "WHERE id_producto = ?",
                (_id,),
            )
            row = cur.fetchone()
            if row and row[2] < self.UMBRAL_BAJO_STOCK:
                self._notificar_bajo_stock(row[0], row[1], row[2])
        conn.close()

    # =========================
    # Consultas
    # =========================
    def mostrar_todo(self) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventario ORDER BY id_producto")
        rows = cur.fetchall()
        conn.close()
        return [self._row_to_dict(r) for r in rows]

    def buscar_producto_id(self, id_producto: int) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM inventario WHERE id_producto = ?", (id_producto,)
        )
        rows = cur.fetchall()
        conn.close()
        return [self._row_to_dict(r) for r in rows]

    def buscar_productos_nombre(self, nombre: str) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM inventario WHERE nombre LIKE ?", (f"%{nombre}%",)
        )
        rows = cur.fetchall()
        conn.close()
        return [self._row_to_dict(r) for r in rows]

    def buscar_producto_categoria(self, categoria: str) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM inventario WHERE categoria LIKE ?",
            (f"%{categoria}%",),
        )
        rows = cur.fetchall()
        conn.close()
        return [self._row_to_dict(r) for r in rows]

    def buscar_por_codigo_barras(self, codigo: int) -> dict | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM inventario WHERE codigo_barras = ?", (codigo,)
        )
        row = cur.fetchone()
        conn.close()
        return self._row_to_dict(row) if row else None

    @staticmethod
    def _row_to_dict(row):
        return {
            "id_producto":   row[0],
            "nombre":        row[1],
            "categoria":     row[2],
            "codigo_barras": row[3],
            "precio_compra": row[4],
            "precio_venta":  row[5],
            "stock":         row[6],
        }
