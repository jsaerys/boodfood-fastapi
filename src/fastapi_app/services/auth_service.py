"""
Service layer para autenticación (login/register)
"""
from sqlalchemy.orm import Session
from app.models import Usuario
import bcrypt
from ..repositories.usuarios_repo import find_by_email, create_usuario
from ..dependencies import create_access_token


def login_user(db: Session, email: str, password: str):
    usuario = find_by_email(db, email)
    if not usuario:
        return None, "invalid"
    
    # Handle password_hash - convert to bytes if it's a string
    password_hash_bytes = usuario.password_hash
    if isinstance(password_hash_bytes, str):
        password_hash_bytes = password_hash_bytes.encode('utf-8')
    
    try:
        if not bcrypt.checkpw(password.encode('utf-8'), password_hash_bytes):
            return None, "invalid"
    except ValueError:
        # Invalid salt/hash format - return generic error
        return None, "invalid"
    
    if not usuario.activo:
        return None, "inactive"
    token = create_access_token(data={"user_id": usuario.id, "email": usuario.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "rol": usuario.rol
        }
    }, "ok"


def register_user(db: Session, user_data):
    existing = find_by_email(db, user_data.email)
    if existing:
        return False, "exists"
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    nuevo_usuario = Usuario(
        nombre=user_data.nombre,
        apellido=user_data.apellido,
        email=user_data.email,
        password_hash=hashed_password.decode('utf-8'),
        telefono=user_data.telefono,
        direccion=user_data.direccion,
        rol='cliente',
        activo=True
    )
    create_usuario(db, nuevo_usuario)
    return True, "created"
