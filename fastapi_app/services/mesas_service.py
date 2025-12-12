"""
Service layer for mesas — lógica de negocio independiente de web.
"""
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from models import Mesa
from fastapi_app.repositories.mesas_repo import (
    list_mesas, get_mesa, create_mesa, update_mesa, delete_mesa, has_active_pedido
)


def obtener_mesas(db: Session, disponible: Optional[bool] = None, tipo: Optional[str] = None) -> List[Dict]:
    mesas = list_mesas(db, disponible, tipo)
    result = []
    for mesa in mesas:
        ocupada = has_active_pedido(db, mesa)
        mesa_dict = {
            "id": mesa.id,
            "numero": mesa.numero,
            "capacidad": mesa.capacidad,
            "ubicacion": mesa.ubicacion,
            "tipo": mesa.tipo,
            "disponible": mesa.disponible,
            "ocupada": ocupada
        }
        result.append(mesa_dict)
    return result


def obtener_mesa(db: Session, mesa_id: int) -> Optional[Dict]:
    mesa = get_mesa(db, mesa_id)
    if not mesa:
        return None
    ocupada = has_active_pedido(db, mesa)
    return {
        "id": mesa.id,
        "numero": mesa.numero,
        "capacidad": mesa.capacidad,
        "ubicacion": mesa.ubicacion,
        "tipo": mesa.tipo,
        "disponible": mesa.disponible,
        "ocupada": ocupada
    }


def crear_mesa(db: Session, mesa_data) -> Mesa:
    nueva = Mesa(
        numero=mesa_data.numero,
        capacidad=mesa_data.capacidad,
        ubicacion=mesa_data.ubicacion,
        tipo=mesa_data.tipo,
        disponible=mesa_data.disponible
    )
    return create_mesa(db, nueva)


def actualizar_mesa(db: Session, mesa_id: int, mesa_data) -> Optional[Mesa]:
    mesa = get_mesa(db, mesa_id)
    if not mesa:
        return None
    for field, value in mesa_data.model_dump(exclude_unset=True).items():
        setattr(mesa, field, value)
    return update_mesa(db, mesa)


def eliminar_mesa(db: Session, mesa_id: int) -> (bool, str):
    mesa = get_mesa(db, mesa_id)
    if not mesa:
        return False, "not_found"
    if has_active_pedido(db, mesa):
        return False, "has_active_pedido"
    delete_mesa(db, mesa)
    return True, "deleted"
