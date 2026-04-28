from tienda_app.model.producto_unitario import ProductoUnitario
from tienda_app.model.producto_granel import ProductoGranel


class ProductoFactory:
    """Factory para crear productos unitarios o granel."""

    def crear_producto_unitario(self, id_producto, nombre, categoria,
                                codigo_barras, precio_compra,
                                precio_venta, stock):
        return ProductoUnitario(id_producto, nombre, categoria,
                                codigo_barras, precio_compra,
                                precio_venta, stock)

    def crear_producto_granel(self, id_producto, nombre, categoria,
                              codigo_barras, precio_compra,
                              precio_venta, stock):
        return ProductoGranel(id_producto, nombre, categoria,
                              codigo_barras, precio_compra,
                              precio_venta, stock)
