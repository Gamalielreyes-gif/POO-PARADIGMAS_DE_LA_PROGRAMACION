from abc import ABC


class Producto(ABC):
    """Producto base de la tienda."""

    def __init__(self, id_producto: int, nombre: str, categoria: str,
                 codigo_barras: int, precio_compra: float,
                 precio_venta: float, stock: float) -> None:
        self._id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self._codigo_barras = codigo_barras
        self._precio_compra = precio_compra
        self.precio_venta = precio_venta
        self._stock = stock

    @property
    def id_producto(self):
        return self._id_producto

    @property
    def codigo_barras(self):
        return self._codigo_barras

    @property
    def precio_compra(self):
        return self._precio_compra
