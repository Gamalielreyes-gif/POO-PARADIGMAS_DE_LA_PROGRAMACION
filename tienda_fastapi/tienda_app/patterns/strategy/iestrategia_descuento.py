from abc import ABC, abstractmethod


class IEstrategiaDescuento(ABC):
    """Interfaz Strategy para descuentos."""

    @abstractmethod
    def aplicar_descuento(self, detalle_venta) -> float:
        """Retorna el monto a descontar."""
        pass
