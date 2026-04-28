class DetalleVenta:
    """Detalle de productos de una venta."""

    IVA_PORCENTAJE = 0.16

    def __init__(self):
        self.productos = []
        self.cantidades = []

    def agregar_productos(self, productos: list, cantidades: list):
        if len(productos) != len(cantidades):
            raise ValueError("Listas de diferente tamano")
        self.productos = productos
        self.cantidades = cantidades

    def calcular_subtotal(self) -> float:
        total = 0.0
        for prod, cant in zip(self.productos, self.cantidades):
            total += prod.precio_venta * cant
        return total

    def calcular_iva(self) -> float:
        return self.calcular_subtotal() * self.IVA_PORCENTAJE

    def calcular_total(self) -> float:
        return self.calcular_subtotal() + self.calcular_iva()

    def __str__(self):
        info = "Detalles de venta:\n"
        for prod, cant in zip(self.productos, self.cantidades):
            info += (f"- {prod.nombre} | Cantidad: {cant} "
                     f"| Precio: {prod.precio_venta}\n")
        info += f"\nSubtotal: {self.calcular_subtotal():.2f}"
        info += f"\nIVA: {self.calcular_iva():.2f}"
        info += f"\nTotal: {self.calcular_total():.2f}"
        return info
