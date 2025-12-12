"""
Service layer para menu — lógica de negocio de items del menú
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models import MenuItem
from fastapi_app.repositories.menu_repo import (
    list_menu, get_item, create_item, update_item, delete_item, list_categorias
)


def obtener_menu(db: Session, disponible: Optional[bool] = None, categoria: Optional[str] = None, destacado: Optional[bool] = None) -> List[MenuItem]:
    return list_menu(db, disponible, categoria, destacado)


def obtener_item(db: Session, item_id: int):
    return get_item(db, item_id)


def crear_item(db: Session, item_data) -> MenuItem:
    nuevo = MenuItem(
        restaurante_id=item_data.restaurante_id,
        nombre=item_data.nombre,
        descripcion=item_data.descripcion,
        precio=item_data.precio,
        precio_descuento=item_data.precio_descuento,
        categoria_nombre=item_data.categoria_nombre,
        imagen_url=item_data.imagen_url,
        disponible=item_data.disponible,
        destacado=item_data.destacado
    )
    return create_item(db, nuevo)


def actualizar_item(db: Session, item_id: int, item_data):
    item = get_item(db, item_id)
    if not item:
        return None
    for field, value in item_data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    return update_item(db, item)


def eliminar_item(db: Session, item_id: int):
    item = get_item(db, item_id)
    if not item:
        return False, "not_found"
    delete_item(db, item)
    return True, "deleted"


def obtener_categorias(db: Session):
    return list_categorias(db)
