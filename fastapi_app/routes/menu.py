"""
Rutas de menú FastAPI
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_app.dependencies import get_db, require_admin
from fastapi_app.schemas import MenuItemResponse, MenuItemCreate, MenuItemUpdate, MessageResponse
from models import Usuario, MenuItem

router = APIRouter()


@router.get("/menu", response_model=List[MenuItemResponse])
async def obtener_menu(
    disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    destacado: Optional[bool] = Query(None, description="Solo items destacados"),
    db: Session = Depends(get_db)
):
    """Obtener items del menú"""
    
    query = db.query(MenuItem)
    
    if disponible is not None:
        query = query.filter(MenuItem.disponible == disponible)
    
    if categoria:
        query = query.filter(MenuItem.categoria_nombre == categoria)
    
    if destacado is not None:
        query = query.filter(MenuItem.destacado == destacado)
    
    items = query.order_by(MenuItem.orden, MenuItem.nombre).all()
    
    return items


@router.get("/menu/{item_id}", response_model=MenuItemResponse)
async def obtener_item(item_id: int, db: Session = Depends(get_db)):
    """Obtener item del menú por ID"""
    
    item = db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    
    return item


@router.post("/menu", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
async def crear_item(
    item_data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Crear nuevo item del menú (solo admin)"""
    
    nuevo_item = MenuItem(
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
    
    db.add(nuevo_item)
    db.commit()
    db.refresh(nuevo_item)
    
    return nuevo_item


@router.put("/menu/{item_id}", response_model=MenuItemResponse)
async def actualizar_item(
    item_id: int,
    item_data: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Actualizar item del menú (solo admin)"""
    
    item = db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    
    # Actualizar campos
    for field, value in item_data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    
    return item


@router.delete("/menu/{item_id}", response_model=MessageResponse)
async def eliminar_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Eliminar item del menú (solo admin)"""
    
    item = db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    
    db.delete(item)
    db.commit()
    
    return {
        "message": f"Item '{item.nombre}' eliminado exitosamente",
        "success": True
    }


@router.get("/categorias", response_model=List[str])
async def obtener_categorias(db: Session = Depends(get_db)):
    """Obtener lista de categorías únicas"""
    
    categorias = db.query(MenuItem.categoria_nombre).distinct().filter(
        MenuItem.categoria_nombre.isnot(None)
    ).all()
    
    return [cat[0] for cat in categorias if cat[0]]
