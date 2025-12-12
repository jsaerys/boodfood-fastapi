"""
Script para reparar la contraseña del admin en la BD.
Genera un nuevo hash bcrypt válido para admin1@gmail.com.
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
        print(f"Usuario encontrado: {usuario.nombre} {usuario.apellido}")
        print(f"Hash actual: {usuario.password_hash[:50]}...")
        
        # Generar nuevo hash para la contraseña correcta
        nueva_password = "3144210095"
        hashed_password = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt())
        
        # Actualizar el hash
        usuario.password_hash = hashed_password.decode('utf-8')
        
        # Commit a la BD
        db.session.commit()
        
        print("Hash actualizado correctamente")
        print("Nuevo hash: " + usuario.password_hash[:50] + "...")
        print("Contraseña: " + nueva_password)
        print("\nYa puedes intentar login con:")
        print("   Email: admin1@gmail.com")
        print("   Contraseña: " + nueva_password)
    else:
        print("❌ Usuario admin1@gmail.com no encontrado en la BD")
