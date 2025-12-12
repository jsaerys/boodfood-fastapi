"""
Repository layer para usuarios
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import Usuario


def list_usuarios(db: Session, activo: Optional[bool] = None, rol: Optional[str] = None, limit: int = 50) -> List[Usuario]:
    query = db.query(Usuario)
    if activo is not None:
        query = query.filter(Usuario.activo == activo)
    if rol:
        query = query.filter(Usuario.rol == rol)
    return query.order_by(Usuario.fecha_registro.desc()).limit(limit).all()


def get_usuario(db: Session, usuario_id: int) -> Optional[Usuario]:
    return db.get(Usuario, usuario_id)


def find_by_email(db: Session, email: str) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.email == email).first()


def create_usuario(db: Session, usuario: Usuario) -> Usuario:
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def update_usuario(db: Session, usuario: Usuario) -> Usuario:
    db.commit()
    db.refresh(usuario)
    return usuario


def delete_usuario(db: Session, usuario: Usuario) -> None:
    db.delete(usuario)
    db.commit()
