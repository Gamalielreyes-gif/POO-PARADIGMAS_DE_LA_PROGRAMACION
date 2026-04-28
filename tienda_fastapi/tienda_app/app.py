"""
FastAPI app principal del Sistema de Tienda.

Sirve:
- Vistas HTML (templates Jinja2) en /, /inventario_view, /agregar_view, /venta_view
- API JSON en /inventario, /inventario/agregar, /venta, etc.
- Archivos estaticos en /static/...

Para que funcione tanto en Vercel (URLs limpias `/`), se monta el mismo
router con y sin prefijo `/api`.
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Literal

# Modelo / patrones
from tienda_app.model.inventario import Inventario
from tienda_app.model.cliente import Cliente
from tienda_app.model.database import init_db
from tienda_app.controller.inventario_controller import InventarioController
from tienda_app.controller.ventas_controller import VentaController
from tienda_app.patterns.factory.producto_factory import ProductoFactory
from tienda_app.patterns.strategy.descuento_porcentaje import (
    DescuentoPorcentaje,
)
from tienda_app.patterns.strategy.descuento_fijo import DescuentoFijo
from tienda_app.patterns.observer.alerta_bajo_stock import AlertaBajoStock
from tienda_app.utils.sin_stock_exception import SinStockException

# =========================
# Inicializacion de la BD y la capa de dominio
# =========================
init_db()

inventario = Inventario()
fabrica = ProductoFactory()
alerta_observer = AlertaBajoStock()
inventario.agregar_observer(alerta_observer)

inventario_controller = InventarioController(inventario, fabrica)
venta_controller = VentaController(inventario)

# =========================
# Templates / static
# =========================
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "view" / "templates"))

# =========================
# Schemas Pydantic
# =========================
class ProductoIn(BaseModel):
    tipo: Literal["unitario", "granel"]
    id: int
    nombre: str
    categoria: str
    codigo_barras: int
    precio_compra: float
    precio_venta: float
    stock: float


class ClienteIn(BaseModel):
    id: int
    nombre: str
    telefono: str = ""


class DescuentoIn(BaseModel):
    tipo: Literal["porcentaje", "fijo"]
    valor: float


class VentaItem(BaseModel):
    id_producto: int = Field(..., description="ID interno (10... o 20...)")
    cantidad: float


class VentaIn(BaseModel):
    items: List[VentaItem]
    cliente: Optional[ClienteIn] = None
    descuentos: List[DescuentoIn] = []


class ActualizarPrecioIn(BaseModel):
    precio: float


class ActualizarTextoIn(BaseModel):
    valor: str


class StockIn(BaseModel):
    cantidad: float


# =========================
# Helper: convertir filas de inventario a "objeto producto" minimo
# para usar en VentaController (necesita .id_producto, .nombre, .precio_venta)
# =========================
class _ProductoLite:
    def __init__(self, row):
        self.id_producto = row["id_producto"]
        self.nombre = row["nombre"]
        self.precio_venta = row["precio_venta"]


# =========================
# Router (se monta dos veces: en / y en /api)
# =========================
router = APIRouter()


# ---------- Vistas HTML ----------
@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/inventario_view", response_class=HTMLResponse)
def inventario_view(request: Request):
    return templates.TemplateResponse("inventario.html", {"request": request})


@router.get("/agregar_view", response_class=HTMLResponse)
def agregar_view(request: Request):
    return templates.TemplateResponse("agregar.html", {"request": request})


@router.get("/venta_view", response_class=HTMLResponse)
def venta_view(request: Request):
    return templates.TemplateResponse("venta.html", {"request": request})


# ---------- API: Inventario ----------
@router.get("/inventario")
def listar_inventario():
    return {"productos": inventario_controller.obtener_todo()}


@router.post("/inventario/agregar")
def agregar_producto(p: ProductoIn):
    if p.tipo == "unitario":
        producto = inventario_controller.crear_producto_unitario(
            p.id, p.nombre, p.categoria, p.codigo_barras,
            p.precio_compra, p.precio_venta, int(p.stock),
        )
    else:
        producto = inventario_controller.crear_producto_granel(
            p.id, p.nombre, p.categoria, p.codigo_barras,
            p.precio_compra, p.precio_venta, float(p.stock),
        )
    return {
        "mensaje": "Producto agregado",
        "id_producto": producto.id_producto,
        "nombre": producto.nombre,
    }


@router.get("/inventario/buscar/{id_producto}")
def buscar_producto(id_producto: int):
    res = inventario_controller.buscar_por_id(id_producto)
    if not res:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return res[0]


@router.get("/inventario/buscar_nombre/{nombre}")
def buscar_por_nombre(nombre: str):
    return {"productos": inventario_controller.buscar_por_nombre(nombre)}


@router.get("/inventario/buscar_categoria/{categoria}")
def buscar_por_categoria(categoria: str):
    return {"productos": inventario_controller.buscar_por_categoria(categoria)}


@router.get("/inventario/buscar_codigo/{codigo}")
def buscar_por_codigo(codigo: int):
    res = inventario_controller.buscar_por_codigo_barras(codigo)
    if not res:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return res


@router.delete("/inventario/{id_producto}")
def eliminar_producto(id_producto: int):
    inventario_controller.eliminar_por_id([id_producto])
    return {"mensaje": "Producto eliminado", "id_producto": id_producto}


@router.put("/inventario/{id_producto}/precio")
def actualizar_precio(id_producto: int, body: ActualizarPrecioIn):
    inventario_controller.actualizar_precio(id_producto, body.precio)
    return {"mensaje": "Precio actualizado", "precio": body.precio}


@router.put("/inventario/{id_producto}/nombre")
def actualizar_nombre(id_producto: int, body: ActualizarTextoIn):
    inventario_controller.actualizar_nombre(id_producto, body.valor)
    return {"mensaje": "Nombre actualizado", "nombre": body.valor}


@router.put("/inventario/{id_producto}/categoria")
def actualizar_categoria(id_producto: int, body: ActualizarTextoIn):
    inventario_controller.actualizar_categoria(id_producto, body.valor)
    return {"mensaje": "Categoria actualizada", "categoria": body.valor}


@router.put("/inventario/{id_producto}/stock")
def aumentar_stock(id_producto: int, body: StockIn):
    inventario_controller.aumentar_stock([id_producto], [body.cantidad])
    return {"mensaje": "Stock actualizado", "delta": body.cantidad}


# ---------- API: Venta ----------
@router.post("/venta")
def realizar_venta(v: VentaIn):
    # Construir objetos producto a partir del inventario actual
    productos = []
    cantidades = []
    for item in v.items:
        consulta = inventario_controller.buscar_por_id(item.id_producto)
        if not consulta:
            raise HTTPException(
                status_code=404,
                detail=f"Producto id={item.id_producto} no existe",
            )
        productos.append(_ProductoLite(consulta[0]))
        cantidades.append(item.cantidad)

    cliente = None
    if v.cliente:
        cliente = Cliente(v.cliente.id, v.cliente.nombre, v.cliente.telefono)

    estrategias = []
    for d in v.descuentos:
        if d.tipo == "porcentaje":
            estrategias.append(DescuentoPorcentaje(d.valor))
        else:
            estrategias.append(DescuentoFijo(d.valor))

    try:
        resumen = venta_controller.procesar_venta(
            productos, cantidades, cliente, estrategias,
        )
    except SinStockException as e:
        raise HTTPException(status_code=409, detail=str(e))

    return resumen


# ---------- API: Alertas ----------
@router.get("/alertas")
def alertas_bajo_stock():
    return {"alertas": alerta_observer.obtener_alertas()}


@router.delete("/alertas")
def limpiar_alertas():
    alerta_observer.limpiar()
    return {"mensaje": "Alertas limpiadas"}


# ---------- Health ----------
@router.get("/health")
def health():
    return {"status": "ok", "app": "tienda-abarrotes"}


# =========================
# App FastAPI
# =========================
app = FastAPI(title="Sistema de Tienda - POO Paradigmas",
              description="POO + MVC + Patrones (Factory/Strategy/Observer)",
              version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Static files (CSS/JS) montados en /static y /api/static
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "view" / "static")),
    name="static",
)
app.mount(
    "/api/static",
    StaticFiles(directory=str(BASE_DIR / "view" / "static")),
    name="static_api",
)

# Rutas en raiz (Vercel/local) y bajo /api (preview Emergent)
app.include_router(router)
app.include_router(router, prefix="/api")


# Manejo global de excepciones de stock
@app.exception_handler(SinStockException)
def _stock_handler(_request: Request, exc: SinStockException):
    return JSONResponse(status_code=409, content={"detail": str(exc)})
