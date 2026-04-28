from tienda_app.patterns.strategy.iestrategia_descuento import (
    IEstrategiaDescuento,
)


class DescuentoFijo(IEstrategiaDescuento):
    def __init__(self, monto: float):
        self.monto = monto

    def aplicar_descuento(self, detalle_venta) -> float:
        return float(self.monto)
