"""
Script para generar el hash correcto de la contraseña del admin
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
        print("ACTUALIZANDO CONTRASEÑA DEL ADMIN")
        print("=" * 60)
        
        # Generar nuevo hash para la contraseña correcta
        contraseña = "3144210095"
        hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
        nuevo_hash = hashed_password.decode('utf-8')
        
        print(f"Contraseña: {contraseña}")
        print(f"Hash generado: {nuevo_hash}")
        
        # Actualizar en la BD
        usuario.password_hash = nuevo_hash
        db.session.commit()
        
        print("=" * 60)
        print("HASH ACTUALIZADO CORRECTAMENTE EN LA BD")
        print("=" * 60)
        
        # Verificar que el nuevo hash funciona
        password_hash_bytes = nuevo_hash.encode('utf-8')
        resultado = bcrypt.checkpw(contraseña.encode('utf-8'), password_hash_bytes)
        print(f"Verificacion del nuevo hash: {resultado}")
        print("=" * 60)
    else:
        print("Usuario admin1@gmail.com no encontrado")
