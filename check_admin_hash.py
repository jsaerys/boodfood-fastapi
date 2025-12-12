"""
Script para verificar el hash del admin en la BD
"""
import bcrypt
from app import create_app
from models import Usuario

# Crear instancia de Flask app
flask_app = create_app('development')

# Usar el contexto de la aplicación para acceder a db
with flask_app.app_context():
    from fastapi_app.models import db
    
    # Buscar el usuario admin
    usuario = db.session.query(Usuario).filter_by(email='admin1@gmail.com').first()
    
    if usuario:
        print("=" * 60)
        print("USUARIO ENCONTRADO")
        print("=" * 60)
        print(f"ID: {usuario.id}")
        print(f"Nombre: {usuario.nombre} {usuario.apellido}")
        print(f"Email: {usuario.email}")
        print(f"Activo: {usuario.activo}")
        print(f"Rol: {usuario.rol}")
        print(f"Hash actual: {usuario.password_hash}")
        print("=" * 60)
        
        # Probar si el hash es válido con la contraseña
        contraseña_test = "3144210095"
        password_hash_bytes = usuario.password_hash
        if isinstance(password_hash_bytes, str):
            password_hash_bytes = password_hash_bytes.encode('utf-8')
        
        try:
            resultado = bcrypt.checkpw(contraseña_test.encode('utf-8'), password_hash_bytes)
            print(f"Prueba de contraseña '{contraseña_test}': {resultado}")
        except ValueError as e:
            print(f"Error al verificar: {e}")
            print("El hash parece estar corrupto o no es un hash bcrypt válido")
        
        print("=" * 60)
    else:
        print("Usuario admin1@gmail.com no encontrado")
