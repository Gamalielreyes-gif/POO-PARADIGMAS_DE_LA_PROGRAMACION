# 🛒 Sistema de Tienda — POO + FastAPI

Refactor del proyecto original (Flask + bugs) a **FastAPI**, con:
- POO + arquitectura MVC
- Patrones de diseño: **Factory**, **Strategy**, **Observer**, **Singleton**
- SQLite para persistencia (en `/tmp` para compatibilidad con Vercel)
- Frontend HTML/CSS/JS plano servido por FastAPI
- Listo para desplegar en **Vercel**

---

## 📁 Estructura

```
/app/
├── tienda_app/                  # Núcleo del proyecto
│   ├── app.py                   # FastAPI: rutas y montaje
│   ├── model/                   # Producto, Inventario, Venta, Cliente, DB
│   ├── controller/              # Inventario / Venta controllers
│   ├── patterns/
│   │   ├── factory/             # ProductoFactory
│   │   ├── strategy/            # DescuentoFijo, DescuentoPorcentaje
│   │   └── observer/            # AlertaBajoStock
│   ├── utils/                   # SinStockException
│   └── view/
│       ├── templates/           # index, inventario, agregar, venta (HTML)
│       └── static/              # CSS + JS
├── api/
│   └── index.py                 # Entrypoint Vercel (reexporta app)
├── backend/server.py            # Entrypoint preview Emergent
├── vercel.json                  # Configuración Vercel
└── requirements.txt             # Deps para Vercel
```

---

## ▶️ Correr en local

```bash
cd /app
pip install -r requirements.txt
uvicorn tienda_app.app:app --reload --port 8000
# Abre http://localhost:8000
```

---

## 🚀 Desplegar en Vercel

### Paso 1 — Subir el código a GitHub
Sube el contenido de `/app` a un repo (puedes usar el botón **Save to GitHub** del chat).

### Paso 2 — Conectar con Vercel
1. Entra a <https://vercel.com> → **New Project**
2. Importa el repo de GitHub
3. Vercel detectará `vercel.json` automáticamente
4. Click en **Deploy**

### Paso 3 — Listo
Vercel servirá:
- `/` → Sistema de Tienda (UI)
- `/inventario`, `/venta`, etc. → API JSON
- `/docs` → Swagger UI generado por FastAPI

> ⚠️ **Nota:** SQLite vive en `/tmp` (único directorio escribible en Vercel
> serverless). Los datos se reinician en cada cold start con datos demo
> precargados (`seed_demo()` en `model/database.py`). Para persistencia real,
> migra a Neon/Turso/MongoDB Atlas.

---

## 🔌 Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Página principal |
| GET | `/inventario_view` | Vista HTML de inventario |
| GET | `/agregar_view` | Formulario para agregar producto |
| GET | `/venta_view` | UI para realizar venta |
| GET | `/inventario` | Lista todo el inventario (JSON) |
| POST | `/inventario/agregar` | Crea un producto (unitario o granel) |
| GET | `/inventario/buscar/{id}` | Busca por ID |
| GET | `/inventario/buscar_nombre/{n}` | Busca por nombre |
| GET | `/inventario/buscar_categoria/{c}` | Busca por categoría |
| GET | `/inventario/buscar_codigo/{cb}` | Busca por código de barras |
| DELETE | `/inventario/{id}` | Elimina producto |
| PUT | `/inventario/{id}/precio` | Actualiza precio |
| PUT | `/inventario/{id}/nombre` | Actualiza nombre |
| PUT | `/inventario/{id}/categoria` | Actualiza categoría |
| PUT | `/inventario/{id}/stock` | Aumenta/disminuye stock |
| POST | `/venta` | Procesa venta + ticket |
| GET | `/alertas` | Alertas de bajo stock (Observer) |
| DELETE | `/alertas` | Limpia alertas |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |

> Todas las rutas también responden con prefijo `/api` (ej. `/api/inventario`)
> para compatibilidad con entornos que filtran por `/api/*`.

---

## 🐛 Bugs corregidos del proyecto original

1. ❌ Import roto: `from controller.venta_controller` → archivo era `ventas_controller.py`
2. ❌ Faltaban `import DetalleVenta, Venta` en `ventas_controller.py`
3. ❌ Templates HTML con bloques markdown ` ``` ` mezclados (sintaxis rota)
4. ❌ Templates `agregar_view.html` y `venta.html` no existían
5. ❌ Carpeta `com.tienda.abarrotes` con puntos = nombre inválido como paquete Python
6. ❌ `get_connection()` usaba ruta relativa rota
7. ❌ CSS solicitado como `style.css` pero archivo era `Style.css` (mayúscula)
8. ❌ Inyección SQL en queries (formateo con f-strings)
9. ❌ Observer/Excepciones eran archivos vacíos
10. ❌ `producto_unitario.py` siempre prefijaba `10` aunque el id ya fuera completo

---

## 🧠 Patrones implementados

- **Factory** (`ProductoFactory`): crea productos unitario / granel
- **Strategy** (`DescuentoFijo`, `DescuentoPorcentaje`): descuentos intercambiables
- **Observer** (`AlertaBajoStock`): observa el inventario y registra alertas cuando stock < 5
- **Singleton** (`Inventario`): instancia única compartida en toda la app

---

## 👨‍💻 Autores originales
* García Reyes Gamaliel
* Montes Olivares Sergio Alonso
