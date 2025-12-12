"""
Prueba automática: login -> crear mesa vía API -> verificar en BD
Usage: python create_and_verify_mesa.py
"""
import requests
import json
import time
from app import create_app

BASE = "http://127.0.0.1:8002/api/v1"

email = "admin1@gmail.com"
password = "3144210095"

def main():
    print("[1] Login...")
    r = requests.post(f"{BASE}/auth/login", json={"email": email, "password": password})
    print(f"Login status: {r.status_code}")
    try:
        print("Login response:", r.json())
    except Exception:
        print("Login response text:", r.text)
    if r.status_code != 200:
        print("Login failed, aborting.")
        return 1

    token = r.json().get("access_token")
    if not token:
        print("No token returned by login.")
        return 1

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Use a unique numero to avoid collisions
    numero = int(time.time() % 1000000)
    payload = {
        "numero": numero,
        "capacidad": 4,
        "tipo": "interior"
    }

    print("[2] Creating mesa via API with payload:", payload)
    r2 = requests.post(f"{BASE}/mesas", json=payload, headers=headers)
    print(f"Create status: {r2.status_code}")
    try:
        print("Create response:", r2.json())
    except Exception:
        print("Create response text:", r2.text)

    # Now verify in DB using Flask app context
    print("[3] Verifying in DB...")
    flask_app = create_app('development')
    with flask_app.app_context():
        from models import Mesa, db
        found = db.session.query(Mesa).filter_by(numero=numero).first()
        if found:
            print("✅ Mesa encontrada en BD:")
            print({
                "id": found.id,
                "numero": found.numero,
                "capacidad": found.capacidad,
                "tipo": found.tipo,
                "disponible": bool(found.disponible)
            })
            return 0
        else:
            print("❌ Mesa no encontrada en BD. Lista de mesas con ese número (consulta directa):")
            rows = db.session.query(Mesa).filter_by(numero=numero).all()
            print(rows)
            return 2

if __name__ == '__main__':
    exit(main())
