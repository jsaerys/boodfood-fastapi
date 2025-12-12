"""
Rutas de pedidos FastAPI
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid
from ..dependencies import get_db, get_current_user
from ..schemas import PedidoResponse, PedidoCreate, PedidoUpdate, MessageResponse
from ...app.models import Usuario, Pedido, PedidoItem, MenuItem, Mesa

router = APIRouter()


@router.get("/pedidos", response_model=List[PedidoResponse])
async def obtener_pedidos(
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    tipo_servicio: Optional[str] = Query(None, description="Filtrar por tipo de servicio"),
    limit: int = Query(50, le=100, description="Límite de resultados"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener pedidos del usuario (o todos si es admin)"""
    
    query = db.query(Pedido)
    
    # Si no es admin, solo ver sus propios pedidos
    if current_user.rol != 'admin':
        query = query.filter(Pedido.usuario_id == current_user.id)
    
    if estado:
        query = query.filter(Pedido.estado == estado)
    
    if tipo_servicio:
        query = query.filter(Pedido.tipo_servicio == tipo_servicio)
    
    pedidos = query.order_by(Pedido.created_at.desc()).limit(limit).all()
    
    # Incluir items de cada pedido
    result = []
    for pedido in pedidos:
        items = db.query(PedidoItem).filter(PedidoItem.pedido_id == pedido.id).all()
        
        pedido_dict = {
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
        result.append(pedido_dict)
    
    return result


@router.get("/pedidos/{pedido_id}", response_model=PedidoResponse)
async def obtener_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener pedido por ID"""
    
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )
    
    # Verificar permisos
    if current_user.rol != 'admin' and pedido.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este pedido"
        )
    
    # Obtener items
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


@router.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
async def crear_pedido(
    pedido_data: PedidoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear nuevo pedido"""
    
    if not pedido_data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El pedido debe tener al menos un item"
        )
    
    # Validar mesa si es pedido para mesa
    if pedido_data.tipo_servicio == 'mesa':
        if not pedido_data.mesa_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe especificar una mesa para pedidos de tipo 'mesa'"
            )
        
        # Verificar que la mesa no esté ocupada por otro usuario
        pedido_existente = db.query(Pedido).filter(
            Pedido.mesa_id == pedido_data.mesa_id,
            Pedido.estado.in_(['pendiente', 'preparando', 'enviado']),
            Pedido.usuario_id != current_user.id
        ).first()
        
        if pedido_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La mesa seleccionada está ocupada por otro cliente"
            )
    
    # Calcular total
    total = sum(item.precio_unitario * item.cantidad for item in pedido_data.items)
    
    # Crear pedido
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
    
    db.add(nuevo_pedido)
    db.flush()
    
    # Crear items del pedido
    items_response = []
    for item_data in pedido_data.items:
        menu_item = db.get(MenuItem, item_data.menu_item_id)
        if not menu_item:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item del menú con ID {item_data.menu_item_id} no encontrado"
            )
        
        pedido_item = PedidoItem(
            pedido_id=nuevo_pedido.id,
            menu_item_id=item_data.menu_item_id,
            cantidad=item_data.cantidad,
            precio_unitario=item_data.precio_unitario,
            nombre_item=menu_item.nombre,
            subtotal=item_data.precio_unitario * item_data.cantidad
        )
        
        db.add(pedido_item)
        items_response.append({
            "id": 0,  # Se asignará después del commit
            "pedido_id": nuevo_pedido.id,
            "menu_item_id": pedido_item.menu_item_id,
            "cantidad": pedido_item.cantidad,
            "precio_unitario": pedido_item.precio_unitario,
            "nombre_item": pedido_item.nombre_item,
            "subtotal": pedido_item.subtotal
        })
    
    db.commit()
    db.refresh(nuevo_pedido)
    
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


@router.put("/pedidos/{pedido_id}", response_model=PedidoResponse)
async def actualizar_pedido(
    pedido_id: int,
    pedido_data: PedidoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar pedido"""
    
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )
    
    # Verificar permisos
    if current_user.rol != 'admin' and pedido.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar este pedido"
        )
    
    # Actualizar campos
    for field, value in pedido_data.model_dump(exclude_unset=True).items():
        setattr(pedido, field, value)
    
    db.commit()
    db.refresh(pedido)
    
    # Obtener items
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
