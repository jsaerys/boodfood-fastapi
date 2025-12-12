"""
Routers para reservas (usa service + repository)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user
from ..schemas import ReservaResponse, ReservaCreate, ReservaUpdate, MessageResponse
from ..services.reservas_service import (
	obtener_reservas, obtener_reserva, crear_reserva, actualizar_reserva, cancelar_reserva
)

router = APIRouter()


@router.get("/reservas", response_model=List[ReservaResponse])
async def api_obtener_reservas(
	estado: Optional[str] = Query(None, description="Filtrar por estado"),
	limit: int = Query(50, le=100, description="Límite de resultados"),
	db: Session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	return obtener_reservas(db, current_user, estado, limit)


@router.get("/reservas/{reserva_id}", response_model=ReservaResponse)
async def api_obtener_reserva(
	reserva_id: int,
	db: Session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	res = obtener_reserva(db, reserva_id, current_user)
	if res is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
	if res == 'forbidden':
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para ver esta reserva")
	return res


@router.post("/reservas", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
async def api_crear_reserva(
	reserva_data: ReservaCreate,
	db: Session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	try:
		return crear_reserva(db, reserva_data, current_user)
	except ValueError as exc:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.put("/reservas/{reserva_id}", response_model=ReservaResponse)
async def api_actualizar_reserva(
	reserva_id: int,
	reserva_data: ReservaUpdate,
	db: Session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	res = actualizar_reserva(db, reserva_id, reserva_data, current_user)
	if res is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
	if res == 'forbidden':
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para actualizar esta reserva")
	return res


@router.delete("/reservas/{reserva_id}", response_model=MessageResponse)
async def api_cancelar_reserva(
	reserva_id: int,
	db: Session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	ok, reason = cancelar_reserva(db, reserva_id, current_user)
	if not ok:
		if reason == 'not_found':
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
		if reason == 'forbidden':
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para cancelar esta reserva")
	return {"message": "Reserva cancelada exitosamente", "success": True}

