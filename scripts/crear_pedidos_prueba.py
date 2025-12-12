"""
Script para crear pedidos de prueba en mesas
"""
import sys
sys.path.insert(0, 'c:/Users/LENOVO/Desktop/Proyec11')

from app import create_app
from datetime import datetime
import random

app = create_app()

with app.app_context():
    from models import db, Pedido, PedidoItem, MenuItem, Mesa, Usuario
    from decimal import Decimal
    
    print("🔧 Creando pedidos de prueba en mesas...\n")
    
    # Obtener primer usuario
    usuario = Usuario.query.first()
    if not usuario:
        print("❌ No hay usuarios en el sistema")
        sys.exit(1)
    
    # Obtener primeros items del menú
    items = MenuItem.query.filter_by(disponible=True).limit(10).all()
    if not items:
        print("❌ No hay items en el menú")
        sys.exit(1)
    
    # Obtener algunas mesas
    mesas = Mesa.query.filter_by(disponible=True).limit(10).all()
    if not mesas:
        print("❌ No hay mesas disponibles")
        sys.exit(1)
    
    print(f"✅ Usuario: {usuario.nombre}")
    print(f"✅ Items disponibles: {len(items)}")
    print(f"✅ Mesas disponibles: {len(mesas)}\n")
    
    # Crear 5 pedidos en diferentes mesas
    pedidos_creados = 0
    estados = ['pendiente', 'preparando', 'enviado']
    
    for i in range(5):
        mesa = mesas[i]
        estado = random.choice(estados)
        
        # Crear pedido
        pedido = Pedido(
            usuario_id=usuario.id,
            restaurante_id=1,
            codigo_pedido=f'TEST-{datetime.now().strftime("%Y%m%d")}-{i+1:04d}',
            estado=estado,
            metodo_pago='efectivo',
            mesa_id=mesa.id,
            tipo_servicio='mesa',
            fecha_pedido=datetime.now(),
            subtotal=Decimal('0'),
            impuestos=Decimal('0'),
            total=Decimal('0'),
            nombre_receptor=usuario.nombre,
            telefono_contacto=usuario.telefono or '3001234567'
        )
        
        db.session.add(pedido)
        db.session.flush()
        
        # Agregar 2-4 items al pedido
        num_items = random.randint(2, 4)
        total_pedido = Decimal('0')
        
        for j in range(num_items):
            item = random.choice(items)
            cantidad = random.randint(1, 3)
            precio_unitario = Decimal(str(item.precio))
            subtotal_item = precio_unitario * cantidad
            
            pedido_item = PedidoItem(
                pedido_id=pedido.id,
                menu_item_id=item.id,
                nombre_item=item.nombre,
                descripcion_item=item.descripcion or '',
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal_item
            )
            
            db.session.add(pedido_item)
            total_pedido += subtotal_item
        
        # Actualizar totales del pedido
        pedido.subtotal = total_pedido
        pedido.impuestos = total_pedido * Decimal('0.08')  # 8% impuesto
        pedido.total = pedido.subtotal + pedido.impuestos
        
        print(f"✅ Pedido {pedido.codigo_pedido}:")
        print(f"   Mesa: {mesa.numero}")
        print(f"   Estado: {estado}")
        print(f"   Total: ${float(pedido.total):,.0f}")
        print(f"   Items: {num_items}\n")
        
        pedidos_creados += 1
    
    # Guardar en BD
    db.session.commit()
    
    print(f"\n✅ {pedidos_creados} pedidos creados exitosamente")
    print(f"\n📊 Resumen:")
    print(f"   Mesas ocupadas: {pedidos_creados}")
    print(f"   Total mesas: {len(mesas)}")
    print(f"\n🎯 Ahora podrás ver las mesas ocupadas en el dashboard!")
