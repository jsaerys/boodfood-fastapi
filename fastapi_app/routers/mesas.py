"""
Routers de mesas (usa service + repository).
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from fastapi_app.dependencies import get_db, require_admin
from fastapi_app.schemas import MesaResponse, MesaCreate, MesaUpdate, MessageResponse
from fastapi_app.services.mesas_service import (
	obtener_mesas, obtener_mesa, crear_mesa, actualizar_mesa, eliminar_mesa
)

router = APIRouter()


@router.get("/mesas", response_model=List[MesaResponse])
async def api_obtener_mesas(
	disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
	tipo: Optional[str] = Query(None, description="Filtrar por tipo (interior, terraza, vip)"),
	db: Session = Depends(get_db)
):
	return obtener_mesas(db, disponible, tipo)


@router.get("/mesas/{mesa_id}", response_model=MesaResponse)
async def api_obtener_mesa(mesa_id: int, db: Session = Depends(get_db)):
	res = obtener_mesa(db, mesa_id)
	if not res:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada")
	return res


@router.post("/mesas", response_model=MesaResponse, status_code=status.HTTP_201_CREATED)
async def api_crear_mesa(
	mesa_data: MesaCreate,
	db: Session = Depends(get_db),
	current_user = Depends(require_admin)
):
	return crear_mesa(db, mesa_data)


@router.put("/mesas/{mesa_id}", response_model=MesaResponse)
async def api_actualizar_mesa(
	mesa_id: int,
	mesa_data: MesaUpdate,
	db: Session = Depends(get_db),
	current_user = Depends(require_admin)
):
	updated = actualizar_mesa(db, mesa_id, mesa_data)
	if not updated:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada")
	return updated


@router.delete("/mesas/{mesa_id}", response_model=MessageResponse)
async def api_eliminar_mesa(
	mesa_id: int,
	db: Session = Depends(get_db),
	current_user = Depends(require_admin)
):
	ok, reason = eliminar_mesa(db, mesa_id)
	if not ok:
		if reason == 'not_found':
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada")
		if reason == 'has_active_pedido':
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar una mesa con pedidos activos")
	return {"message": f"Mesa {mesa_id} eliminada exitosamente", "success": True}

