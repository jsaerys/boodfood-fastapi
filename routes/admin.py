"""
Rutas del panel de administrador
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
from models import db, MenuItem, Usuario, Mesa, Mesero, Servicio
try:
    from models import Inventario, InventarioMovimiento
except ImportError:
    Inventario = None
    InventarioMovimiento = None

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorador para verificar que el usuario es administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'admin':
            return jsonify({'error': 'No autorizado'}), 403
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def panel_admin():
    """Panel de administración"""
    return render_template('panels/admin.html')


# ===== GESTIÓN DE INVENTARIO =====

@admin_bp.route('/api/inventario')
@login_required
@admin_required
def listar_inventario():
    """Listar todo el inventario"""
    items = Inventario.query.all()
    return jsonify([item.to_dict() for item in items])


@admin_bp.route('/api/inventario/crear', methods=['POST'])
@login_required
@admin_required
def crear_item_inventario():
    """Crear un nuevo item de inventario"""
    try:
        data = request.get_json()
        
        nuevo_item = Inventario(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            cantidad=data['cantidad'],
            unidad=data['unidad'],
            precio_unitario=data.get('precio_unitario'),
            stock_minimo=data.get('stock_minimo', 0)
        )
        
        db.session.add(nuevo_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item creado exitosamente',
            'item': nuevo_item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/inventario/<int:item_id>/movimiento', methods=['POST'])
@login_required
@admin_required
def registrar_movimiento_inventario(item_id):
    """Registrar entrada o salida de inventario"""
    try:
        data = request.get_json()
        
        item = Inventario.query.get_or_404(item_id)
        tipo = data.get('tipo')  # 'entrada' o 'salida'
        cantidad = float(data.get('cantidad', 0))
        
        if tipo not in ['entrada', 'salida']:
            return jsonify({'error': 'Tipo de movimiento inválido'}), 400
        
        # Registrar movimiento
        movimiento = InventarioMovimiento(
            inventario_id=item.id,
            tipo=tipo,
            cantidad=cantidad,
            usuario_id=current_user.id,
            notas=data.get('notas', '')
        )
        
        # Actualizar cantidad en inventario
        if tipo == 'entrada':
            item.cantidad += cantidad
        else:  # salida
            if item.cantidad < cantidad:
                return jsonify({'error': 'Cantidad insuficiente en inventario'}), 400
            item.cantidad -= cantidad
        
        db.session.add(movimiento)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Movimiento registrado exitosamente',
            'item': item.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/inventario/<int:item_id>/historial')
@login_required
@admin_required
def historial_inventario(item_id):
    """Obtener historial de movimientos de un item"""
    movimientos = InventarioMovimiento.query.filter_by(inventario_id=item_id).order_by(
        InventarioMovimiento.fecha_movimiento.desc()
    ).all()
    
    return jsonify([mov.to_dict() for mov in movimientos])


# ===== GESTIÓN DE MENÚ =====

@admin_bp.route('/api/menu/crear', methods=['POST'])
@login_required
@admin_required
def crear_menu_item():
    """Crear un nuevo item del menú"""
    try:
        data = request.get_json()
        
        nuevo_item = MenuItem(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            precio=data['precio'],
            categoria_id=data.get('categoria_id'),
            imagen=data.get('imagen', ''),
            tipo=data['tipo'],
            disponible=data.get('disponible', True)
        )
        
        db.session.add(nuevo_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item del menú creado exitosamente',
            'item': nuevo_item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/menu/<int:item_id>/actualizar', methods=['PUT'])
@login_required
@admin_required
def actualizar_menu_item(item_id):
    """Actualizar un item del menú"""
    try:
        data = request.get_json()
        item = MenuItem.query.get_or_404(item_id)
        
        if 'nombre' in data:
            item.nombre = data['nombre']
        if 'descripcion' in data:
            item.descripcion = data['descripcion']
        if 'precio' in data:
            item.precio = data['precio']
        if 'categoria_id' in data:
            item.categoria_id = data['categoria_id']
        if 'imagen' in data:
            item.imagen = data['imagen']
        if 'disponible' in data:
            item.disponible = data['disponible']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item actualizado exitosamente',
            'item': item.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===== GESTIÓN DE USUARIOS =====

@admin_bp.route('/api/usuarios')
@login_required
@admin_required
def listar_usuarios():
    """Listar todos los usuarios"""
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios])


@admin_bp.route('/api/usuario/<int:usuario_id>/rol', methods=['PUT'])
@login_required
@admin_required
def cambiar_rol_usuario(usuario_id):
    """Cambiar el rol de un usuario"""
    try:
        data = request.get_json()
        nuevo_rol = data.get('rol')
        
        if nuevo_rol not in ['cliente', 'mesero', 'cocinero', 'cajero', 'admin']:
            return jsonify({'error': 'Rol inválido'}), 400
        
        usuario = Usuario.query.get_or_404(usuario_id)
        usuario.rol = nuevo_rol
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Rol actualizado a {nuevo_rol}',
            'usuario': usuario.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===== GESTIÓN DE MESAS =====

@admin_bp.route('/api/mesas/crear', methods=['POST'])
@login_required
@admin_required
def crear_mesa():
    """Crear una nueva mesa"""
    try:
        data = request.get_json()
        
        nueva_mesa = Mesa(
            numero=data['numero'],
            capacidad=data['capacidad'],
            ubicacion=data.get('ubicacion', ''),
            tipo=data.get('tipo', 'interior'),
            disponible=data.get('disponible', True)
        )
        
        db.session.add(nueva_mesa)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mesa creada exitosamente',
            'mesa': nueva_mesa.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===== GESTIÓN DE MESEROS =====

@admin_bp.route('/api/meseros/crear', methods=['POST'])
@login_required
@admin_required
def crear_mesero():
    """Crear un nuevo mesero"""
    try:
        data = request.get_json()
        
        nuevo_mesero = Mesero(
            usuario_id=data.get('usuario_id'),
            nombre=data['nombre'],
            foto=data.get('foto', ''),
            especialidad=data.get('especialidad', ''),
            disponible=data.get('disponible', True)
        )
        
        db.session.add(nuevo_mesero)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mesero creado exitosamente',
            'mesero': nuevo_mesero.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===== GESTIÓN DE SERVICIOS =====

@admin_bp.route('/api/servicios/crear', methods=['POST'])
@login_required
@admin_required
def crear_servicio():
    """Crear un nuevo servicio"""
    try:
        data = request.get_json()
        
        nuevo_servicio = Servicio(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            precio=data['precio'],
            tipo=data['tipo'],
            capacidad=data.get('capacidad'),
            disponible=data.get('disponible', True)
        )
        
        db.session.add(nuevo_servicio)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Servicio creado exitosamente',
            'servicio': nuevo_servicio.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
