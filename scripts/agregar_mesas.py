"""
Script para agregar más mesas a la base de datos
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models import Mesa

def agregar_mesas():
    app = create_app('development')
    with app.app_context():
        # Verificar cuántas mesas hay actualmente
        mesas_actuales = Mesa.query.count()
        print(f"Mesas actuales en la base de datos: {mesas_actuales}")
        
        # Definir nuevas mesas a agregar
        nuevas_mesas = [
            # Mesas Interior (2-4 personas)
            {"numero": 10, "capacidad": 2, "tipo": "interior", "disponible": True},
            {"numero": 11, "capacidad": 2, "tipo": "interior", "disponible": True},
            {"numero": 12, "capacidad": 4, "tipo": "interior", "disponible": True},
            {"numero": 13, "capacidad": 4, "tipo": "interior", "disponible": True},
            {"numero": 14, "capacidad": 4, "tipo": "interior", "disponible": True},
            {"numero": 15, "capacidad": 6, "tipo": "interior", "disponible": True},
            {"numero": 16, "capacidad": 8, "tipo": "interior", "disponible": True},
            {"numero": 17, "capacidad": 10, "tipo": "interior", "disponible": True},
            {"numero": 18, "capacidad": 12, "tipo": "interior", "disponible": True},
            
            # Mesas Terraza (2-6 personas)
            {"numero": 20, "capacidad": 2, "tipo": "terraza", "disponible": True},
            {"numero": 21, "capacidad": 2, "tipo": "terraza", "disponible": True},
            {"numero": 22, "capacidad": 4, "tipo": "terraza", "disponible": True},
            {"numero": 23, "capacidad": 4, "tipo": "terraza", "disponible": True},
            {"numero": 24, "capacidad": 6, "tipo": "terraza", "disponible": True},
            {"numero": 25, "capacidad": 6, "tipo": "terraza", "disponible": True},
            {"numero": 26, "capacidad": 4, "tipo": "terraza", "disponible": True},
            {"numero": 27, "capacidad": 2, "tipo": "terraza", "disponible": True},
            {"numero": 28, "capacidad": 8, "tipo": "terraza", "disponible": True},
            
            # Mesas VIP (4-8 personas)
            {"numero": 30, "capacidad": 4, "tipo": "vip", "disponible": True},
            {"numero": 31, "capacidad": 6, "tipo": "vip", "disponible": True},
            {"numero": 32, "capacidad": 8, "tipo": "vip", "disponible": True},
            {"numero": 33, "capacidad": 8, "tipo": "vip", "disponible": True},
            {"numero": 34, "capacidad": 10, "tipo": "vip", "disponible": True},
        ]
        
        mesas_agregadas = 0
        mesas_existentes = 0
        
        for mesa_data in nuevas_mesas:
            # Verificar si la mesa ya existe
            mesa_existente = Mesa.query.filter_by(numero=mesa_data["numero"]).first()
            
            if mesa_existente:
                print(f"⚠️  Mesa {mesa_data['numero']} ya existe - saltando")
                mesas_existentes += 1
            else:
                nueva_mesa = Mesa(
                    numero=mesa_data["numero"],
                    capacidad=mesa_data["capacidad"],
                    tipo=mesa_data["tipo"],
                    disponible=mesa_data["disponible"]
                )
                db.session.add(nueva_mesa)
                print(f"✅ Agregando Mesa {mesa_data['numero']} - Capacidad: {mesa_data['capacidad']}, Ubicación: {mesa_data['tipo']}")
                mesas_agregadas += 1
        
        # Guardar cambios
        db.session.commit()
        
        # Mostrar resumen
        total_mesas = Mesa.query.count()
        print("\n" + "="*60)
        print(f"✅ Proceso completado!")
        print(f"   Mesas agregadas: {mesas_agregadas}")
        print(f"   Mesas ya existentes: {mesas_existentes}")
        print(f"   Total de mesas en la base de datos: {total_mesas}")
        print("="*60)
        
        # Mostrar distribución por ubicación
        print("\n📊 Distribución de mesas:")
        for tipo in ['interior', 'terraza', 'vip']:
            count = Mesa.query.filter_by(tipo=tipo).count()
            print(f"   {tipo.capitalize()}: {count} mesas")

if __name__ == '__main__':
    agregar_mesas()
