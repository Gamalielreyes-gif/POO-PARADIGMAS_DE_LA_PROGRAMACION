from datetime import datetime


class Venta:
    """Venta de la tienda. Integra detalle, cliente y estrategias de descuento."""

    def __init__(self, detalle_venta, inventario, cliente=None,
                 estrategia_descuento=None):
        self.detalle = detalle_venta
        self.inventario = inventario
        self.cliente = cliente
        self.estrategia_descuento = estrategia_descuento or []
        self.fecha = datetime.now()

    def calcular_subtotal(self) -> float:
        return self.detalle.calcular_subtotal()

    def calcular_iva(self) -> float:
        return self.detalle.calcular_iva()

    def calcular_descuento_total(self) -> float:
        total = 0.0
        for est in self.estrategia_descuento:
            total += est.aplicar_descuento(self.detalle)
        return total

    def calcular_total(self) -> float:
        total = (self.calcular_subtotal()
                 + self.calcular_iva()
                 - self.calcular_descuento_total())
        return max(total, 0)

    def sumar_puntos(self):
        if self.cliente:
            puntos = int(self.calcular_total() // 10)
            self.cliente.acumular_puntos(puntos)

    def descontar_stock(self):
        ids = [p.id_producto for p in self.detalle.productos]
        cantidades = list(self.detalle.cantidades)
        self.inventario.aumentar_stock(ids, [-c for c in cantidades])

    def finalizar_venta(self):
        self.descontar_stock()
        self.sumar_puntos()

    def generar_ticket(self) -> str:
        t = "===== TICKET DE COMPRA =====\n"
        t += f"Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}\n"
        if self.cliente:
            t += f"Cliente: {self.cliente.nombre}\n"
        t += "--- Productos ---\n"
        for prod, cant in zip(self.detalle.productos, self.detalle.cantidades):
            t += f"{prod.nombre} x{cant} - ${prod.precio_venta * cant:.2f}\n"

        t += "---------------------------\n"
        t += f"Subtotal: ${self.calcular_subtotal():.2f}\n"
        t += f"IVA:      ${self.calcular_iva():.2f}\n"
        t += f"Descuento: -${self.calcular_descuento_total():.2f}\n"
        t += f"TOTAL:    ${self.calcular_total():.2f}\n"
        if self.cliente:
            t += f"Puntos acumulados: {self.cliente.puntos}\n"
        t += "===========================\n"
        return t
