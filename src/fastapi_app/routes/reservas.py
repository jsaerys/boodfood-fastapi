"""
Rutas de reservas FastAPI
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from fastapi_app.dependencies import get_db, get_current_user
from fastapi_app.schemas import ReservaResponse, ReservaCreate, ReservaUpdate, MessageResponse
from models import Usuario, Reserva, Mesa

router = APIRouter()


@router.get("/reservas", response_model=List[ReservaResponse])
async def obtener_reservas(
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    limit: int = Query(50, le=100, description="Límite de resultados"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener reservas del usuario (o todas si es admin)"""
    
    query = db.query(Reserva)
    
    # Si no es admin, solo ver sus propias reservas
    if current_user.rol != 'admin':
        query = query.filter(Reserva.usuario_id == current_user.id)
    
    if estado:
        query = query.filter(Reserva.estado == estado)
    
    reservas = query.order_by(Reserva.fecha_reserva.desc()).limit(limit).all()
    
    return reservas


@router.get("/reservas/{reserva_id}", response_model=ReservaResponse)
async def obtener_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener reserva por ID"""
    
    reserva = db.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # Verificar permisos
    if current_user.rol != 'admin' and reserva.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta reserva"
        )
    
    return reserva


@router.post("/reservas", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
async def crear_reserva(
    reserva_data: ReservaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear nueva reserva"""
    
    # Verificar que la mesa existe
    mesa = db.get(Mesa, reserva_data.mesa_id)
    if not mesa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mesa no encontrada"
        )
    
    # Verificar que la mesa esté disponible
    if not mesa.disponible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La mesa seleccionada no está disponible"
        )
    
    # Verificar capacidad
    if reserva_data.num_personas > mesa.capacidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La mesa seleccionada tiene capacidad para {mesa.capacidad} personas, pero solicitaste {reserva_data.num_personas}"
        )
    
    # Verificar que no haya otra reserva para la misma mesa en la misma fecha
    reserva_existente = db.query(Reserva).filter(
        Reserva.mesa_id == reserva_data.mesa_id,
        Reserva.fecha_reserva == reserva_data.fecha_reserva,
        Reserva.estado.in_(['pendiente', 'confirmada'])
    ).first()
    
    if reserva_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una reserva para esta mesa en la fecha seleccionada"
        )
    
    # Crear reserva
    nueva_reserva = Reserva(
        usuario_id=current_user.id,
        restaurante_id=1,
        mesa_id=reserva_data.mesa_id,
        fecha_reserva=reserva_data.fecha_reserva,
        num_personas=reserva_data.num_personas,
        nombre_cliente=reserva_data.nombre_cliente,
        telefono_cliente=reserva_data.telefono_cliente,
        email_cliente=reserva_data.email_cliente or current_user.email,
        ocasion_especial=reserva_data.ocasion_especial,
        notas=reserva_data.notas,
        estado='pendiente'
    )
    
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    
    return nueva_reserva


@router.put("/reservas/{reserva_id}", response_model=ReservaResponse)
async def actualizar_reserva(
    reserva_id: int,
    reserva_data: ReservaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar reserva"""
    
    reserva = db.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # Verificar permisos
    if current_user.rol != 'admin' and reserva.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar esta reserva"
        )
    
    # Actualizar campos
    for field, value in reserva_data.model_dump(exclude_unset=True).items():
        setattr(reserva, field, value)
    
    db.commit()
    db.refresh(reserva)
    
    return reserva


@router.delete("/reservas/{reserva_id}", response_model=MessageResponse)
async def cancelar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Cancelar reserva"""
    
    reserva = db.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # Verificar permisos
    if current_user.rol != 'admin' and reserva.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para cancelar esta reserva"
        )
    
    # Cambiar estado a cancelada en lugar de eliminar
    reserva.estado = 'cancelada'
    db.commit()
    
    return {
        "message": "Reserva cancelada exitosamente",
        "success": True
    }
