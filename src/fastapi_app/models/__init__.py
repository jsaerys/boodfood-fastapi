"""
Re-export de modelos del paquete raíz `models`.
Usar `fastapi_app.models` en lugar de importar directamente desde el paquete raíz
para facilitar la reorganización y los imports internos de FastAPI.
"""
from app.models import (
    db,
    Usuario,
    Mesa,
    MenuItem,
    Pedido,
    PedidoItem,
    Reserva,
    Categoria,
    Servicio,
    Inventario,
    InventarioMovimiento,
)

__all__ = [
    "db",
    "Usuario",
    "Mesa",
    "MenuItem",
    "Pedido",
    "PedidoItem",
    "Reserva",
    "Categoria",
    "Servicio",
    "Inventario",
    "InventarioMovimiento",
]
