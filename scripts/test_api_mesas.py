"""
Script para probar la API de mesas
"""
import sys
sys.path.insert(0, 'c:/Users/LENOVO/Desktop/Proyec11')

from app import create_app

app = create_app()

with app.app_context():
    from models import Mesa
    
    print("🔍 Probando obtención de mesas...\n")
    
    mesas = Mesa.query.filter_by(disponible=True).all()
    
    print(f"📊 Total mesas disponibles: {len(mesas)}\n")
    
    if mesas:
        print("✅ Primeras 10 mesas:")
        for mesa in mesas[:10]:
            data = mesa.to_dict()
            print(f"   Mesa {data['numero']}: {data['capacidad']} personas, {data['tipo']}, {data['ubicacion']}")
        
        print(f"\n📋 Resumen por tipo:")
        tipos = {}
        capacidades = {}
        
        for mesa in mesas:
            tipos[mesa.tipo] = tipos.get(mesa.tipo, 0) + 1
            capacidades[mesa.capacidad] = capacidades.get(mesa.capacidad, 0) + 1
        
        for tipo, count in tipos.items():
            print(f"   {tipo}: {count} mesas")
        
        print(f"\n👥 Resumen por capacidad:")
        for cap, count in sorted(capacidades.items()):
            print(f"   {cap} personas: {count} mesas")
    else:
        print("❌ No hay mesas disponibles en la base de datos")
