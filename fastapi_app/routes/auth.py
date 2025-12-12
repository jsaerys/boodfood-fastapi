"""
Rutas de autenticación FastAPI
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi_app.dependencies import get_db, create_access_token
from fastapi_app.schemas import LoginRequest, LoginResponse, RegisterRequest, MessageResponse
from models import Usuario
import bcrypt

router = APIRouter()


@router.post("/auth/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Iniciar sesión y obtener token JWT"""
    
    # Buscar usuario por email
    usuario = db.query(Usuario).filter(Usuario.email == credentials.email).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Verificar contraseña
    if not bcrypt.checkpw(credentials.password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Verificar que el usuario esté activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Crear token
    access_token = create_access_token(data={"user_id": usuario.id, "email": usuario.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "rol": usuario.rol
        }
    }


@router.post("/auth/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""
    
    # Verificar si el email ya existe
    existing_user = db.query(Usuario).filter(Usuario.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Hash de la contraseña
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    
    # Crear nuevo usuario
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
    
    db.add(nuevo_usuario)
    db.commit()
    
    return {
        "message": "Usuario registrado exitosamente",
        "success": True
    }
