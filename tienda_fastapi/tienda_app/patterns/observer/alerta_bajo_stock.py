from tienda_app.patterns.observer.istock_observer import IStockObserver


class AlertaBajoStock(IStockObserver):
    """Observer que registra alertas cuando un producto tiene bajo stock."""

    def __init__(self):
        self.alertas: list[dict] = []

    def notificar_bajo_stock(self, id_producto, nombre, stock):
        alerta = {
            "id_producto": id_producto,
            "nombre": nombre,
            "stock": stock,
            "mensaje": f"Bajo stock: {nombre} (id={id_producto}), stock={stock}",
        }
        self.alertas.append(alerta)

    def obtener_alertas(self):
        return list(self.alertas)

    def limpiar(self):
        self.alertas.clear()
