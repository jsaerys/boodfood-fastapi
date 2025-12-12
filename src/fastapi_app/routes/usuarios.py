"""
Rutas de usuarios FastAPI
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..dependencies import get_db, get_current_user, require_admin
from ..schemas import UsuarioResponse, UsuarioCreate, UsuarioUpdate, MessageResponse
from ...app.models import Usuario
import bcrypt

router = APIRouter()


@router.get("/usuarios", response_model=List[UsuarioResponse])
async def obtener_usuarios(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    rol: Optional[str] = Query(None, description="Filtrar por rol"),
    limit: int = Query(50, le=100, description="Límite de resultados"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Obtener lista de usuarios (solo admin)"""
    
    query = db.query(Usuario)
    
    if activo is not None:
        query = query.filter(Usuario.activo == activo)
    
    if rol:
        query = query.filter(Usuario.rol == rol)
    
    usuarios = query.order_by(Usuario.fecha_registro.desc()).limit(limit).all()
    
    return usuarios


@router.get("/usuarios/me", response_model=UsuarioResponse)
async def obtener_perfil(current_user: Usuario = Depends(get_current_user)):
    """Obtener perfil del usuario actual"""
    return current_user


@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener usuario por ID"""
    
    # Solo admin puede ver otros usuarios
    if current_user.rol != 'admin' and usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este usuario"
        )
    
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return usuario


@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Crear nuevo usuario (solo admin)"""
    
    # Verificar si el email ya existe
    existing = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Hash de la contraseña
    hashed_password = bcrypt.hashpw(usuario_data.password.encode('utf-8'), bcrypt.gensalt())
    
    nuevo_usuario = Usuario(
        nombre=usuario_data.nombre,
        apellido=usuario_data.apellido,
        email=usuario_data.email,
        password_hash=hashed_password.decode('utf-8'),
        telefono=usuario_data.telefono,
        direccion=usuario_data.direccion,
        rol=usuario_data.rol,
        activo=usuario_data.activo
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario


@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar usuario"""
    
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Solo admin puede actualizar otros usuarios o cambiar roles
    if current_user.rol != 'admin':
        if usuario_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para actualizar este usuario"
            )
        
        # Usuario normal no puede cambiar su propio rol
        if usuario_data.rol is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puedes cambiar tu propio rol"
            )
    
    # Actualizar campos
    for field, value in usuario_data.model_dump(exclude_unset=True).items():
        setattr(usuario, field, value)
    
    db.commit()
    db.refresh(usuario)
    
    return usuario


@router.delete("/usuarios/{usuario_id}", response_model=MessageResponse)
async def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Eliminar usuario (solo admin)"""
    
    if usuario_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )
    
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    db.delete(usuario)
    db.commit()
    
    return {
        "message": f"Usuario {usuario.nombre} {usuario.apellido} eliminado exitosamente",
        "success": True
    }
