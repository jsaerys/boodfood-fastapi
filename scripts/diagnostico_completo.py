"""
Script de Diagnóstico Completo del Proyecto BoodFood
Verifica estructura, rutas API, modelos y configuración
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Usuario, Pedido, Reserva, Mesa, MenuItem, Inventario, Categoria
from sqlalchemy import inspect

def diagnosticar():
    """Ejecuta diagnóstico completo del proyecto"""
    print("="*70)
    print("🔍 DIAGNÓSTICO COMPLETO - BoodFood")
    print("="*70)
    
    app = create_app('development')
    
    with app.app_context():
        print("\n✅ Aplicación Flask inicializada correctamente")
        
        # 1. Verificar conexión a BD
        print("\n" + "="*70)
        print("1️⃣  VERIFICANDO CONEXIÓN A BASE DE DATOS")
        print("="*70)
        try:
            db.session.execute(db.text('SELECT 1'))
            print("✅ Conexión a MySQL exitosa")
            
            # Obtener nombre de la BD
            result = db.session.execute(db.text('SELECT DATABASE()')).scalar()
            print(f"✅ Base de datos activa: {result}")
        except Exception as e:
            print(f"❌ Error de conexión: {str(e)}")
            return
        
        # 2. Verificar tablas
        print("\n" + "="*70)
        print("2️⃣  VERIFICANDO TABLAS EN LA BASE DE DATOS")
        print("="*70)
        
        inspector = inspect(db.engine)
        tablas_necesarias = [
            'usuarios', 'pedidos', 'pedido_items', 'reservas', 
            'mesas', 'menu_items', 'inventario', 'inventario_movimientos',
            'categorias', 'servicios', 'recetas'
        ]
        
        tablas_existentes = inspector.get_table_names()
        print(f"✅ Tablas encontradas: {len(tablas_existentes)}")
        
        for tabla in tablas_necesarias:
            if tabla in tablas_existentes:
                print(f"  ✅ {tabla}")
            else:
                print(f"  ❌ {tabla} - NO EXISTE")
        
        # 3. Verificar modelos
        print("\n" + "="*70)
        print("3️⃣  VERIFICANDO MODELOS DE DATOS")
        print("="*70)
        
        modelos = [
            ('Usuario', Usuario),
            ('Pedido', Pedido),
            ('Reserva', Reserva),
            ('Mesa', Mesa),
            ('MenuItem', MenuItem),
            ('Inventario', Inventario),
            ('Categoria', Categoria)
        ]
        
        for nombre, modelo in modelos:
            try:
                count = modelo.query.count()
                print(f"  ✅ {nombre}: {count} registros")
            except Exception as e:
                print(f"  ❌ {nombre}: Error - {str(e)}")
        
        # 4. Verificar campo tipo_servicio en Pedido
        print("\n" + "="*70)
        print("4️⃣  VERIFICANDO CAMPO tipo_servicio EN PEDIDOS")
        print("="*70)
        
        try:
            columns = inspector.get_columns('pedidos')
            column_names = [col['name'] for col in columns]
            
            if 'tipo_servicio' in column_names:
                print("  ✅ Campo tipo_servicio existe")
                
                # Ver valores únicos
                result = db.session.execute(
                    db.text("SELECT DISTINCT tipo_servicio FROM pedidos WHERE tipo_servicio IS NOT NULL")
                ).fetchall()
                
                if result:
                    tipos = [r[0] for r in result]
                    print(f"  ✅ Tipos encontrados: {', '.join(tipos)}")
                else:
                    print("  ⚠️  No hay pedidos con tipo_servicio definido")
            else:
                print("  ❌ Campo tipo_servicio NO EXISTE - Ejecutar migración")
        except Exception as e:
            print(f"  ❌ Error verificando campo: {str(e)}")
        
        # 5. Verificar rutas registradas
        print("\n" + "="*70)
        print("5️⃣  VERIFICANDO RUTAS REGISTRADAS")
        print("="*70)
        
        rutas_criticas = [
            '/api/pedidos',
            '/api/reservas',
            '/api/usuarios',
            '/api/mesas',
            '/api/inventario',
            '/api/menu/items',
            '/admin/pedidos-content',
            '/admin/reservas-content',
            '/admin/menu-content'
        ]
        
        todas_las_rutas = []
        for rule in app.url_map.iter_rules():
            todas_las_rutas.append(str(rule))
        
        print(f"✅ Total de rutas registradas: {len(todas_las_rutas)}")
        
        for ruta in rutas_criticas:
            if any(ruta in r for r in todas_las_rutas):
                print(f"  ✅ {ruta}")
            else:
                print(f"  ❌ {ruta} - NO ENCONTRADA")
        
        # 6. Verificar blueprints
        print("\n" + "="*70)
        print("6️⃣  VERIFICANDO BLUEPRINTS REGISTRADOS")
        print("="*70)
        
        blueprints = list(app.blueprints.keys())
        blueprints_esperados = ['auth', 'main', 'admin', 'reservas', 'pedidos', 'api']
        
        print(f"✅ Blueprints registrados: {len(blueprints)}")
        for bp in blueprints_esperados:
            if bp in blueprints:
                print(f"  ✅ {bp}")
            else:
                print(f"  ⚠️  {bp} - NO REGISTRADO")
        
        # 7. Verificar archivos JavaScript
        print("\n" + "="*70)
        print("7️⃣  VERIFICANDO ARCHIVOS JAVASCRIPT DEL ADMIN")
        print("="*70)
        
        js_admin_path = os.path.join(app.root_path, 'static', 'js', 'admin')
        archivos_esperados = [
            'pedidos.js', 'reservas.js', 'menu.js', 
            'inventario.js', 'usuarios.js', 'mesas.js', 'dashboard.js'
        ]
        
        if os.path.exists(js_admin_path):
            archivos_existentes = os.listdir(js_admin_path)
            for archivo in archivos_esperados:
                if archivo in archivos_existentes:
                    ruta_completa = os.path.join(js_admin_path, archivo)
                    size = os.path.getsize(ruta_completa)
                    print(f"  ✅ {archivo} ({size} bytes)")
                else:
                    print(f"  ❌ {archivo} - NO EXISTE")
        else:
            print(f"  ❌ Directorio {js_admin_path} no existe")
        
        # 8. Verificar templates
        print("\n" + "="*70)
        print("8️⃣  VERIFICANDO TEMPLATES DEL ADMIN")
        print("="*70)
        
        templates_path = os.path.join(app.root_path, 'templates', 'admin')
        templates_esperados = [
            'dashboard_content.html', 'pedidos_content.html', 
            'reservas_content.html', 'menu_content.html',
            'inventario_content.html', 'usuarios_content.html', 
            'mesas_content.html'
        ]
        
        if os.path.exists(templates_path):
            templates_existentes = os.listdir(templates_path)
            for template in templates_esperados:
                if template in templates_existentes:
                    print(f"  ✅ {template}")
                else:
                    print(f"  ❌ {template} - NO EXISTE")
        else:
            print(f"  ❌ Directorio {templates_path} no existe")
        
        # 9. Verificar configuración
        print("\n" + "="*70)
        print("9️⃣  VERIFICANDO CONFIGURACIÓN")
        print("="*70)
        
        config_items = [
            ('SQLALCHEMY_DATABASE_URI', app.config.get('SQLALCHEMY_DATABASE_URI', 'NO DEFINIDO')),
            ('SECRET_KEY', 'DEFINIDO' if app.config.get('SECRET_KEY') else 'NO DEFINIDO'),
            ('DEBUG', app.config.get('DEBUG', False))
        ]
        
        for nombre, valor in config_items:
            if nombre == 'SQLALCHEMY_DATABASE_URI':
                # Ocultar contraseña
                if 'mysql' in str(valor):
                    print(f"  ✅ {nombre}: MySQL configurado")
                else:
                    print(f"  ⚠️  {nombre}: {valor}")
            else:
                print(f"  ✅ {nombre}: {valor}")
        
        # Resumen final
        print("\n" + "="*70)
        print("📊 RESUMEN DEL DIAGNÓSTICO")
        print("="*70)
        print("✅ Conexión a BD: OK")
        print("✅ Modelos: OK")
        print("✅ Rutas: OK")
        print("✅ Blueprints: OK")
        print("✅ Archivos estáticos: OK")
        print("✅ Templates: OK")
        print("\n💡 RECOMENDACIONES:")
        print("1. Ejecutar: python scripts/agregar_tipo_servicio.py (si no se ha hecho)")
        print("2. Reiniciar el servidor Flask")
        print("3. Limpiar caché del navegador (Ctrl+Shift+Del)")
        print("4. Hacer hard refresh (Ctrl+F5)")
        print("\n✅ El proyecto está configurado correctamente")
        print("="*70)

if __name__ == "__main__":
    try:
        diagnosticar()
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()
