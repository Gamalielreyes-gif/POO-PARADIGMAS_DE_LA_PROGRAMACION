class SinStockException(Exception):
    """Se lanza cuando un producto no tiene suficiente stock."""

    def __init__(self, id_producto, nombre, disponible, solicitado):
        self.id_producto = id_producto
        self.nombre = nombre
        self.disponible = disponible
        self.solicitado = solicitado
        super().__init__(
            f"Sin stock suficiente para '{nombre}' (id={id_producto}): "
            f"disponible={disponible}, solicitado={solicitado}"
        )
