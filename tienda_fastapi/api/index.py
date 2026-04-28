"""
Entrada para Vercel.
Vercel ejecuta automáticamente cualquier archivo bajo /api/*.py
como una función serverless. Reexportamos la app FastAPI.
"""
import sys
from pathlib import Path

# /api/index.py vive 1 nivel debajo de la raíz del proyecto
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tienda_app.app import app  # noqa: E402,F401
