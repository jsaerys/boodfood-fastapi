"""
Rutas del panel de administrador - COMPLETO Y FUNCIONAL
"""
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, date, timedelta
from decimal import Decimal
from flask import current_app
from sqlalchemy import func
from ..models import db, MenuItem, Categoria, Usuario, Mesa, Mesero, Servicio, Pedido, PedidoItem, Reserva, Inventario, InventarioMovimiento

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
    """Panel de administración principal"""
    try:
        mesas = Mesa.query.order_by(Mesa.numero.asc()).all()
        mesas_config = [m.to_dict() for m in mesas]
    except Exception:
        mesas_config = []

    # ✅ AÑADIDO: estado_inicial con datos reales para evitar el error de Undefined
    try:
        pedidos = Pedido.query.order_by(Pedido.fecha_pedido.desc()).limit(20).all()
        pedidos_data = [p.to_dict() for p in pedidos]
        
        hoy = date.today()
        reservas = Reserva.query.filter(Reserva.fecha >= hoy).order_by(Reserva.fecha, Reserva.hora).limit(10).all()
        reservas_data = [r.to_dict() for r in reservas]
        
        inventario_bajo = Inventario.query.filter(Inventario.cantidad <= Inventario.stock_minimo).all()
        inventario_data = [i.to_dict() for i in inventario_bajo]

    except Exception as e:
        current_app.logger.error(f"Error al cargar estado_inicial: {e}")
        pedidos_data = []
        reservas_data = []
        inventario_data = []

    estado_inicial = {
        "mesas": mesas_config,
        "pedidos": pedidos_data,
        "reservas": reservas_data,
        "inventario_bajo": inventario_data
    }

    return render_template(
        'panels/admin.html',
        current_user_id=current_user.id,
        mesas_config=mesas_config,
        estado_inicial=estado_inicial  # ✅ Ahora sí se pasa
    )


# ===== USUARIOS =====

@admin_bp.route('/api/dashboard/stats', methods=['GET'])
@login_required
@admin_required
def dashboard_stats():
    """Estadísticas completas para el dashboard"""
    try:
        hoy = date.today()
        inicio_mes = date(hoy.year, hoy.month, 1)
        hace_7_dias = hoy - timedelta(days=7)
        hace_30_dias = hoy - timedelta(days=30)
        
        # Pedidos de hoy
        pedidos_hoy = Pedido.query.filter(
            func.date(Pedido.fecha_pedido) == hoy
        ).all()
        
        # Reservas de hoy
        reservas_hoy = Reserva.query.filter(Reserva.fecha == hoy).count()
        
        # Ventas de hoy
        ventas_hoy = sum(float(p.total) for p in pedidos_hoy)
        
        # Mesas
        total_mesas = Mesa.query.filter_by(disponible=True).count()
        
        # Mesas ocupadas: contar mesas con pedidos activos
        pedidos_activos = Pedido.query.filter(
            Pedido.mesa_id.isnot(None),
            Pedido.estado.in_(['pendiente', 'preparando', 'enviado'])
        ).all()
        mesas_ocupadas_ids = set(p.mesa_id for p in pedidos_activos if p.mesa_id)
        mesas_ocupadas = len(mesas_ocupadas_ids)
        
        # Pedidos pendientes
        pedidos_pendientes = Pedido.query.filter(Pedido.estado == 'pendiente').count()
        
        # Usuarios totales
        total_usuarios = Usuario.query.count()
        
        # Inventario bajo stock
        inventario_bajo = Inventario.query.filter(
            Inventario.cantidad <= Inventario.stock_minimo
        ).count()
        
        # Ventas del mes
        pedidos_mes = Pedido.query.filter(
            func.date(Pedido.fecha_pedido) >= inicio_mes
        ).all()
        ventas_mes = sum(float(p.total) for p in pedidos_mes)
        
        # Pedidos por estado (últimos 30 días)
        pedidos_30d = Pedido.query.filter(
            func.date(Pedido.fecha_pedido) >= hace_30_dias
        ).all()
        
        estados_count = {}
        for p in pedidos_30d:
            estados_count[p.estado] = estados_count.get(p.estado, 0) + 1
        
        # Ventas por día (últimos 7 días)
        ventas_por_dia = {}
        for i in range(7):
            dia = hoy - timedelta(days=i)
            pedidos_dia = Pedido.query.filter(
                func.date(Pedido.fecha_pedido) == dia
            ).all()
            ventas_por_dia[dia.strftime('%Y-%m-%d')] = sum(float(p.total) for p in pedidos_dia)
        
        # Top productos más vendidos
        from models import PedidoItem
        productos_vendidos = db.session.query(
            PedidoItem.menu_item_id,
            func.sum(PedidoItem.cantidad).label('total_vendido')
        ).join(Pedido).filter(
            func.date(Pedido.fecha_pedido) >= hace_30_dias
        ).group_by(PedidoItem.menu_item_id).order_by(
            func.sum(PedidoItem.cantidad).desc()
        ).limit(5).all()
        
        top_productos = []
        for item_id, cantidad in productos_vendidos:
            menu_item = MenuItem.query.get(item_id)
            if menu_item:
                top_productos.append({
                    'nombre': menu_item.nombre,
                    'cantidad': int(cantidad)
                })
        
        return jsonify({
            'pedidos_hoy': len(pedidos_hoy),
            'reservas_hoy': reservas_hoy,
            'ventas_hoy': ventas_hoy,
            'mesas_ocupadas': mesas_ocupadas,
            'total_mesas': total_mesas,
            'pedidos_pendientes': pedidos_pendientes,
            'total_usuarios': total_usuarios,
            'inventario_bajo': inventario_bajo,
            'ventas_mes': ventas_mes,
            'pedidos_mes': len(pedidos_mes),
            'estados_pedidos': estados_count,
            'ventas_por_dia': ventas_por_dia,
            'top_productos': top_productos
        })
    except Exception as e:
        current_app.logger.error(f'Error en dashboard_stats: {e}')
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/mesas', methods=['GET', 'POST'])
@login_required
@admin_required
def api_mesas():
    """Devuelve todas las mesas (GET) o crea una nueva (POST)"""
    if request.method == 'POST':
        data = request.get_json()
        numero = data.get('numero')
        capacidad = data.get('capacidad')
        tipo = data.get('tipo')
        
        if not numero or not capacidad or not tipo:
            return jsonify({'error': 'Faltan datos requeridos (numero, capacidad, tipo)'}), 400
            
        if Mesa.query.filter_by(numero=numero).first():
            return jsonify({'error': f'Ya existe una mesa con el número {numero}'}), 409
            
        try:
            nueva_mesa = Mesa(numero=numero, capacidad=capacidad, tipo=tipo, disponible=True)
            db.session.add(nueva_mesa)
            db.session.commit()
            return jsonify(nueva_mesa.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error al crear la mesa: {str(e)}'}), 500
            
    else: # GET
        mesas = Mesa.query.all()
        return jsonify([m.to_dict() for m in mesas])

@admin_bp.route('/api/mesas/<int:mesa_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_mesa(mesa_id):
    """Elimina una mesa específica"""
    mesa = Mesa.query.get_or_404(mesa_id)
    
    try:
        db.session.delete(mesa)
        db.session.commit()
        return jsonify({'message': f'Mesa {mesa_id} eliminada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar la mesa: {str(e)}'}), 500

@admin_bp.route('/api/mesas/<int:mesa_id>/actualizar', methods=['PUT'])
@login_required
@admin_required
def actualizar_mesa(mesa_id):
    """Actualiza todos los campos de una mesa"""
    mesa = Mesa.query.get_or_404(mesa_id)
    data = request.get_json()
    
    try:
        # Verificar si el nuevo número ya existe en otra mesa
        nuevo_numero = data.get('numero')
        if nuevo_numero and nuevo_numero != mesa.numero:
            if Mesa.query.filter_by(numero=nuevo_numero).first():
                return jsonify({'error': f'Ya existe una mesa con el número {nuevo_numero}'}), 409
        
        # Actualizar campos
        mesa.numero = data.get('numero', mesa.numero)
        mesa.capacidad = data.get('capacidad', mesa.capacidad)
        mesa.tipo = data.get('tipo', mesa.tipo)
        mesa.disponible = data.get('disponible', mesa.disponible)
        
        db.session.commit()
        return jsonify(mesa.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar la mesa: {str(e)}'}), 500

@admin_bp.route('/api/mesas/<int:mesa_id>/disponibilidad', methods=['PUT'])
@login_required
@admin_required
def toggle_disponibilidad_mesa(mesa_id):
    """Cambia solo el estado de disponibilidad de una mesa"""
    mesa = Mesa.query.get_or_404(mesa_id)
    data = request.get_json()
    
    try:
        mesa.disponible = data.get('disponible', not mesa.disponible)
        db.session.commit()
        return jsonify(mesa.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al cambiar disponibilidad: {str(e)}'}), 500


@admin_bp.route('/api/usuarios', methods=['GET'])
@login_required
@admin_required
def api_usuarios():
    """Devuelve todos los usuarios"""
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])

@admin_bp.route('/api/usuarios/crear', methods=['POST'])
@login_required
@admin_required
def crear_usuario():
    """Crea un nuevo usuario (solo para fines de admin)"""
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido', '')
    email = data.get('email')
    telefono = data.get('telefono', '')
    rol = data.get('rol', 'cliente')
    password = data.get('password')
    activo = data.get('activo', True)
    
    if not nombre or not email or not password:
        return jsonify({'error': 'Faltan datos requeridos (nombre, email, password)'}), 400
        
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': f'El email {email} ya está registrado'}), 409
    
    try:
        nuevo_usuario = Usuario(
            nombre=nombre, 
            apellido=apellido, 
            email=email, 
            telefono=telefono,
            rol=rol,
            activo=activo
        )
        nuevo_usuario.set_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify(nuevo_usuario.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear el usuario: {str(e)}'}), 500

@admin_bp.route('/api/usuarios/<int:user_id>/actualizar', methods=['PUT'])
@login_required
@admin_required
def actualizar_usuario(user_id):
    """Actualiza la información de un usuario"""
    usuario = Usuario.query.get_or_404(user_id)
    data = request.get_json()
    
    try:
        if 'nombre' in data:
            usuario.nombre = data['nombre']
        if 'apellido' in data:
            usuario.apellido = data['apellido']
        if 'email' in data:
            # Verificar que el email no esté en uso por otro usuario
            existing = Usuario.query.filter(Usuario.email == data['email'], Usuario.id != user_id).first()
            if existing:
                return jsonify({'error': 'El email ya está en uso'}), 409
            usuario.email = data['email']
        if 'telefono' in data:
            usuario.telefono = data['telefono']
        if 'rol' in data:
            roles_validos = ['cliente', 'mesero', 'cocinero', 'cajero', 'admin']
            if data['rol'] in roles_validos:
                usuario.rol = data['rol']
        if 'activo' in data:
            usuario.activo = data['activo']
        if 'password' in data and data['password']:
            usuario.set_password(data['password'])
        
        db.session.commit()
        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar usuario: {str(e)}'}), 500

@admin_bp.route('/api/usuarios/<int:user_id>/estado', methods=['PUT'])
@login_required
@admin_required
def cambiar_estado_usuario(user_id):
    """Cambia el estado activo/inactivo de un usuario"""
    usuario = Usuario.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'activo' not in data:
        return jsonify({'error': 'Estado no proporcionado'}), 400
    
    try:
        usuario.activo = data['activo']
        db.session.commit()
        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al cambiar estado: {str(e)}'}), 500

@admin_bp.route('/api/usuarios/<int:user_id>/rol', methods=['PUT'])
@login_required
@admin_required
def cambiar_rol(user_id):
    """Cambia el rol de un usuario"""
    usuario = Usuario.query.get_or_404(user_id)
    data = request.get_json()
    nuevo_rol = data.get('rol')
    
    if not nuevo_rol:
        return jsonify({'error': 'Rol no proporcionado'}), 400
        
    roles_validos = ['cliente', 'mesero', 'cocinero', 'cajero', 'admin']
    if nuevo_rol not in roles_validos:
        return jsonify({'error': f'Rol inválido: {nuevo_rol}'}), 400
        
    usuario.rol = nuevo_rol
    db.session.commit()
    
    return jsonify(usuario.to_dict())

@admin_bp.route('/api/usuarios/<int:user_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def eliminar_usuario_admin(user_id):
    """Elimina un usuario"""
    if user_id == current_user.id:
        return jsonify({'error': 'No puedes eliminar tu propia cuenta'}), 403
        
    usuario = Usuario.query.get_or_404(user_id)
    
    try:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': f'Usuario {user_id} eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar el usuario: {str(e)}'}), 500

@admin_bp.route('/api/usuarios/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def eliminar_usuario(user_id):
    """Alias para eliminar usuario (para compatibilidad con frontend)"""
    return eliminar_usuario_admin(user_id)


# ===== PEDIDOS =====

# ✅ MODIFICADO: Asegurar que to_dict() incluya el campo 'tipo'
@admin_bp.route('/api/pedidos')
@login_required
@admin_required
def api_pedidos():
    """Devuelve todos los pedidos con filtros opcionales por estado.

    Nota: El modelo Pedido no tiene un campo 'tipo', por lo que el filtrado
    de tipo (mesa/domicilio) se realiza en el frontend a partir de si el
    pedido tiene o no 'direccion_entrega'.
    """
    estado = request.args.get('estado')

    query = Pedido.query.order_by(Pedido.fecha_pedido.desc())

    if estado:
        query = query.filter(Pedido.estado == estado)

    pedidos = query.all()
    return jsonify([p.to_dict() for p in pedidos])


@admin_bp.route('/api/pedidos/<int:pedido_id>')
@login_required
@admin_required
def get_pedido(pedido_id):
    """Obtiene los detalles de un pedido específico"""
    pedido = Pedido.query.get_or_404(pedido_id)
    return jsonify(pedido.to_dict())

@admin_bp.route('/api/pedidos/<int:pedido_id>/estado', methods=['POST', 'PUT'])
@login_required
@admin_required
def update_pedido_estado(pedido_id):
    """Actualiza el estado de un pedido específico"""
    pedido = Pedido.query.get_or_404(pedido_id)
    data = request.get_json()
    nuevo_estado = data.get('estado')
    
    if not nuevo_estado:
        return jsonify({'error': 'Estado no proporcionado'}), 400
        
    estados_validos = ['pendiente', 'preparando', 'enviado', 'entregado', 'cancelado', 'rechazado']
    if nuevo_estado not in estados_validos:
        return jsonify({'error': f'Estado inválido: {nuevo_estado}'}), 400
        
    pedido.estado = nuevo_estado
    db.session.commit()
    
    try:
        from app import socketio
        socketio.emit('estado_pedido_actualizado', {'pedido_id': pedido.id, 'estado': nuevo_estado}, namespace='/')
    except ImportError:
        pass
    
    return jsonify({'message': f'Estado de pedido {pedido_id} actualizado a {nuevo_estado}', 'estado': nuevo_estado})


@admin_bp.route('/api/pedidos/<int:pedido_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_pedido(pedido_id):
    """Elimina un pedido específico"""
    pedido = Pedido.query.get_or_404(pedido_id)
    
    try:
        # Eliminar items del pedido primero (cascade debería hacerlo, pero por seguridad)
        for item in pedido.items:
            db.session.delete(item)
        
        # Eliminar el pedido
        db.session.delete(pedido)
        db.session.commit()
        
        return jsonify({'message': f'Pedido #{pedido.codigo_pedido} eliminado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar pedido: {str(e)}'}), 500


@admin_bp.route('/api/pedidos/<int:pedido_id>', methods=['PUT'])
@login_required
@admin_required
def update_pedido(pedido_id):
    """Actualiza un pedido completo"""
    pedido = Pedido.query.get_or_404(pedido_id)
    data = request.get_json()
    
    try:
        # Actualizar campos básicos si vienen en la petición
        if 'estado' in data:
            pedido.estado = data['estado']
        if 'metodo_pago' in data:
            pedido.metodo_pago = data['metodo_pago']
        if 'direccion_entrega' in data:
            pedido.direccion_entrega = data['direccion_entrega']
        if 'telefono_contacto' in data:
            pedido.telefono_contacto = data['telefono_contacto']
        if 'nombre_receptor' in data:
            pedido.nombre_receptor = data['nombre_receptor']
        if 'mesa_id' in data:
            pedido.mesa_id = data['mesa_id']
        if 'instrucciones_entrega' in data:
            pedido.instrucciones_entrega = data['instrucciones_entrega']
        
        pedido.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(pedido.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar pedido: {str(e)}'}), 500


@admin_bp.route('/api/usuarios/lista')
@login_required
@admin_required
def api_usuarios_lista():
    """Devuelve la lista de usuarios (solo nombre, email y rol)"""
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])


@admin_bp.route('/api/pedido/<int:pedido_id>/actualizar', methods=['PUT'])
@login_required
@admin_required
def actualizar_pedido(pedido_id):
    """Actualizar un pedido (estado, mesa, etc.)"""
    try:
        data = request.get_json()
        pedido = Pedido.query.get_or_404(pedido_id)
        
        if 'estado' in data:
            if data['estado'] in ['pendiente', 'preparando', 'enviado', 'entregado', 'cancelado', 'rechazado']:
                pedido.estado = data['estado']
        
        if 'mesa_id' in data:
            pedido.mesa_id = data['mesa_id']
        
        db.session.commit()
        return jsonify({'success': True, 'pedido': pedido.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===== RESERVAS =====
@admin_bp.route('/api/reservas', methods=['GET', 'POST'])
@login_required
@admin_required
def api_reservas():
    """Devuelve todas las reservas (GET) o crea una nueva (POST)"""
    if request.method == 'POST':
        data = request.get_json()
        
        if not data.get('fecha') or not data.get('hora') or not data.get('numero_personas') or not data.get('nombre_reserva'):
            return jsonify({'error': 'Faltan datos requeridos (fecha, hora, numero_personas, nombre_reserva)'}), 400
            
        try:
            nueva_reserva = Reserva(
                usuario_id=current_user.id,
                restaurante_id=1,
                fecha=datetime.strptime(data['fecha'], '%Y-%m-%d').date(),
                hora=datetime.strptime(data['hora'], '%H:%M').time(),
                numero_personas=data['numero_personas'],
                nombre_reserva=data['nombre_reserva'],
                email_reserva=data.get('email_reserva'),
                telefono_reserva=data.get('telefono_reserva'),
                zona_mesa=data.get('zona_mesa', 'interior'),
                estado='confirmada'
            )
            db.session.add(nueva_reserva)
            db.session.commit()
            
            try:
                from app import socketio
                socketio.emit('nueva_reserva', nueva_reserva.to_dict(), namespace='/')
            except ImportError:
                pass
            
            return jsonify(nueva_reserva.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error al crear la reserva: {str(e)}'}), 500
    else: # GET
        # Limitar a las últimas 300 reservas para mejor rendimiento
        reservas = Reserva.query.order_by(Reserva.id.desc()).limit(300).all()
        return jsonify([r.to_dict() for r in reservas])

@admin_bp.route('/api/reservas/<int:reserva_id>/estado', methods=['PUT'])
@login_required
@admin_required
def update_reserva_estado(reserva_id):
    """Actualiza el estado de una reserva específica"""
    reserva = Reserva.query.get_or_404(reserva_id)
    data = request.get_json()
    nuevo_estado = data.get('estado')
    
    if not nuevo_estado:
        return jsonify({'error': 'Estado no proporcionado'}), 400
        
    estados_validos = ['pendiente', 'confirmada', 'cancelada', 'completada', 'no_asistio']
    if nuevo_estado not in estados_validos:
        return jsonify({'error': f'Estado inválido: {nuevo_estado}'}), 400
        
    reserva.estado = nuevo_estado
    db.session.commit()
    
    try:
        from app import socketio
        socketio.emit('estado_reserva_actualizado', {'reserva_id': reserva.id, 'estado': nuevo_estado}, namespace='/')
    except ImportError:
        pass
    
    return jsonify(reserva.to_dict())


@admin_bp.route('/api/reservas/crear', methods=['POST'])
@login_required
@admin_required
def crear_reserva():
    """Crear una nueva reserva"""
    try:
        data = request.get_json()
        nueva = Reserva(
            usuario_id=data.get('usuario_id', current_user.id),
            restaurante_id=data.get('restaurante_id', 1),
            fecha=datetime.strptime(data['fecha'], '%Y-%m-%d').date(),
            hora=datetime.strptime(data['hora'], '%H:%M').time(),
            numero_personas=data['numero_personas'],
            nombre_reserva=data.get('nombre_reserva'),
            email_reserva=data.get('email_reserva'),
            telefono_reserva=data.get('telefono_reserva'),
            notas_especiales=data.get('notas_especiales'),
            estado=data.get('estado', 'pendiente'),
            metodo_pago=data.get('metodo_pago'),
            total_reserva=data.get('total_reserva', 0),
            zona_mesa=data.get('zona_mesa')
        )
        db.session.add(nueva)
        db.session.commit()
        return jsonify({'success': True, 'reserva': nueva.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@admin_bp.route('/api/menu/subir-imagen', methods=['POST'])
@login_required
@admin_required
def subir_imagen_menu():
    """Subir imagen para un item del menú"""
    try:
        if 'imagen' not in request.files:
            return jsonify({'error': 'No se seleccionó ninguna imagen'}), 400
        
        file = request.files['imagen']
        if file.filename == '':
            return jsonify({'error': 'Nombre de archivo vacío'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
            
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            url = f"/static/uploads/menu/{filename}"
            return jsonify({'success': True, 'url': url})
        
        return jsonify({'error': 'Formato de archivo no permitido'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/reserva/<int:reserva_id>/actualizar', methods=['PUT'])
@login_required
@admin_required
def actualizar_reserva(reserva_id):
    """Actualizar una reserva completa"""
    try:
        data = request.get_json()
        reserva = Reserva.query.get_or_404(reserva_id)
        
        # Actualizar campos simples
        for field in ['estado', 'mesa_asignada', 'zona_mesa', 'notas_especiales', 
                      'nombre_reserva', 'email_reserva', 'telefono_reserva', 
                      'numero_personas', 'total_reserva', 'metodo_pago']:
            if field in data:
                setattr(reserva, field, data[field])
        
        # Actualizar fecha y hora si vienen en el request
        if 'fecha' in data:
            reserva.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        if 'hora' in data:
            reserva.hora = datetime.strptime(data['hora'], '%H:%M').time()
        
        db.session.commit()
        
        # Emitir evento de actualización
        try:
            from app import socketio
            socketio.emit('reserva_actualizada', reserva.to_dict(), namespace='/')
        except ImportError:
            pass
        
        return jsonify({'success': True, 'reserva': reserva.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/reservas/<int:reserva_id>', methods=['GET'])
@login_required
@admin_required
def obtener_reserva(reserva_id):
    """Obtener una reserva específica"""
    try:
        reserva = Reserva.query.get_or_404(reserva_id)
        return jsonify(reserva.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/reservas/<int:reserva_id>/asignar-mesa', methods=['PUT'])
@login_required
@admin_required
def asignar_mesa_reserva(reserva_id):
    """Asignar mesa a una reserva específica"""
    try:
        data = request.get_json()
        reserva = Reserva.query.get_or_404(reserva_id)
        
        reserva.mesa_asignada = data.get('mesa_asignada')
        reserva.zona_mesa = data.get('zona_mesa', reserva.zona_mesa)
        
        db.session.commit()
        
        # Emitir evento de mesa asignada
        try:
            from app import socketio
            socketio.emit('mesa_asignada', {
                'reserva_id': reserva.id,
                'mesa': reserva.mesa_asignada,
                'zona': reserva.zona_mesa
            }, namespace='/')
        except ImportError:
            pass
        
        return jsonify({'success': True, 'reserva': reserva.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/reservas/<int:reserva_id>', methods=['DELETE'])
@login_required
@admin_required
def eliminar_reserva(reserva_id):
    """Eliminar una reserva (soft delete cambiando estado a cancelada)"""
    try:
        reserva = Reserva.query.get_or_404(reserva_id)
        
        # En lugar de eliminar, cambiar estado a cancelada
        reserva.estado = 'cancelada'
        db.session.commit()
        
        # Emitir evento de eliminación
        try:
            from app import socketio
            socketio.emit('reserva_eliminada', {'reserva_id': reserva_id}, namespace='/')
        except ImportError:
            pass
        
        return jsonify({'success': True, 'message': 'Reserva cancelada correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


## ===== INVENTARIO =====
@admin_bp.route('/api/inventario', methods=['GET', 'POST'])
@login_required
@admin_required
def api_inventario():
    """Devuelve todos los items de inventario (GET) o crea uno nuevo (POST)"""
    if request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')
        cantidad = data.get('cantidad')
        unidad = data.get('unidad')
        stock_minimo = data.get('stock_minimo', 0)
        
        if not nombre or not cantidad or not unidad:
            return jsonify({'error': 'Faltan datos requeridos (nombre, cantidad, unidad)'}), 400
            
        try:
            nuevo_item = Inventario(
                nombre=nombre,
                cantidad=Decimal(str(cantidad)),
                unidad=unidad,
                stock_minimo=Decimal(str(stock_minimo))
            )
            db.session.add(nuevo_item)
            db.session.commit()
            return jsonify(nuevo_item.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error al crear el item: {str(e)}'}), 500
    else: # GET
        items = Inventario.query.all()
        return jsonify([i.to_dict() for i in items])

@admin_bp.route('/api/inventario/<int:item_id>/movimiento', methods=['POST'])
@login_required
@admin_required
def registrar_movimiento(item_id):
    """Registra un movimiento de inventario (entrada o salida)"""
    item = Inventario.query.get_or_404(item_id)
    data = request.get_json()
    tipo = data.get('tipo')
    cantidad = data.get('cantidad')
    notas = data.get('notas')
    
    if tipo not in ['entrada', 'salida'] or not cantidad:
        return jsonify({'error': 'Tipo de movimiento o cantidad inválida'}), 400
        
    try:
        cantidad_movimiento = Decimal(str(cantidad))
        
        nuevo_movimiento = InventarioMovimiento(
            inventario_id=item.id,
            tipo=tipo,
            cantidad=cantidad_movimiento,
            usuario_id=current_user.id,
            notas=notas
        )
        db.session.add(nuevo_movimiento)
        
        if tipo == 'entrada':
            item.cantidad += cantidad_movimiento
        elif tipo == 'salida':
            if item.cantidad < cantidad_movimiento:
                return jsonify({'error': 'Stock insuficiente para esta salida'}), 400
            item.cantidad -= cantidad_movimiento
            
        db.session.commit()
        
        return jsonify({'message': 'Movimiento registrado', 'nueva_cantidad': float(item.cantidad)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al registrar movimiento: {str(e)}'}), 500

@admin_bp.route('/api/inventario/lista')
@login_required
@admin_required
def api_inventario_lista():
    """Devuelve todo el inventario"""
    items = Inventario.query.all()
    return jsonify([i.to_dict() for i in items])


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
            cantidad=Decimal(str(data['cantidad'])),
            unidad=data['unidad'],
            precio_unitario=Decimal(str(data.get('precio_unitario', 0))),
            stock_minimo=Decimal(str(data.get('stock_minimo', 0)))
        )
        db.session.add(nuevo_item)
        db.session.commit()
        return jsonify({'success': True, 'item': nuevo_item.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/inventario/<int:item_id>/actualizar', methods=['PUT'])
@login_required
@admin_required
def actualizar_item_inventario(item_id):
    """Actualizar un item de inventario"""
    try:
        item = Inventario.query.get_or_404(item_id)
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            item.nombre = data['nombre']
        if 'descripcion' in data:
            item.descripcion = data['descripcion']
        if 'unidad' in data:
            item.unidad = data['unidad']
        if 'precio_unitario' in data:
            item.precio_unitario = Decimal(str(data['precio_unitario'])) if data['precio_unitario'] else None
        if 'stock_minimo' in data:
            item.stock_minimo = Decimal(str(data['stock_minimo']))
        
        db.session.commit()
        return jsonify({'success': True, 'item': item.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/inventario/<int:item_id>', methods=['DELETE'])
@login_required
@admin_required
def eliminar_item_inventario(item_id):
    """Eliminar un item de inventario"""
    try:
        item = Inventario.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Item eliminado correctamente'})
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
        tipo = data.get('tipo')
        cantidad = Decimal(str(data.get('cantidad', 0)))
        
        if tipo not in ['entrada', 'salida']:
            return jsonify({'error': 'Tipo de movimiento inválido'}), 400
        
        if tipo == 'salida' and item.cantidad < cantidad:
            return jsonify({'error': 'Cantidad insuficiente en inventario'}), 400
        
        movimiento = InventarioMovimiento(
            inventario_id=item.id,
            tipo=tipo,
            cantidad=cantidad,
            usuario_id=current_user.id,
            notas=data.get('notas', '')
        )
        
        if tipo == 'entrada':
            item.cantidad += cantidad
        else:
            item.cantidad -= cantidad
        
        db.session.add(movimiento)
        db.session.commit()
        return jsonify({'success': True, 'item': item.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===== MENÚ =====

@admin_bp.route('/api/menu/crear', methods=['POST'])
@login_required
@admin_required
def crear_menu_item():
    """Crear un nuevo item del menú"""
    try:
        data = request.get_json() or {}

        nombre = data.get('nombre')
        precio = data.get('precio')
        if not nombre or precio is None:
            return jsonify({'error': 'nombre y precio son requeridos'}), 400

        restaurante_id = data.get('restaurante_id', 1)

        nuevo_item = MenuItem(
            restaurante_id=restaurante_id,
            nombre=nombre,
            descripcion=data.get('descripcion', ''),
            precio=float(precio),
            categoria_id=data.get('categoria_id'),
            imagen_url=data.get('imagen_url', ''),
            disponible=data.get('disponible', True)
        )
        db.session.add(nuevo_item)
        db.session.commit()
        return jsonify({'success': True, 'item': nuevo_item.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception('Error creando menu item')
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
            item.precio = float(data['precio'])
        if 'categoria_id' in data:
            item.categoria_id = data['categoria_id']
        if 'imagen_url' in data:
            item.imagen_url = data['imagen_url']
        if 'disponible' in data:
            item.disponible = data['disponible']
        
        db.session.commit()
        return jsonify({'success': True, 'item': item.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/menu/<int:item_id>', methods=['DELETE'])
@login_required
@admin_required
def eliminar_menu_item(item_id):
    """Eliminar un item del menú"""
    try:
        item = MenuItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Item eliminado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/categorias/lista')
@login_required
@admin_required
def api_categorias_lista():
    """Devuelve todas las categorías"""
    categorias = Categoria.query.all()
    return jsonify([c.to_dict() for c in categorias])


@admin_bp.route('/api/menu/items')
@login_required
@admin_required
def api_menu_items():
    """Devuelve todos los items del menú"""
    items = MenuItem.query.all()
    return jsonify([i.to_dict() for i in items])


# Nueva ruta para cargar contenido dinámico del menú
@admin_bp.route('/dashboard-content')
@login_required
@admin_required
def dashboard_content():
    """Devuelve solo el contenido HTML para la sección de dashboard"""
    return render_template('admin/dashboard_content.html')

@admin_bp.route('/pedidos-content')
@login_required
@admin_required
def pedidos_content():
    """Devuelve solo el contenido HTML para la sección de pedidos"""
    return render_template('admin/pedidos_content.html')

@admin_bp.route('/reservas-content')
@login_required
@admin_required
def reservas_content():
    """Devuelve solo el contenido HTML para la sección de reservas"""
    return render_template('admin/reservas_content.html')

@admin_bp.route('/usuarios-content')
@login_required
@admin_required
def usuarios_content():
    """Devuelve solo el contenido HTML para la sección de usuarios"""
    return render_template('admin/usuarios_content.html')

@admin_bp.route('/inventario-content')
@login_required
@admin_required
def inventario_content():
    """Devuelve solo el contenido HTML para la sección de inventario"""
    return render_template('admin/inventario_content.html')

@admin_bp.route('/mesas-content')
@login_required
@admin_required
def mesas_content():
    """Devuelve solo el contenido HTML para la sección de mesas"""
    return render_template('admin/mesas_content.html')

@admin_bp.route('/menu-content')
@login_required
@admin_required
def menu_content():
    """Devuelve solo el contenido HTML para la sección de menú"""
    return render_template('admin/menu_content.html')

@admin_bp.route('/notificaciones-content')
@login_required
@admin_required
def notificaciones_content():
    """Devuelve solo el contenido HTML para la sección de notificaciones"""
    return render_template('admin/notificaciones_content.html')

