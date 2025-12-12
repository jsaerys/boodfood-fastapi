"""
Routers para pedidos (usa service + repository)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from fastapi_app.dependencies import get_db, get_current_user
from fastapi_app.schemas import PedidoResponse, PedidoCreate, PedidoUpdate, MessageResponse
from fastapi_app.services.pedidos_service import (
	obtener_pedidos, obtener_pedido, crear_pedido, actualizar_pedido
)

router = APIRouter()


@router.get("/pedidos", response_model=List[PedidoResponse])
async def api_obtener_pedidos(
	estado: Optional[str] = Query(None, description="Filtrar por estado"),
	tipo_servicio: Optional[str] = Query(None, description="Filtrar por tipo de servicio"),
	limit: int = Query(50, le=100, description="Límite de resultados"),
	db: Session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	return obtener_pedidos(db, current_user, estado, tipo_servicio, limit)


@router.get("/pedidos/{pedido_id}", response_model=PedidoResponse)
async def api_obtener_pedido(
	pedido_id: int,
	db: Session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	res = obtener_pedido(db, pedido_id, current_user)
	if res is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
	if res == 'forbidden':
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para ver este pedido")
	return res


@router.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
async def api_crear_pedido(
	pedido_data: PedidoCreate,
	db: Session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	try:
		return crear_pedido(db, pedido_data, current_user)
	except ValueError as exc:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.put("/pedidos/{pedido_id}", response_model=PedidoResponse)
async def api_actualizar_pedido(
	pedido_id: int,
	pedido_data: PedidoUpdate,
	db: Session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	res = actualizar_pedido(db, pedido_id, pedido_data, current_user)
	if res is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
	if res == 'forbidden':
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para actualizar este pedido")
	return res

