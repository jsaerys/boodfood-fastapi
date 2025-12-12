"""
Script para actualizar TODAS las imágenes del menú con URLs completas de Unsplash
"""
import sys
sys.path.insert(0, 'c:/Users/LENOVO/Desktop/Proyec11')

from app import create_app

app = create_app()

with app.app_context():
    from models import db, MenuItem
    
    print("🖼️  Actualizando TODAS las imágenes del menú con URLs de Unsplash...\n")
    
    # Mapeo completo de TODOS los items con imágenes de alta calidad
    imagenes_completas = {
        # IDs 1-12 (ya tenían imágenes pero con rutas locales, actualizamos a URLs)
        1: 'https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=600&h=400&fit=crop',  # Alitas BBQ
        2: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&h=400&fit=crop',  # Hamburguesa Clásica
        3: 'https://images.unsplash.com/photo-1544025162-d76694265947?w=600&h=400&fit=crop',  # Lomo de Cerdo
        5: 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=600&h=400&fit=crop',  # Pasta Alfredo
        6: 'https://images.unsplash.com/photo-1523677011781-c91d1bbe2f4d?w=600&h=400&fit=crop',  # Limonada Natural
        7: 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&h=400&fit=crop',  # Jugo de Naranja
        8: 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=600&h=400&fit=crop',  # Gaseosa
        9: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&h=400&fit=crop',  # Brownie con Helado
        11: 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=600&h=400&fit=crop',  # Mojito
        12: 'https://images.unsplash.com/photo-1546171753-97d7676e4602?w=600&h=400&fit=crop',  # Piña Colada
        
        # IDs 13-25 (ya actualizados pero mejoramos las URLs)
        13: 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=600&h=400&fit=crop',  # Arroz chino
        14: 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&h=400&fit=crop',  # Papas Fritas
        15: 'https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=600&h=400&fit=crop',  # Alitas BBQ (6 unidades)
        16: 'https://images.unsplash.com/photo-1582169296194-e4d644c48063?w=600&h=400&fit=crop',  # Nachos con Queso
        17: 'https://images.unsplash.com/photo-1523677011781-c91d1bbe2f4d?w=600&h=400&fit=crop',  # Limonada Personal
        18: 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&h=400&fit=crop',  # Jugo Naranja Personal
        19: 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=600&h=400&fit=crop',  # Gaseosa Personal
        20: 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=600&h=400&fit=crop',  # Agua Embotellada
        21: 'https://images.unsplash.com/photo-1612392061787-2d078b3e573f?w=600&h=400&fit=crop',  # Perro Caliente
        22: 'https://images.unsplash.com/photo-1639024471283-03518883512d?w=600&h=400&fit=crop',  # Salchipapas
        23: 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=600&h=400&fit=crop',  # Leona (Cerveza)
        24: 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=600&h=400&fit=crop',  # Dorada (Cerveza)
        25: 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=600&h=400&fit=crop',  # Bogotá (Cerveza)
    }
    
    # Obtener todos los items
    todos_items = MenuItem.query.all()
    
    print(f"📊 Total items en BD: {len(todos_items)}\n")
    
    actualizados = 0
    
    for item in todos_items:
        if item.id in imagenes_completas:
            item.imagen_url = imagenes_completas[item.id]
            print(f"✅ ID {item.id:2d} - {item.nombre:30s} → {imagenes_completas[item.id][:60]}...")
            actualizados += 1
        else:
            # Si hay algún item sin mapear, le ponemos una imagen genérica de comida
            item.imagen_url = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&h=400&fit=crop'
            print(f"⚠️  ID {item.id:2d} - {item.nombre:30s} → Imagen genérica")
            actualizados += 1
    
    db.session.commit()
    
    print(f"\n✅ {actualizados} imágenes actualizadas correctamente!")
    print(f"\n🎯 Características de las URLs:")
    print(f"   - Alta resolución (600x400)")
    print(f"   - Optimizadas para web")
    print(f"   - CDN de Unsplash (carga rápida)")
    print(f"   - Crop automático para mantener aspecto")
    
    print(f"\n📱 Ahora verás las imágenes en:")
    print(f"   1. Página principal: http://localhost:5000/")
    print(f"   2. Menú completo: http://localhost:5000/menu")
    print(f"   3. Domicilios: http://localhost:5000/domicilios")
    print(f"   4. Panel admin → Menú")
    
    print(f"\n💡 Tip: Recarga el navegador con Ctrl+F5 para ver los cambios")
