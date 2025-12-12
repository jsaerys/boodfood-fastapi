"""
Routers para menú (usa service + repository)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from fastapi_app.dependencies import get_db, require_admin
from fastapi_app.schemas import MenuItemResponse, MenuItemCreate, MenuItemUpdate, MessageResponse
from fastapi_app.services.menu_service import (
	obtener_menu, obtener_item, crear_item, actualizar_item, eliminar_item, obtener_categorias
)

router = APIRouter()


@router.get("/menu", response_model=List[MenuItemResponse])
async def api_obtener_menu(
	disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
	categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
	destacado: Optional[bool] = Query(None, description="Solo items destacados"),
	db: Session = Depends(get_db)
):
	return obtener_menu(db, disponible, categoria, destacado)


@router.get("/menu/{item_id}", response_model=MenuItemResponse)
async def api_obtener_item(item_id: int, db: Session = Depends(get_db)):
	item = obtener_item(db, item_id)
	if not item:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
	return item


@router.post("/menu", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
async def api_crear_item(
	item_data: MenuItemCreate,
	db: Session = Depends(get_db),
	current_user = Depends(require_admin)
):
	return crear_item(db, item_data)


@router.put("/menu/{item_id}", response_model=MenuItemResponse)
async def api_actualizar_item(
	item_id: int,
	item_data: MenuItemUpdate,
	db: Session = Depends(get_db),
	current_user = Depends(require_admin)
):
	updated = actualizar_item(db, item_id, item_data)
	if not updated:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
	return updated


@router.delete("/menu/{item_id}", response_model=MessageResponse)
async def api_eliminar_item(
	item_id: int,
	db: Session = Depends(get_db),
	current_user = Depends(require_admin)
):
	ok, reason = eliminar_item(db, item_id)
	if not ok:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
	return {"message": f"Item eliminado exitosamente", "success": True}


@router.get("/categorias", response_model=List[str])
async def api_obtener_categorias(db: Session = Depends(get_db)):
	return obtener_categorias(db)

