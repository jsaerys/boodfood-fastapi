"""
Service layer for pedidos — contiene la lógica para crear/consultar/actualizar pedidos.
"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.models import Pedido, PedidoItem, MenuItem
from ..repositories.pedidos_repo import (
    query_pedidos, get_pedido, add_pedido, add_pedido_item, commit, refresh, update_pedido
)


def obtener_pedidos(db: Session, current_user, estado: Optional[str] = None, tipo_servicio: Optional[str] = None, limit: int = 50) -> List[Dict]:
    usuario_id = None if getattr(current_user, 'rol', None) == 'admin' else current_user.id
    pedidos = query_pedidos(db, usuario_id, estado, tipo_servicio, limit)
    result = []
    for pedido in pedidos:
        items = db.query(PedidoItem).filter(PedidoItem.pedido_id == pedido.id).all()
        result.append({
            "id": pedido.id,
            "usuario_id": pedido.usuario_id,
            "codigo_pedido": pedido.codigo_pedido,
            "tipo_servicio": pedido.tipo_servicio,
            "mesa_id": pedido.mesa_id,
            "subtotal": pedido.subtotal,
            "total": pedido.total,
            "estado": pedido.estado,
            "metodo_pago": pedido.metodo_pago,
            "fecha_pedido": pedido.fecha_pedido,
            "items": [
                {
                    "id": item.id,
                    "pedido_id": item.pedido_id,
                    "menu_item_id": item.menu_item_id,
                    "cantidad": item.cantidad,
                    "precio_unitario": item.precio_unitario,
                    "nombre_item": item.nombre_item,
                    "subtotal": item.subtotal
                }
                for item in items
            ]
        })
    return result


def obtener_pedido(db: Session, pedido_id: int, current_user) -> Optional[Dict]:
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        return None
    if getattr(current_user, 'rol', None) != 'admin' and pedido.usuario_id != current_user.id:
        return 'forbidden'
    items = db.query(PedidoItem).filter(PedidoItem.pedido_id == pedido.id).all()
    return {
        "id": pedido.id,
        "usuario_id": pedido.usuario_id,
        "codigo_pedido": pedido.codigo_pedido,
        "tipo_servicio": pedido.tipo_servicio,
        "mesa_id": pedido.mesa_id,
        "subtotal": pedido.subtotal,
        "total": pedido.total,
        "estado": pedido.estado,
        "metodo_pago": pedido.metodo_pago,
        "fecha_pedido": pedido.fecha_pedido,
        "items": [
            {
                "id": item.id,
                "pedido_id": item.pedido_id,
                "menu_item_id": item.menu_item_id,
                "cantidad": item.cantidad,
                "precio_unitario": item.precio_unitario,
                "nombre_item": item.nombre_item,
                "subtotal": item.subtotal
            }
            for item in items
        ]
    }


def crear_pedido(db: Session, pedido_data, current_user) -> Dict:
    if not pedido_data.items:
        raise ValueError("El pedido debe tener al menos un item")

    # Validar mesa
    if pedido_data.tipo_servicio == 'mesa':
        if not pedido_data.mesa_id:
            raise ValueError("Debe especificar una mesa para pedidos de tipo 'mesa'")
        pedido_existente = db.query(Pedido).filter(
            Pedido.mesa_id == pedido_data.mesa_id,
            Pedido.estado.in_(['pendiente', 'preparando', 'enviado']),
            Pedido.usuario_id != current_user.id
        ).first()
        if pedido_existente:
            raise ValueError("La mesa seleccionada está ocupada por otro cliente")

    total = sum(item.precio_unitario * item.cantidad for item in pedido_data.items)

    nuevo_pedido = Pedido(
        usuario_id=current_user.id,
        restaurante_id=1,
        codigo_pedido=f"PED{uuid.uuid4().hex[:8].upper()}",
        tipo_servicio=pedido_data.tipo_servicio,
        mesa_id=pedido_data.mesa_id,
        subtotal=total,
        total=total,
        estado='pendiente',
        metodo_pago=pedido_data.metodo_pago,
        direccion_entrega=pedido_data.direccion_entrega,
        telefono_contacto=pedido_data.telefono_contacto or current_user.telefono,
        nombre_receptor=f"{current_user.nombre} {current_user.apellido}",
        instrucciones_entrega=pedido_data.instrucciones_entrega,
        fecha_pedido=datetime.utcnow()
    )

    add_pedido(db, nuevo_pedido)

    items_response = []
    for item_data in pedido_data.items:
        menu_item = db.get(MenuItem, item_data.menu_item_id)
        if not menu_item:
            db.rollback()
            raise ValueError(f"Item del menú con ID {item_data.menu_item_id} no encontrado")

        pedido_item = PedidoItem(
            pedido_id=nuevo_pedido.id,
            menu_item_id=item_data.menu_item_id,
            cantidad=item_data.cantidad,
            precio_unitario=item_data.precio_unitario,
            nombre_item=menu_item.nombre,
            subtotal=item_data.precio_unitario * item_data.cantidad
        )
        add_pedido_item(db, pedido_item)
        items_response.append({
            "id": 0,
            "pedido_id": nuevo_pedido.id,
            "menu_item_id": pedido_item.menu_item_id,
            "cantidad": pedido_item.cantidad,
            "precio_unitario": pedido_item.precio_unitario,
            "nombre_item": pedido_item.nombre_item,
            "subtotal": pedido_item.subtotal
        })

    commit(db)
    refresh(db, nuevo_pedido)

    return {
        "id": nuevo_pedido.id,
        "usuario_id": nuevo_pedido.usuario_id,
        "codigo_pedido": nuevo_pedido.codigo_pedido,
        "tipo_servicio": nuevo_pedido.tipo_servicio,
        "mesa_id": nuevo_pedido.mesa_id,
        "subtotal": nuevo_pedido.subtotal,
        "total": nuevo_pedido.total,
        "estado": nuevo_pedido.estado,
        "metodo_pago": nuevo_pedido.metodo_pago,
        "fecha_pedido": nuevo_pedido.fecha_pedido,
        "items": items_response
    }


def actualizar_pedido(db: Session, pedido_id: int, pedido_data, current_user) -> Optional[Dict]:
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        return None
    if getattr(current_user, 'rol', None) != 'admin' and pedido.usuario_id != current_user.id:
        return 'forbidden'
    for field, value in pedido_data.model_dump(exclude_unset=True).items():
        setattr(pedido, field, value)
    update_pedido(db, pedido)
    items = db.query(PedidoItem).filter(PedidoItem.pedido_id == pedido.id).all()
    return {
        "id": pedido.id,
        "usuario_id": pedido.usuario_id,
        "codigo_pedido": pedido.codigo_pedido,
        "tipo_servicio": pedido.tipo_servicio,
        "mesa_id": pedido.mesa_id,
        "subtotal": pedido.subtotal,
        "total": pedido.total,
        "estado": pedido.estado,
        "metodo_pago": pedido.metodo_pago,
        "fecha_pedido": pedido.fecha_pedido,
        "items": [
            {
                "id": item.id,
                "pedido_id": item.pedido_id,
                "menu_item_id": item.menu_item_id,
                "cantidad": item.cantidad,
                "precio_unitario": item.precio_unitario,
                "nombre_item": item.nombre_item,
                "subtotal": item.subtotal
            }
            for item in items
        ]
    }
