"""Routers de usuarios (usa service + repository)."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..dependencies import get_db, get_current_user, require_admin
from ..schemas import UsuarioResponse, UsuarioCreate, UsuarioUpdate, MessageResponse
from ..services.usuarios_service import (
	obtener_usuarios, obtener_usuario, crear_usuario_admin, actualizar_usuario, eliminar_usuario
)

router = APIRouter()


@router.get("/usuarios", response_model=List[UsuarioResponse])
async def api_obtener_usuarios(
	activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
	rol: Optional[str] = Query(None, description="Filtrar por rol"),
	limit: int = Query(50, le=100, description="Límite de resultados"),
	db: Session = Depends(get_db),
	current_user = Depends(require_admin)
):
	return obtener_usuarios(db, activo, rol, limit)


@router.get("/usuarios/me", response_model=UsuarioResponse)
async def api_obtener_perfil(current_user = Depends(get_current_user)):
	return current_user


@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def api_obtener_usuario(
	usuario_id: int,
	db: Session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	res = obtener_usuario(db, usuario_id, current_user)
	if res is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
	if res == 'forbidden':
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para ver este usuario")
	return res


@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def api_crear_usuario(
	usuario_data: UsuarioCreate,
	db: Session = Depends(get_db),
	current_user = Depends(require_admin)
):
	try:
		return crear_usuario_admin(db, usuario_data)
	except ValueError as exc:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def api_actualizar_usuario(
	usuario_id: int,
	usuario_data: UsuarioUpdate,
	db: Session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	res = actualizar_usuario(db, usuario_id, usuario_data, current_user)
	if res is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
	if res == 'forbidden':
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para actualizar este usuario")
	if res == 'forbidden_role_change':
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes cambiar tu propio rol")
	return res


@router.delete("/usuarios/{usuario_id}", response_model=MessageResponse)
async def api_eliminar_usuario(
	usuario_id: int,
	db: Session = Depends(get_db),
	current_user = Depends(require_admin)
):
	ok, reason = eliminar_usuario(db, usuario_id, current_user)
	if not ok:
		if reason == 'cannot_delete_self':
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes eliminar tu propia cuenta")
		if reason == 'not_found':
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
	return {"message": "Usuario eliminado exitosamente", "success": True}
