"""
Service layer para usuarios — lógica de negocio relacionada con usuarios.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import Usuario
import bcrypt
from ..repositories.usuarios_repo import (
    list_usuarios, get_usuario, find_by_email, create_usuario, update_usuario, delete_usuario
)


def obtener_usuarios(db: Session, activo: Optional[bool] = None, rol: Optional[str] = None, limit: int = 50) -> List[Usuario]:
    return list_usuarios(db, activo, rol, limit)


def obtener_usuario(db: Session, usuario_id: int, current_user) -> Optional[Usuario]:
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        return None
    # permisos: sólo admin puede ver otros usuarios
    if getattr(current_user, 'rol', None) != 'admin' and usuario_id != current_user.id:
        return 'forbidden'
    return usuario


def crear_usuario_admin(db: Session, usuario_data) -> Usuario:
    existing = find_by_email(db, usuario_data.email)
    if existing:
        raise ValueError("El email ya está registrado")
    hashed_password = bcrypt.hashpw(usuario_data.password.encode('utf-8'), bcrypt.gensalt())
    nuevo = Usuario(
        nombre=usuario_data.nombre,
        apellido=usuario_data.apellido,
        email=usuario_data.email,
        password_hash=hashed_password.decode('utf-8'),
        telefono=usuario_data.telefono,
        direccion=usuario_data.direccion,
        rol=usuario_data.rol,
        activo=usuario_data.activo
    )
    return create_usuario(db, nuevo)


def actualizar_usuario(db: Session, usuario_id: int, usuario_data, current_user):
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        return None
    if getattr(current_user, 'rol', None) != 'admin':
        if usuario_id != current_user.id:
            return 'forbidden'
        if usuario_data.rol is not None:
            return 'forbidden_role_change'
    for field, value in usuario_data.model_dump(exclude_unset=True).items():
        setattr(usuario, field, value)
    return update_usuario(db, usuario)


def eliminar_usuario(db: Session, usuario_id: int, current_user):
    if usuario_id == current_user.id:
        return False, 'cannot_delete_self'
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        return False, 'not_found'
    delete_usuario(db, usuario)
    return True, 'deleted'
