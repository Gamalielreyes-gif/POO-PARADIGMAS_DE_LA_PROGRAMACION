from tienda_app.model.producto import Producto


class ProductoUnitario(Producto):
    """Producto unitario. ID compuesto: prefijo 10."""

    def __init__(self, id_producto: int, nombre: str, categoria: str,
                 codigo_barras: int, precio_compra: float,
                 precio_venta: float, stock: int) -> None:
        # Si el id NO inicia con 10, lo prefijamos
        id_str = str(id_producto)
        if not id_str.startswith("10"):
            id_producto = int(f"10{id_producto}")
        super().__init__(id_producto, nombre, categoria, codigo_barras,
                         precio_compra, precio_venta, int(stock))

    def __str__(self):
        return (f"===== {self.nombre} =====\n"
                f"Categoria: {self.categoria}\n"
                f"Precio: ${self.precio_venta}\n"
                f"Codigo: {self._codigo_barras}\n")
