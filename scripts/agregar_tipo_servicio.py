# Script para agregar columna tipo_servicio a la tabla pedidos
# Este script es necesario porque los pedidos ya creados no tienen este campo

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Pedido
import pymysql

def agregar_columna_tipo_servicio():
    """Agrega columna tipo_servicio a pedidos existentes"""
    
    app = create_app('development')
    
    with app.app_context():
        try:
            # Usar SQL directo para agregar la columna
            connection = db.engine.raw_connection()
            cursor = connection.cursor()
            
            print("📝 Verificando si la columna tipo_servicio ya existe...")
            
            # Verificar si la columna ya existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'pedidos' 
                AND COLUMN_NAME = 'tipo_servicio'
            """)
            
            exists = cursor.fetchone()[0]
            
            if exists:
                print("✅ La columna tipo_servicio ya existe")
            else:
                print("➕ Agregando columna tipo_servicio...")
                
                # Agregar columna con valor por defecto 'mesa'
                cursor.execute("""
                    ALTER TABLE pedidos 
                    ADD COLUMN tipo_servicio ENUM('mesa', 'domicilio', 'piscina', 'billar', 'eventos') 
                    DEFAULT 'mesa' 
                    AFTER mesa_id
                """)
                
                connection.commit()
                print("✅ Columna tipo_servicio agregada exitosamente")
            
            # Actualizar pedidos existentes para inferir el tipo correcto
            print("\n🔄 Actualizando tipo_servicio en pedidos existentes...")
            
            # Pedidos con dirección de entrega = domicilio
            cursor.execute("""
                UPDATE pedidos 
                SET tipo_servicio = 'domicilio' 
                WHERE direccion_entrega IS NOT NULL 
                AND direccion_entrega != ''
            """)
            domicilios = cursor.rowcount
            
            # Pedidos con mesa = mesa (ya está por defecto)
            cursor.execute("""
                UPDATE pedidos 
                SET tipo_servicio = 'mesa' 
                WHERE mesa_id IS NOT NULL 
                AND (direccion_entrega IS NULL OR direccion_entrega = '')
            """)
            mesas = cursor.rowcount
            
            connection.commit()
            
            print(f"✅ {domicilios} pedidos marcados como 'domicilio'")
            print(f"✅ {mesas} pedidos marcados como 'mesa'")
            
            cursor.close()
            connection.close()
            
            print("\n✅ Migración completada exitosamente")
            print("💡 Ahora los nuevos pedidos de piscina/billar/eventos se guardarán correctamente")
            
        except Exception as e:
            print(f"❌ Error en la migración: {str(e)}")
            raise

if __name__ == "__main__":
    print("="*60)
    print("🔧 MIGRACIÓN: Agregar campo tipo_servicio a pedidos")
    print("="*60)
    agregar_columna_tipo_servicio()
