"""
Service layer para reservas — lógica de negocio.
"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from datetime import datetime
from models import Reserva, Mesa
from fastapi_app.repositories.reservas_repo import query_reservas, get_reserva, add_reserva, update_reserva


def obtener_reservas(db: Session, current_user, estado: Optional[str] = None, limit: int = 50) -> List[Reserva]:
    usuario_id = None if getattr(current_user, 'rol', None) == 'admin' else current_user.id
    return query_reservas(db, usuario_id, estado, limit)


def obtener_reserva(db: Session, reserva_id: int, current_user):
    reserva = get_reserva(db, reserva_id)
    if not reserva:
        return None
    if getattr(current_user, 'rol', None) != 'admin' and reserva.usuario_id != current_user.id:
        return 'forbidden'
    return reserva


def crear_reserva(db: Session, reserva_data, current_user):
    # Parsear fecha si es string
    fecha_dt = reserva_data.fecha_reserva
    if isinstance(fecha_dt, str):
        try:
            fecha_dt = datetime.fromisoformat(fecha_dt.replace(' ', 'T'))
        except:
            raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD HH:MM o ISO 8601")
    
    # Extraer fecha y hora del datetime
    fecha = fecha_dt.date()
    hora = fecha_dt.time()
    
    # Obtener número de personas
    num_personas = reserva_data.numero_personas or reserva_data.num_personas
    if not num_personas:
        raise ValueError("Debe especificar el número de personas")

    # Crear nueva reserva (sin validación de mesa ya que el modelo no usa mesa_id)
    nueva_reserva = Reserva(
        usuario_id=current_user.id,
        restaurante_id=1,
        fecha=fecha,
        hora=hora,
        numero_personas=num_personas,
        nombre_reserva=reserva_data.nombre_cliente or f"{current_user.nombre} {current_user.apellido}",
        telefono_reserva=reserva_data.telefono_cliente or current_user.telefono,
        email_reserva=reserva_data.email_cliente or current_user.email,
        notas_especiales=reserva_data.notas,
        estado='pendiente'
    )
    return add_reserva(db, nueva_reserva)


def actualizar_reserva(db: Session, reserva_id: int, reserva_data, current_user):
    reserva = get_reserva(db, reserva_id)
    if not reserva:
        return None
    if getattr(current_user, 'rol', None) != 'admin' and reserva.usuario_id != current_user.id:
        return 'forbidden'
    for field, value in reserva_data.model_dump(exclude_unset=True).items():
        setattr(reserva, field, value)
    return update_reserva(db, reserva)


def cancelar_reserva(db: Session, reserva_id: int, current_user):
    reserva = get_reserva(db, reserva_id)
    if not reserva:
        return False, 'not_found'
    if getattr(current_user, 'rol', None) != 'admin' and reserva.usuario_id != current_user.id:
        return False, 'forbidden'
    reserva.estado = 'cancelada'
    db.commit()
    return True, 'cancelled'
