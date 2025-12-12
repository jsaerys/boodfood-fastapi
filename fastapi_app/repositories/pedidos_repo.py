"""
Repository layer para pedidos: operaciones CRUD con Pedidos y PedidoItem.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from models import Pedido, PedidoItem


def query_pedidos(db: Session, usuario_id: Optional[int] = None, estado: Optional[str] = None, tipo_servicio: Optional[str] = None, limit: int = 50) -> List[Pedido]:
    query = db.query(Pedido)
    if usuario_id is not None:
        query = query.filter(Pedido.usuario_id == usuario_id)
    if estado:
        query = query.filter(Pedido.estado == estado)
    if tipo_servicio:
        query = query.filter(Pedido.tipo_servicio == tipo_servicio)
    return query.order_by(Pedido.created_at.desc()).limit(limit).all()


def get_pedido(db: Session, pedido_id: int) -> Optional[Pedido]:
    return db.get(Pedido, pedido_id)


def add_pedido(db: Session, pedido: Pedido) -> Pedido:
    db.add(pedido)
    db.flush()
    return pedido


def add_pedido_item(db: Session, pedido_item: PedidoItem) -> PedidoItem:
    db.add(pedido_item)
    return pedido_item


def commit(db: Session):
    db.commit()


def refresh(db: Session, obj):
    db.refresh(obj)


def update_pedido(db: Session, pedido: Pedido) -> Pedido:
    db.commit()
    db.refresh(pedido)
    return pedido
