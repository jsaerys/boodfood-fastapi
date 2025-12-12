"""
Routers de autenticación (login/register) usando auth_service
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..schemas import LoginRequest, LoginResponse, RegisterRequest, MessageResponse
from ..services.auth_service import login_user, register_user

router = APIRouter()


@router.post("/auth/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
	res, status_code = login_user(db, credentials.email, credentials.password)
	if status_code != 'ok':
		if status_code == 'inactive':
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
	return res


@router.post("/auth/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
	ok, reason = register_user(db, user_data)
	if not ok:
		if reason == 'exists':
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está registrado")
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al registrar usuario")
	return {"message": "Usuario registrado exitosamente", "success": True}
