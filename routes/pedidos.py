"""
Rutas de gestión de pedidos
"""
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from datetime import datetime
import random
import string
from models import db, Pedido, PedidoItem, MenuItem

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/api/pedidos')


def generar_codigo_pedido():
    """Genera un código único para el pedido"""
    return 'PED-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


@pedidos_bp.route('/crear', methods=['POST'])
@login_required
def crear_pedido():
    """Crear un nuevo pedido"""
    try:
        data = request.get_json()
        
        # Validar datos
        if not data.get('items') or not data.get('metodo_pago'):
            return jsonify({'error': 'Datos incompletos'}), 400
        
        # Crear nuevo pedido
        nuevo_pedido = Pedido(
            usuario_id=current_user.id,
            restaurante_id=1,  # ID del restaurante BoodFood
            codigo_pedido=generar_codigo_pedido(),
            subtotal=0,
            total=0,
            estado='pendiente',
            metodo_pago=data['metodo_pago'],
            direccion_entrega=data.get('direccion_entrega'),
            telefono_contacto=data.get('telefono_contacto', current_user.telefono),
            nombre_receptor=data.get('nombre_receptor', current_user.nombre),
            instrucciones_entrega=data.get('instrucciones', '')
        )
        
        db.session.add(nuevo_pedido)
        db.session.flush()  # Para obtener el ID del pedido
        
        # Agregar items al pedido
        subtotal = 0
        for item_data in data['items']:
            menu_item = MenuItem.query.get(item_data['menu_item_id'])
            if not menu_item or not menu_item.disponible:
                db.session.rollback()
                return jsonify({'error': f'Item {item_data["menu_item_id"]} no disponible'}), 400
            
            cantidad = item_data['cantidad']
            precio_unitario = menu_item.precio
            item_subtotal = precio_unitario * cantidad
            
            pedido_item = PedidoItem(
                pedido_id=nuevo_pedido.id,
                menu_item_id=menu_item.id,
                nombre_item=menu_item.nombre,
                descripcion_item=menu_item.descripcion,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=item_subtotal
            )
            
            db.session.add(pedido_item)
            subtotal += item_subtotal
        
        nuevo_pedido.subtotal = subtotal
        nuevo_pedido.total = subtotal
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pedido creado exitosamente',
            'pedido': nuevo_pedido.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@pedidos_bp.route('/activo', methods=['GET'])
@login_required
def obtener_pedido_activo():
    """Obtener el pedido activo del usuario"""
    try:
        pedido = Pedido.query.filter_by(
            usuario_id=current_user.id,
            estado='pendiente'
        ).first()
        
        if pedido:
            return jsonify(pedido.to_dict())
        
        return jsonify({'pedido': None})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pedidos_bp.route('/<int:pedido_id>', methods=['GET'])
@login_required
def obtener_pedido(pedido_id):
    """Obtener detalles de un pedido"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        
        # Verificar permisos
        if pedido.usuario_id != current_user.id and current_user.rol not in ['admin', 'administrador', 'cocinero', 'cajero']:
            return jsonify({'error': 'No autorizado'}), 403
        
        return jsonify(pedido.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pedidos_bp.route('/mis-pedidos', methods=['GET'])
@login_required
def mis_pedidos():
    """Listar todos los pedidos del usuario"""
    try:
        pedidos = Pedido.query.filter_by(usuario_id=current_user.id).order_by(Pedido.fecha_pedido.desc()).all()
        return jsonify([pedido.to_dict() for pedido in pedidos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pedidos_bp.route('/<int:pedido_id>/cancelar', methods=['POST'])
@login_required
def cancelar_pedido(pedido_id):
    """Cancelar un pedido"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        
        # Verificar permisos
        if pedido.usuario_id != current_user.id and current_user.rol not in ['admin', 'administrador']:
            return jsonify({'error': 'No autorizado'}), 403
        
        if pedido.estado not in ['pendiente', 'preparando']:
            return jsonify({'error': 'No se puede cancelar este pedido'}), 400
        
        pedido.estado = 'cancelado'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pedido cancelado exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@pedidos_bp.route('/total-cuenta', methods=['GET'])
@login_required
def obtener_total_cuenta():
    """Obtener el total de la cuenta del usuario (suma de todos los pedidos activos)"""
    try:
        pedidos = Pedido.query.filter_by(
            usuario_id=current_user.id,
            estado='pendiente'
        ).all()
        
        total = sum(float(pedido.total) for pedido in pedidos)
        
        return jsonify({
            'total': total,
            'pedidos': [pedido.to_dict() for pedido in pedidos]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
