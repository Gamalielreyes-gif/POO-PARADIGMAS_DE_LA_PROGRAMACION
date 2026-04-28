class Cliente:
    """Cliente frecuente con puntos acumulables."""

    def __init__(self, id_cliente: int, nombre: str, telefono: str,
                 puntos: int = 0):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__telefono = telefono
        self.__puntos = puntos

    @property
    def id_cliente(self):
        return self.__id_cliente

    @property
    def nombre(self):
        return self.__nombre

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo: str):
        if not isinstance(nuevo, str):
            raise TypeError("El telefono debe ser texto")
        self.__telefono = nuevo

    @property
    def puntos(self):
        return self.__puntos

    def acumular_puntos(self, puntos: int):
        if puntos < 0:
            raise ValueError("No se pueden acumular puntos negativos")
        self.__puntos += puntos

    def redimir_puntos(self, puntos: int) -> bool:
        if puntos <= self.__puntos:
            self.__puntos -= puntos
            return True
        return False

    def __str__(self):
        return (f"{self.__nombre} - Tel: {self.__telefono} "
                f"- Puntos: {self.__puntos}")
