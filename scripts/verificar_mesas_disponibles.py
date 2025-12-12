"""
Script para verificar las mesas disponibles en la base de datos
"""
import sys
sys.path.append('.')

from app import create_app
from models import Mesa, Pedido, db

app = create_app()

with app.app_context():
    print("="*60)
    print("VERIFICACIÓN DE MESAS DISPONIBLES")
    print("="*60)
    
    # 1. Total de mesas en la BD
    total_mesas = Mesa.query.count()
    print(f"\n📊 Total de mesas en BD: {total_mesas}")
    
    # 2. Mesas con disponible=True
    mesas_disponibles = Mesa.query.filter_by(disponible=True).all()
    print(f"✅ Mesas con disponible=True: {len(mesas_disponibles)}")
    
    # 3. Mesas ocupadas por pedidos activos
    pedidos_activos = Pedido.query.filter(
        Pedido.mesa_id.isnot(None),
        Pedido.estado.in_(['pendiente', 'preparando', 'enviado'])
    ).all()
    
    mesas_ocupadas_ids = set(p.mesa_id for p in pedidos_activos if p.mesa_id)
    print(f"🔒 Mesas ocupadas por pedidos activos: {len(mesas_ocupadas_ids)}")
    
    if mesas_ocupadas_ids:
        print(f"   IDs ocupadas: {sorted(mesas_ocupadas_ids)}")
    
    # 4. Mesas realmente disponibles (disponible=True Y sin pedido activo)
    mesas_libres = [m for m in mesas_disponibles if m.id not in mesas_ocupadas_ids]
    print(f"\n🎯 Mesas REALMENTE disponibles para seleccionar: {len(mesas_libres)}")
    
    if len(mesas_libres) > 0:
        print("\n📋 Lista de mesas disponibles:")
        for mesa in mesas_libres[:10]:  # Mostrar solo las primeras 10
            print(f"   • Mesa {mesa.numero} - Capacidad: {mesa.capacidad} - Tipo: {mesa.tipo} - Ubicación: {mesa.ubicacion}")
        
        if len(mesas_libres) > 10:
            print(f"   ... y {len(mesas_libres) - 10} mesas más")
    else:
        print("\n⚠️  NO HAY MESAS DISPONIBLES")
        print("   Todas están ocupadas o deshabilitadas")
    
    # 5. Detalles de pedidos activos
    if pedidos_activos:
        print(f"\n📦 Detalles de pedidos activos en mesas:")
        for pedido in pedidos_activos[:5]:  # Mostrar solo los primeros 5
            mesa = Mesa.query.get(pedido.mesa_id)
            mesa_num = mesa.numero if mesa else "?"
            usuario = pedido.usuario.nombre if pedido.usuario else "Desconocido"
            print(f"   • Pedido {pedido.codigo_pedido} - Mesa {mesa_num} - Usuario: {usuario} - Estado: {pedido.estado}")
        
        if len(pedidos_activos) > 5:
            print(f"   ... y {len(pedidos_activos) - 5} pedidos más")
    
    print("\n" + "="*60)
    print("✅ Verificación completada")
    print("="*60)
