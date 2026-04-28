from tienda_app.model.detalles_venta import DetalleVenta
from tienda_app.model.venta import Venta
from tienda_app.utils.sin_stock_exception import SinStockException


class VentaController:
    """Controlador de ventas."""

    def __init__(self, inventario, cliente_controller=None):
        self.inventario = inventario
        self.cliente_controller = cliente_controller

    def crear_detalle(self, productos: list, cantidades: list) -> DetalleVenta:
        detalle = DetalleVenta()
        detalle.agregar_productos(productos, cantidades)
        return detalle

    def crear_venta(self, detalle, cliente=None, estrategias=None) -> Venta:
        return Venta(detalle, self.inventario, cliente, estrategias or [])

    def _validar_stock(self, productos, cantidades):
        for p, c in zip(productos, cantidades):
            consulta = self.inventario.buscar_producto_id(p.id_producto)
            if not consulta:
                raise SinStockException(p.id_producto, p.nombre, 0, c)
            disponible = consulta[0]["stock"]
            if disponible < c:
                raise SinStockException(p.id_producto, p.nombre,
                                        disponible, c)

    def procesar_venta(self, productos, cantidades, cliente=None,
                       estrategias=None) -> dict:
        """Flujo completo: valida stock, calcula, finaliza y devuelve ticket."""
        self._validar_stock(productos, cantidades)

        detalle = self.crear_detalle(productos, cantidades)
        venta = self.crear_venta(detalle, cliente, estrategias)

        # Calcular totales antes de tocar stock
        subtotal = round(venta.calcular_subtotal(), 2)
        iva = round(venta.calcular_iva(), 2)
        descuento = round(venta.calcular_descuento_total(), 2)
        total = round(venta.calcular_total(), 2)

        # Descontar stock + acumular puntos
        venta.finalizar_venta()

        # Ticket (ya con puntos actualizados del cliente)
        ticket = venta.generar_ticket()

        return {
            "ticket":    ticket,
            "subtotal":  subtotal,
            "iva":       iva,
            "descuento": descuento,
            "total":     total,
            "fecha":     venta.fecha.isoformat(),
            "cliente":   cliente.nombre if cliente else None,
            "puntos":    cliente.puntos if cliente else None,
        }
