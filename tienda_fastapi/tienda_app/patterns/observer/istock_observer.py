from abc import ABC, abstractmethod


class IStockObserver(ABC):
    """Interfaz Observer para alertas de stock."""

    @abstractmethod
    def notificar_bajo_stock(self, id_producto, nombre, stock):
        pass
