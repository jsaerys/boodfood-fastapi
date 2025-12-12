"""
Repository layer for mesas — encapsula queries a la base de datos.
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models import Mesa, Pedido


def list_mesas(db: Session, disponible: Optional[bool] = None, tipo: Optional[str] = None) -> List[Mesa]:
    query = db.query(Mesa)
    if disponible is not None:
        query = query.filter(Mesa.disponible == disponible)
    if tipo:
        query = query.filter(Mesa.tipo == tipo)
    return query.order_by(Mesa.numero).all()


def get_mesa(db: Session, mesa_id: int) -> Optional[Mesa]:
    return db.get(Mesa, mesa_id)


def create_mesa(db: Session, mesa_obj: Mesa) -> Mesa:
    db.add(mesa_obj)
    db.commit()
    db.refresh(mesa_obj)
    return mesa_obj


def update_mesa(db: Session, mesa: Mesa) -> Mesa:
    db.commit()
    db.refresh(mesa)
    return mesa


def delete_mesa(db: Session, mesa: Mesa) -> None:
    db.delete(mesa)
    db.commit()


def has_active_pedido(db: Session, mesa: Mesa) -> bool:
    pedido_activo = db.query(Pedido).filter(
        Pedido.mesa_id == mesa.id,
        Pedido.estado.in_(['pendiente', 'preparando', 'enviado'])
    ).first()
    return pedido_activo is not None
