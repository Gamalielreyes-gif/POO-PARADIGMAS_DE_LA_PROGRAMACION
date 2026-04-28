from tienda_app.model.producto import Producto


class ProductoGranel(Producto):
    """Producto granel (se pesa). ID compuesto: prefijo 20."""

    def __init__(self, id_producto: int, nombre: str, categoria: str,
                 codigo_barras: int, precio_compra: float,
                 precio_venta: float, stock: float) -> None:
        id_str = str(id_producto)
        if not id_str.startswith("20"):
            id_producto = int(f"20{id_producto}")
        super().__init__(id_producto, nombre, categoria, codigo_barras,
                         precio_compra, precio_venta, float(stock))

    def __str__(self):
        return (f"===== {self.nombre} =====\n"
                f"Categoria: {self.categoria}\n"
                f"Precio: ${self.precio_venta}\n"
                f"Codigo: {self._codigo_barras}\n")
