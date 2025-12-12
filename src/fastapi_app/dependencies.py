"""
Dependencias comunes para FastAPI
"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .models import db, Usuario
import jwt
from datetime import datetime, timedelta
from config.config import Config

# Seguridad
security = HTTPBearer()


async def get_db(request: Request):
    """Obtener sesión de base de datos.

    Esta versión es `async` para asegurarse de que el `app_context` se
    hace `push()` y `pop()` en el mismo hilo/loop donde FastAPI ejecuta la
    dependencia (evita que el `finally` se ejecute en otro worker thread).
    """
    flask_app = getattr(request.app.state, '_flask_app', None)

    # Si no hay Flask app en el state, devolvemos la sesión tal cual.
    if flask_app is None:
        try:
            yield db.session
        finally:
            db.session.close()

    else:
        ctx = flask_app.app_context()
        ctx.push()
        try:
            yield db.session
        finally:
            # Cerrar la sesión y sacar el contexto en el mismo hilo
            try:
                db.session.close()
            finally:
                ctx.pop()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear token JWT"""
    from datetime import timezone
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    
    # Convertir datetime a timestamp (segundos desde epoch)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_access_token(token: str):
    """Decodificar token JWT"""
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError as e:
        print(f"DEBUG: Token expirado: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except Exception as e:
        print(f"DEBUG: Error al decodificar token: {type(e).__name__}: {e}")
        print(f"DEBUG: Token recibido: {token[:50]}...")
        print(f"DEBUG: Secret key: {Config.SECRET_KEY}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {type(e).__name__}"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """Obtener usuario actual desde el token.

    Mantener la dependencia `HTTPBearer` permite que Swagger muestre
    el botón Authorize. Aquí extraemos el token desde `credentials`
    y lo validamos con `decode_access_token`.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token requerido"
        )

    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token vacío"
        )

    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido (sin user_id)"
        )

    usuario = db.get(Usuario, user_id)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return usuario


async def require_admin(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Requiere que el usuario sea administrador"""
    if current_user.rol != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: se requieren permisos de administrador"
        )
    return current_user
