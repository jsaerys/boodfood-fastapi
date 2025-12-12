"""
Script rápido para crear pedidos usando SQL directo
"""
import sys
sys.path.insert(0, 'c:/Users/LENOVO/Desktop/Proyec11')

from app import create_app

app = create_app()

with app.app_context():
    from models import db
    
    print("🔧 Creando 5 pedidos de prueba con SQL directo...\n")
    
    # Crear pedidos con SQL directo
    queries = [
        # Pedido 1 - Mesa 1
        "INSERT INTO pedidos (usuario_id, restaurante_id, codigo_pedido, subtotal, impuestos, total, estado, metodo_pago, mesa_id, tipo_servicio, fecha_pedido, nombre_receptor, telefono_contacto, created_at) VALUES (1, 1, 'TEST-001', 50000, 4000, 54000, 'pendiente', 'efectivo', 1, 'mesa', NOW(), 'Cliente 1', '3001111111', NOW())",
        
        # Pedido 2 - Mesa 2
        "INSERT INTO pedidos (usuario_id, restaurante_id, codigo_pedido, subtotal, impuestos, total, estado, metodo_pago, mesa_id, tipo_servicio, fecha_pedido, nombre_receptor, telefono_contacto, created_at) VALUES (1, 1, 'TEST-002', 75000, 6000, 81000, 'preparando', 'efectivo', 2, 'mesa', NOW(), 'Cliente 2', '3002222222', NOW())",
        
        # Pedido 3 - Mesa 3
        "INSERT INTO pedidos (usuario_id, restaurante_id, codigo_pedido, subtotal, impuestos, total, estado, metodo_pago, mesa_id, tipo_servicio, fecha_pedido, nombre_receptor, telefono_contacto, created_at) VALUES (1, 1, 'TEST-003', 100000, 8000, 108000, 'enviado', 'efectivo', 3, 'mesa', NOW(), 'Cliente 3', '3003333333', NOW())",
        
        # Pedido 4 - Mesa 4
        "INSERT INTO pedidos (usuario_id, restaurante_id, codigo_pedido, subtotal, impuestos, total, estado, metodo_pago, mesa_id, tipo_servicio, fecha_pedido, nombre_receptor, telefono_contacto, created_at) VALUES (1, 1, 'TEST-004', 65000, 5200, 70200, 'pendiente', 'efectivo', 4, 'mesa', NOW(), 'Cliente 4', '3004444444', NOW())",
        
        # Pedido 5 - Mesa 5
        "INSERT INTO pedidos (usuario_id, restaurante_id, codigo_pedido, subtotal, impuestos, total, estado, metodo_pago, mesa_id, tipo_servicio, fecha_pedido, nombre_receptor, telefono_contacto, created_at) VALUES (1, 1, 'TEST-005', 90000, 7200, 97200, 'preparando', 'efectivo', 5, 'mesa', NOW(), 'Cliente 5', '3005555555', NOW())",
    ]
    
    try:
        for i, query in enumerate(queries, 1):
            db.session.execute(db.text(query))
            print(f"✅ Pedido {i} creado en Mesa {i}")
        
        db.session.commit()
        
        print(f"\n✅ {len(queries)} pedidos creados exitosamente!")
        print(f"\n🎯 Ahora verás 5 mesas ocupadas en el dashboard del admin panel")
        print(f"   Recarga el panel de administración para ver el cambio")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error: {e}")
