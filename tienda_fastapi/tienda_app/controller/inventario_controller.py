class InventarioController:
    """Controlador de inventario."""

    def __init__(self, inventario, fabrica_producto):
        self.inventario = inventario
        self.fabrica = fabrica_producto

    # ============ CREAR ============
    def crear_producto_unitario(self, id_producto, nombre, categoria,
                                codigo_barras, precio_compra,
                                precio_venta, stock):
        producto = self.fabrica.crear_producto_unitario(
            id_producto, nombre, categoria, codigo_barras,
            precio_compra, precio_venta, stock,
        )
        self.inventario.agregar_productos([(
            producto.id_producto, producto.nombre, producto.categoria,
            producto.codigo_barras, producto.precio_compra,
            producto.precio_venta, int(stock),
        )])
        return producto

    def crear_producto_granel(self, id_producto, nombre, categoria,
                              codigo_barras, precio_compra,
                              precio_venta, stock):
        producto = self.fabrica.crear_producto_granel(
            id_producto, nombre, categoria, codigo_barras,
            precio_compra, precio_venta, stock,
        )
        self.inventario.agregar_productos([(
            producto.id_producto, producto.nombre, producto.categoria,
            producto.codigo_barras, producto.precio_compra,
            producto.precio_venta, float(stock),
        )])
        return producto

    # ============ ELIMINAR ============
    def eliminar_por_id(self, ids: list[int]):
        self.inventario.eliminar_productos_id(ids)

    def eliminar_por_nombre(self, nombres: list[str]):
        self.inventario.eliminar_productos_nombre(nombres)

    # ============ ACTUALIZAR ============
    def actualizar_nombre(self, id_producto: int, nuevo: str):
        self.inventario.actualizar_columnas_textos(id_producto, "nombre", nuevo)

    def actualizar_categoria(self, id_producto: int, nueva: str):
        self.inventario.actualizar_columnas_textos(
            id_producto, "categoria", nueva,
        )

    def actualizar_precio(self, id_producto: int, nuevo: float):
        self.inventario.actualizar_precio_venta(id_producto, nuevo)

    # ============ STOCK ============
    def aumentar_stock(self, ids, cantidades):
        self.inventario.aumentar_stock(ids, cantidades)

    def disminuir_stock(self, ids, cantidades):
        self.inventario.aumentar_stock(ids, [-c for c in cantidades])

    def rellenar_stock(self, ids):
        self.inventario.rellenar_stock(ids)

    # ============ CONSULTAS ============
    def obtener_todo(self):
        return self.inventario.mostrar_todo()

    def buscar_por_id(self, id_producto: int):
        return self.inventario.buscar_producto_id(id_producto)

    def buscar_por_nombre(self, nombre: str):
        return self.inventario.buscar_productos_nombre(nombre)

    def buscar_por_categoria(self, categoria: str):
        return self.inventario.buscar_producto_categoria(categoria)

    def buscar_por_codigo_barras(self, codigo: int):
        return self.inventario.buscar_por_codigo_barras(codigo)
