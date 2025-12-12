"""
Repository layer para reservas
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from models import Reserva


def query_reservas(db: Session, usuario_id: Optional[int] = None, estado: Optional[str] = None, limit: int = 50) -> List[Reserva]:
    query = db.query(Reserva)
    if usuario_id is not None:
        query = query.filter(Reserva.usuario_id == usuario_id)
    if estado:
        query = query.filter(Reserva.estado == estado)
    return query.order_by(Reserva.fecha_reserva.desc()).limit(limit).all()


def get_reserva(db: Session, reserva_id: int) -> Optional[Reserva]:
    return db.get(Reserva, reserva_id)


def add_reserva(db: Session, reserva: Reserva) -> Reserva:
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva


def update_reserva(db: Session, reserva: Reserva) -> Reserva:
    db.commit()
    db.refresh(reserva)
    return reserva
