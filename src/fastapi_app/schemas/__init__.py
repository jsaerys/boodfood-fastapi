"""
Esquemas Pydantic para validación de datos
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, time
from decimal import Decimal


# ==================== AUTH ====================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class RegisterRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    telefono: Optional[str] = None
    direccion: Optional[str] = None


# ==================== USUARIO ====================
class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    rol: str = "cliente"
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int
    fecha_registro: datetime
    ultima_sesion: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ==================== MESA ====================
class MesaBase(BaseModel):
    numero: int
    capacidad: int
    ubicacion: Optional[str] = None
    tipo: str = "interior"
    disponible: bool = True


class MesaCreate(MesaBase):
    pass


class MesaUpdate(BaseModel):
    numero: Optional[int] = None
    capacidad: Optional[int] = None
    ubicacion: Optional[str] = None
    tipo: Optional[str] = None
    disponible: Optional[bool] = None


class MesaResponse(MesaBase):
    id: int
    ocupada: bool = False
    
    model_config = ConfigDict(from_attributes=True)


# ==================== MENU ====================
class MenuItemBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=200)
    descripcion: Optional[str] = None
    precio: Decimal = Field(..., gt=0)
    precio_descuento: Optional[Decimal] = None
    categoria_nombre: Optional[str] = None
    imagen_url: Optional[str] = None
    disponible: bool = True
    destacado: bool = False


class MenuItemCreate(MenuItemBase):
    restaurante_id: int = 1


class MenuItemUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = None
    precio_descuento: Optional[Decimal] = None
    categoria_nombre: Optional[str] = None
    imagen_url: Optional[str] = None
    disponible: Optional[bool] = None
    destacado: Optional[bool] = None


class MenuItemResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    precio_descuento: Optional[Decimal] = None
    categoria_nombre: Optional[str] = None
    imagen_url: Optional[str] = None
    disponible: bool = True
    destacado: Optional[bool] = None
    restaurante_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ==================== PEDIDO ====================
class PedidoItemBase(BaseModel):
    menu_item_id: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: Decimal


class PedidoItemCreate(PedidoItemBase):
    pass


class PedidoItemResponse(PedidoItemBase):
    id: int
    pedido_id: int
    nombre_item: Optional[str] = None
    subtotal: Decimal
    
    model_config = ConfigDict(from_attributes=True)


class PedidoCreate(BaseModel):
    tipo_servicio: str = "mesa"  # mesa, domicilio, piscina, billar, eventos
    mesa_id: Optional[int] = None
    items: List[PedidoItemCreate]
    metodo_pago: str = "efectivo"
    direccion_entrega: Optional[str] = None
    telefono_contacto: Optional[str] = None
    instrucciones_entrega: Optional[str] = None


class PedidoUpdate(BaseModel):
    estado: Optional[str] = None
    mesa_id: Optional[int] = None
    metodo_pago: Optional[str] = None


class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    codigo_pedido: str
    tipo_servicio: str
    mesa_id: Optional[int] = None
    subtotal: Decimal
    total: Decimal
    estado: str
    metodo_pago: str
    fecha_pedido: datetime
    items: List[PedidoItemResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


# ==================== RESERVA ====================
class ReservaCreate(BaseModel):
    fecha_reserva: str  # "YYYY-MM-DD HH:MM"
    numero_personas: Optional[int] = Field(None, gt=0)
    num_personas: Optional[int] = Field(None, gt=0)  # soporte para ambos nombres
    nombre_cliente: Optional[str] = None
    telefono_cliente: Optional[str] = None
    email_cliente: Optional[EmailStr] = None
    ocasion_especial: Optional[str] = None
    notas: Optional[str] = None


class ReservaUpdate(BaseModel):
    estado: Optional[str] = None
    fecha_reserva: Optional[str] = None
    numero_personas: Optional[int] = None
    notas: Optional[str] = None


class ReservaResponse(BaseModel):
    id: int
    usuario_id: Optional[int] = None
    restaurante_id: Optional[int] = None
    fecha: Optional[datetime] = None
    hora: Optional[time] = None
    numero_personas: Optional[int] = None
    nombre_reserva: Optional[str] = None
    email_reserva: Optional[str] = None
    telefono_reserva: Optional[str] = None
    notas_especiales: Optional[str] = None
    codigo_reserva: Optional[str] = None
    estado: Optional[str] = None
    mesa_asignada: Optional[str] = None
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ==================== RESPUESTAS GENÉRICAS ====================
class MessageResponse(BaseModel):
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    success: bool = False
