from tienda_app.patterns.strategy.iestrategia_descuento import (
    IEstrategiaDescuento,
)


class DescuentoPorcentaje(IEstrategiaDescuento):
    def __init__(self, porcentaje: float):
        self.porcentaje = porcentaje

    def aplicar_descuento(self, detalle_venta) -> float:
        subtotal = detalle_venta.calcular_subtotal()
        return subtotal * (self.porcentaje / 100.0)
