"""
Rutas de mesas FastAPI
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..dependencies import get_db, get_current_user, require_admin
from ..schemas import MesaResponse, MesaCreate, MesaUpdate, MessageResponse
from ...app.models import Usuario, Mesa, Pedido

router = APIRouter()


@router.get("/mesas", response_model=List[MesaResponse])
async def obtener_mesas(
    disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo (interior, terraza, vip)"),
    db: Session = Depends(get_db)
):
    """Obtener lista de mesas"""
    
    query = db.query(Mesa)
    
    if disponible is not None:
        query = query.filter(Mesa.disponible == disponible)
    
    if tipo:
        query = query.filter(Mesa.tipo == tipo)
    
    mesas = query.order_by(Mesa.numero).all()
    
    # Agregar información de ocupación
    result = []
    for mesa in mesas:
        pedido_activo = db.query(Pedido).filter(
            Pedido.mesa_id == mesa.id,
            Pedido.estado.in_(['pendiente', 'preparando', 'enviado'])
        ).first()
        
        mesa_dict = {
            "id": mesa.id,
            "numero": mesa.numero,
            "capacidad": mesa.capacidad,
            "ubicacion": mesa.ubicacion,
            "tipo": mesa.tipo,
            "disponible": mesa.disponible,
            "ocupada": pedido_activo is not None
        }
        result.append(mesa_dict)
    
    return result


@router.get("/mesas/{mesa_id}", response_model=MesaResponse)
async def obtener_mesa(mesa_id: int, db: Session = Depends(get_db)):
    """Obtener mesa por ID"""
    
    mesa = db.get(Mesa, mesa_id)
    if not mesa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mesa no encontrada"
        )
    
    # Verificar si está ocupada
    pedido_activo = db.query(Pedido).filter(
        Pedido.mesa_id == mesa.id,
        Pedido.estado.in_(['pendiente', 'preparando', 'enviado'])
    ).first()
    
    return {
        "id": mesa.id,
        "numero": mesa.numero,
        "capacidad": mesa.capacidad,
        "ubicacion": mesa.ubicacion,
        "tipo": mesa.tipo,
        "disponible": mesa.disponible,
        "ocupada": pedido_activo is not None
    }


@router.post("/mesas", response_model=MesaResponse, status_code=status.HTTP_201_CREATED)
async def crear_mesa(
    mesa_data: MesaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Crear nueva mesa (solo admin)"""
    
    # Verificar si el número de mesa ya existe
    existing = db.query(Mesa).filter(Mesa.numero == mesa_data.numero).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una mesa con el número {mesa_data.numero}"
        )
    
    nueva_mesa = Mesa(
        numero=mesa_data.numero,
        capacidad=mesa_data.capacidad,
        ubicacion=mesa_data.ubicacion,
        tipo=mesa_data.tipo,
        disponible=mesa_data.disponible
    )
    
    db.add(nueva_mesa)
    db.commit()
    db.refresh(nueva_mesa)
    
    return nueva_mesa


@router.put("/mesas/{mesa_id}", response_model=MesaResponse)
async def actualizar_mesa(
    mesa_id: int,
    mesa_data: MesaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Actualizar mesa (solo admin)"""
    
    mesa = db.get(Mesa, mesa_id)
    if not mesa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mesa no encontrada"
        )
    
    # Actualizar campos
    for field, value in mesa_data.model_dump(exclude_unset=True).items():
        setattr(mesa, field, value)
    
    db.commit()
    db.refresh(mesa)
    
    return mesa


@router.delete("/mesas/{mesa_id}", response_model=MessageResponse)
async def eliminar_mesa(
    mesa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Eliminar mesa (solo admin)"""
    
    mesa = db.get(Mesa, mesa_id)
    if not mesa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mesa no encontrada"
        )
    
    # Verificar si tiene pedidos activos
    pedido_activo = db.query(Pedido).filter(
        Pedido.mesa_id == mesa.id,
        Pedido.estado.in_(['pendiente', 'preparando', 'enviado'])
    ).first()
    
    if pedido_activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar una mesa con pedidos activos"
        )
    
    db.delete(mesa)
    db.commit()
    
    return {
        "message": f"Mesa {mesa.numero} eliminada exitosamente",
        "success": True
    }
