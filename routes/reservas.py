"""
Rutas de gestión de reservas
"""
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from datetime import datetime
import random
import string
from models import db, Reserva, Mesa, Mesero, Servicio

reservas_bp = Blueprint('reservas', __name__, url_prefix='/api/reservas')


def generar_codigo_reserva():
    """Genera un código único para la reserva"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


@reservas_bp.route('/', methods=['GET'])
@login_required
def listar_reservas():
    """Listar reservas del usuario actual"""
    try:
        reservas = Reserva.query.filter_by(usuario_id=current_user.id).order_by(Reserva.created_at.desc()).all()
        return jsonify([reserva.to_dict() for reserva in reservas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reservas_bp.route('/crear', methods=['POST'])
@login_required
def crear_reserva():
    """Crear una nueva reserva"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('fecha') or not data.get('hora') or not data.get('numero_personas'):
            return jsonify({'error': 'Datos incompletos'}), 400
        
        # Parsear fecha y hora
        fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        hora = datetime.strptime(data['hora'], '%H:%M').time()
        
        # Crear reserva
        nueva_reserva = Reserva(
            usuario_id=current_user.id,
            restaurante_id=1,  # ID del restaurante BoodFood
            fecha=fecha,
            hora=hora,
            numero_personas=data['numero_personas'],
            nombre_reserva=data.get('nombre_reserva', current_user.nombre),
            email_reserva=data.get('email_reserva', current_user.email),
            telefono_reserva=data.get('telefono_reserva', current_user.telefono),
            notas_especiales=data.get('notas', ''),
            codigo_reserva=generar_codigo_reserva(),
            estado='pendiente',
            mesa_asignada=data.get('mesa_id'),
            zona_mesa=data.get('zona_mesa', 'interior')
        )
        
        db.session.add(nueva_reserva)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Reserva creada exitosamente',
            'reserva': nueva_reserva.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@reservas_bp.route('/<int:reserva_id>', methods=['GET'])
@login_required
def obtener_reserva(reserva_id):
    """Obtener detalles de una reserva"""
    try:
        reserva = Reserva.query.get_or_404(reserva_id)
        
        # Verificar que la reserva pertenece al usuario o es admin
        if reserva.usuario_id != current_user.id and current_user.rol not in ['admin', 'administrador']:
            return jsonify({'error': 'No autorizado'}), 403
        
        return jsonify(reserva.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reservas_bp.route('/<int:reserva_id>/cancelar', methods=['POST'])
@login_required
def cancelar_reserva(reserva_id):
    """Cancelar una reserva"""
    try:
        reserva = Reserva.query.get_or_404(reserva_id)
        
        # Verificar que la reserva pertenece al usuario o es admin
        if reserva.usuario_id != current_user.id and current_user.rol not in ['admin', 'administrador']:
            return jsonify({'error': 'No autorizado'}), 403
        
        reserva.estado = 'cancelada'
        reserva.fecha_cancelacion = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Reserva cancelada exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@reservas_bp.route('/disponibilidad', methods=['GET'])
def verificar_disponibilidad():
    """Verificar disponibilidad de mesas en una fecha"""
    try:
        fecha_str = request.args.get('fecha')
        
        if not fecha_str:
            return jsonify({'error': 'Fecha requerida'}), 400
        
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        # Obtener reservas para esa fecha
        reservas_fecha = Reserva.query.filter(
            Reserva.fecha == fecha,
            Reserva.estado.in_(['pendiente', 'confirmada'])
        ).all()
        
        mesas_reservadas = [r.mesa_asignada for r in reservas_fecha if r.mesa_asignada]
        
        # Obtener mesas disponibles
        mesas_disponibles = Mesa.query.filter(
            Mesa.disponible == True
        ).all()
        
        # Filtrar las que no están reservadas
        mesas_libres = [mesa for mesa in mesas_disponibles if str(mesa.numero) not in mesas_reservadas]
        
        return jsonify({
            'disponibles': [mesa.to_dict() for mesa in mesas_libres],
            'reservadas': mesas_reservadas
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
