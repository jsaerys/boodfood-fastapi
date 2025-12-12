"""
Repository layer para menu
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import MenuItem


def list_menu(db: Session, disponible: Optional[bool] = None, categoria: Optional[str] = None, destacado: Optional[bool] = None) -> List[MenuItem]:
    query = db.query(MenuItem)
    if disponible is not None:
        query = query.filter(MenuItem.disponible == disponible)
    if categoria:
        query = query.filter(MenuItem.categoria_nombre == categoria)
    if destacado is not None:
        query = query.filter(MenuItem.destacado == destacado)
    return query.order_by(MenuItem.orden, MenuItem.nombre).all()


def get_item(db: Session, item_id: int):
    return db.get(MenuItem, item_id)


def create_item(db: Session, item_obj: MenuItem):
    db.add(item_obj)
    db.commit()
    db.refresh(item_obj)
    return item_obj


def update_item(db: Session, item: MenuItem):
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item: MenuItem):
    db.delete(item)
    db.commit()


def list_categorias(db: Session):
    categorias = db.query(MenuItem.categoria_nombre).distinct().filter(
        MenuItem.categoria_nombre.isnot(None)
    ).all()
    return [c[0] for c in categorias if c[0]]
