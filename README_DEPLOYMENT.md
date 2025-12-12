# 🚀 Guía de Despliegue - BoodFood (Sin Docker)

## Opción 1: Despliegue en Servidor Linux/VPS (Recomendado para cool.enlinea.sbs)

### Requisitos
- Python 3.11+
- MySQL 8.0+
- Git
- Supervisor o Systemd (para mantener servicios corriendo)

### Pasos

#### 1. Clonar el repositorio
```bash
git clone <tu_repo_url>
cd boodfood-fastapi-main
```

#### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\Activate.ps1
```

#### 3. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Edita .env con tus credenciales de base de datos y secretos
nano .env  # O usa tu editor favorito
```

#### 5. Crear/Inicializar base de datos
```bash
python scripts/init_db.py
```

#### 6. Ejecutar migraciones (si aplica)
```bash
python scripts/init_db.py  # Crea tablas automáticamente
```

---

## Opción 2: Despliegue Local en Windows (Desarrollo/Pruebas)

### Requisitos
- Python 3.11+
- MySQL Community Server (o usar Docker solo para DB)
- Git

### Pasos

#### 1. Clonar repositorio
```powershell
git clone <tu_repo_url>
cd boodfood-fastapi-main
```

#### 2. Crear entorno virtual
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 3. Instalar dependencias
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno
```powershell
Copy-Item .env.example .env
# Edita .env con tus credenciales
```

#### 5. Inicializar base de datos
```powershell
python scripts/init_db.py
```

#### 6. Ejecutar Frontend y API (dos terminales)

**Terminal 1 - Frontend (Flask + SocketIO):**
```powershell
python run_frontend.py
```
Accede en: http://localhost:8000

**Terminal 2 - API (FastAPI):**
```powershell
python -m uvicorn fastapi_app.asgi:app --host 0.0.0.0 --port 3311 --reload
```
Accede en: http://localhost:3311/api

---

## Opción 3: Despliegue en Servidor con Supervisor (Recomendado para Producción)

### Crear archivos de configuración Supervisor

#### `/etc/supervisor/conf.d/boodfood-frontend.conf`
```ini
[program:boodfood-frontend]
directory=/home/app/boodfood-fastapi-main
command=/home/app/boodfood-fastapi-main/venv/bin/python run_frontend.py
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/boodfood-frontend.log
environment=PATH="/home/app/boodfood-fastapi-main/venv/bin",FLASK_ENV="production"
```

#### `/etc/supervisor/conf.d/boodfood-api.conf`
```ini
[program:boodfood-api]
directory=/home/app/boodfood-fastapi-main
command=/home/app/boodfood-fastapi-main/venv/bin/uvicorn fastapi_app.asgi:app --host 0.0.0.0 --port 3311 --workers 4
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/boodfood-api.log
environment=PATH="/home/app/boodfood-fastapi-main/venv/bin",DATABASE_URL="mysql+pymysql://..."
```

#### Comandos Supervisor
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start boodfood-frontend boodfood-api
sudo supervisorctl status
```

---

## Opción 4: Despliegue con Systemd (Alternativa a Supervisor)

#### `/etc/systemd/system/boodfood-frontend.service`
```ini
[Unit]
Description=BoodFood Frontend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/app/boodfood-fastapi-main
ExecStart=/home/app/boodfood-fastapi-main/venv/bin/python run_frontend.py
Restart=always
Environment="FLASK_ENV=production"

[Install]
WantedBy=multi-user.target
```

#### `/etc/systemd/system/boodfood-api.service`
```ini
[Unit]
Description=BoodFood API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/app/boodfood-fastapi-main
ExecStart=/home/app/boodfood-fastapi-main/venv/bin/uvicorn fastapi_app.asgi:app --host 0.0.0.0 --port 3311 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Activar servicios
```bash
sudo systemctl daemon-reload
sudo systemctl enable boodfood-frontend boodfood-api
sudo systemctl start boodfood-frontend boodfood-api
sudo systemctl status boodfood-frontend boodfood-api
```

---

## Configurar Nginx como Proxy Reverso (Producción)

```nginx
server {
    listen 80;
    server_name tudominio.com;

    # Frontend (Flask)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # API (FastAPI)
    location /api {
        proxy_pass http://127.0.0.1:3311;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Verificación Post-Despliegue

```bash
# Ver logs del frontend
tail -f /var/log/boodfood-frontend.log

# Ver logs de la API
tail -f /var/log/boodfood-api.log

# Verificar que los servicios están corriendo
curl http://localhost:8000      # Frontend
curl http://localhost:3311/api  # API
```

---

## Troubleshooting

### Error: ModuleNotFoundError
```bash
# Asegúrate de activar el venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\Activate.ps1  # Windows

# Reinstala dependencias
pip install -r requirements.txt
```

### Error: MySQL connection refused
```bash
# Verifica que MySQL esté corriendo
sudo systemctl status mysql

# O en Windows
# Abre Services y busca MySQL, reinicia el servicio
```

### Error: Puerto ya en uso
```bash
# Linux: ver qué proceso ocupa el puerto
lsof -i :8000
lsof -i :3311

# Windows PowerShell
Get-NetTCPConnection -LocalPort 8000
```

---

## Variables de Entorno Obligatorias

- `DATABASE_URL`: URL de conexión MySQL (format: `mysql+pymysql://user:pass@host:port/dbname`)
- `FLASK_ENV`: `production` o `development`
- `DEBUG`: `False` en producción
- `SECRET_KEY`: Clave secreta para sesiones Flask (mínimo 32 caracteres)
- `JWT_SECRET`: Secreto JWT para autenticación API

---

¡Listo! Tu aplicación debería estar corriendo. 🚀
