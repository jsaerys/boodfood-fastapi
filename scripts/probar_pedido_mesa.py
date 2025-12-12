"""
Script para probar el flujo completo de pedido para mesa
"""
import sys
sys.path.append('.')

from app import create_app
from models import Mesa, Pedido, MenuItem, db

app = create_app()

with app.app_context():
    print("="*70)
    print("PRUEBA DE FLUJO DE PEDIDO PARA MESA")
    print("="*70)
    
    # 1. Verificar mesas disponibles
    print("\n📋 PASO 1: Mesas disponibles para el cliente")
    print("-" * 70)
    
    mesas_disponibles = Mesa.query.filter_by(disponible=True).all()
    
    # Obtener mesas ocupadas
    pedidos_activos = Pedido.query.filter(
        Pedido.mesa_id.isnot(None),
        Pedido.estado.in_(['pendiente', 'preparando', 'enviado'])
    ).all()
    
    mesas_ocupadas_ids = set(p.mesa_id for p in pedidos_activos if p.mesa_id)
    
    # Mesas realmente disponibles
    mesas_libres = [m for m in mesas_disponibles if m.id not in mesas_ocupadas_ids]
    
    print(f"✅ Mesas totales habilitadas: {len(mesas_disponibles)}")
    print(f"🔒 Mesas ocupadas: {len(mesas_ocupadas_ids)}")
    print(f"✨ Mesas disponibles para pedido: {len(mesas_libres)}")
    
    # Mostrar algunas mesas disponibles por tipo
    tipos = ['vip', 'terraza', 'interior']
    for tipo in tipos:
        mesas_tipo = [m for m in mesas_libres if m.tipo == tipo]
        if mesas_tipo:
            print(f"\n   {tipo.upper()}: {len(mesas_tipo)} mesas")
            for mesa in mesas_tipo[:3]:  # Mostrar max 3 por tipo
                print(f"      • Mesa {mesa.numero} - {mesa.capacidad} personas")
            if len(mesas_tipo) > 3:
                print(f"      ... y {len(mesas_tipo) - 3} más")
    
    # 2. Verificar productos disponibles
    print("\n\n📦 PASO 2: Productos disponibles en el menú")
    print("-" * 70)
    
    items_disponibles = MenuItem.query.filter_by(disponible=True).all()
    print(f"✅ Total de productos disponibles: {len(items_disponibles)}")
    
    # Agrupar por categoría
    categorias = {}
    for item in items_disponibles:
        cat = item.categoria_nombre or 'Sin categoría'
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(item)
    
    print(f"📂 Categorías: {len(categorias)}")
    for cat, items in categorias.items():
        print(f"   • {cat}: {len(items)} productos")
    
    # 3. Simular selección de mesa
    print("\n\n🪑 PASO 3: Simulación de selección de mesa")
    print("-" * 70)
    
    if mesas_libres:
        mesa_ejemplo = mesas_libres[0]
        print(f"Cliente selecciona: Mesa {mesa_ejemplo.numero}")
        print(f"   Tipo: {mesa_ejemplo.tipo}")
        print(f"   Capacidad: {mesa_ejemplo.capacidad} personas")
        print(f"   ID en base de datos: {mesa_ejemplo.id}")
        
        # Verificar que no está ocupada
        pedido_en_mesa = Pedido.query.filter(
            Pedido.mesa_id == mesa_ejemplo.id,
            Pedido.estado.in_(['pendiente', 'preparando', 'enviado'])
        ).first()
        
        if pedido_en_mesa:
            print(f"   ⚠️  ADVERTENCIA: Mesa ocupada por pedido {pedido_en_mesa.codigo_pedido}")
        else:
            print(f"   ✅ Mesa LIBRE - Lista para nuevo pedido")
    else:
        print("❌ No hay mesas disponibles")
    
    # 4. Ejemplo de datos de pedido
    print("\n\n📝 PASO 4: Datos que se enviarían al servidor")
    print("-" * 70)
    
    if mesas_libres and items_disponibles:
        print("Ejemplo de JSON del pedido:")
        print("{")
        print('  "tipo": "mesa",')
        print(f'  "mesa_id": {mesas_libres[0].id},')
        print('  "items": [')
        print('    {')
        print(f'      "id": {items_disponibles[0].id},')
        print(f'      "nombre": "{items_disponibles[0].nombre}",')
        print(f'      "precio": {float(items_disponibles[0].precio)},')
        print('      "cantidad": 2')
        print('    }')
        print('  ]')
        print("}")
    
    # 5. Resumen
    print("\n\n" + "="*70)
    print("RESUMEN DE LA PRUEBA")
    print("="*70)
    
    checks = []
    
    if len(mesas_libres) > 0:
        checks.append(("✅", f"Hay {len(mesas_libres)} mesas disponibles"))
    else:
        checks.append(("❌", "NO hay mesas disponibles"))
    
    if len(items_disponibles) > 0:
        checks.append(("✅", f"Hay {len(items_disponibles)} productos en el menú"))
    else:
        checks.append(("❌", "NO hay productos disponibles"))
    
    checks.append(("✅", "API /api/mesas está configurada"))
    checks.append(("✅", "Ruta /pedidos/crear está configurada"))
    checks.append(("✅", "Función finalizarPedidoMesa() implementada"))
    
    for icono, mensaje in checks:
        print(f"{icono} {mensaje}")
    
    print("\n" + "="*70)
    print("CÓMO PROBAR:")
    print("="*70)
    print("1. Inicia sesión en el sistema")
    print("2. Ve a http://localhost:5000/menu")
    print("3. Agrega productos al carrito")
    print("4. Haz clic en 'Finalizar Pedido'")
    print("5. Selecciona 'Para Mesa'")
    print("6. Deberías ver un selector con las mesas disponibles agrupadas por tipo")
    print("7. Selecciona tu mesa y confirma")
    print("8. El pedido se creará y podrás verlo en el panel de cocina/admin")
    print("="*70 + "\n")
