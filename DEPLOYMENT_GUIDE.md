# Guía de Despliegue - BoodFood en cool.enlinea.sbs

## Requisitos Previos
- Acceso a panel de cool.enlinea.sbs
- Git instalado en el servidor
- Python 3.8+ configurado
- MySQL conectado a `mysql.enlinea.sbs:3311` (ya funcionando)

---

## Paso 1: Clonar el Repositorio

```bash
cd /home/usuario/public_html/  # O donde desees instalar
git clone https://github.com/jsaerys/boodfood-fastapi.git
cd boodfood-fastapi
```

---

## Paso 2: Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

---

## Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

---

## Paso 4: Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```bash
# .env para PRODUCCIÓN en cool.enlinea.sbs
FLASK_ENV=production
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-segura-2025

# Base de datos (ya configurada)
DATABASE_URL=mysql+pymysql://brandon:brandonc@mysql.enlinea.sbs:3311/f58_brandon

# JWT
JWT_SECRET_KEY=tu-jwt-secret-key-muy-seguro

# Puertos (a verificar con hosting)
FLASK_PORT=5001
FASTAPI_PORT=3311
```

---

## Paso 5: Desplegar Flask (Frontend)

**Opción A: Con Gunicorn (RECOMENDADO)**

```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5001 wsgi:app
```

**Opción B: Con SocketIO directamente**
```bash
python wsgi.py
```

---

## Paso 6: Desplegar FastAPI (API REST)

**Opción A: Con Uvicorn + Gunicorn**
```bash
pip install uvicorn
gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker asgi:app --bind 0.0.0.0:3311
```

**Opción B: Uvicorn directo**
```bash
python -m uvicorn asgi:app --host 0.0.0.0 --port 3311 --workers 4
```

---

## Paso 7: Configurar Supervisor (Para Mantener Servicios Activos)

Instalar Supervisor:
```bash
sudo apt-get install supervisor
```

Crear archivo `/etc/supervisor/conf.d/boodfood.conf`:

```ini
[program:boodfood-flask]
directory=/home/usuario/public_html/boodfood-fastapi
command=/home/usuario/public_html/boodfood-fastapi/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5001 wsgi:app
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/usuario/public_html/boodfood-fastapi/logs/flask.log

[program:boodfood-fastapi]
directory=/home/usuario/public_html/boodfood-fastapi
command=/home/usuario/public_html/boodfood-fastapi/venv/bin/uvicorn asgi:app --host 127.0.0.1 --port 3311 --workers 4
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/usuario/public_html/boodfood-fastapi/logs/fastapi.log
```

Luego:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start boodfood-flask boodfood-fastapi
```

---

## Paso 8: Configurar Nginx (Proxy Reverso)

Crear archivo `/etc/nginx/sites-available/boodfood`:

```nginx
upstream flask_app {
    server 127.0.0.1:5001;
}

upstream fastapi_app {
    server 127.0.0.1:3311;
}

server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend Flask
    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API FastAPI
    location /api/ {
        proxy_pass http://fastapi_app/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Docs de FastAPI
    location /docs {
        proxy_pass http://fastapi_app/docs;
        proxy_set_header Host $host;
    }
}
```

Activar:
```bash
sudo ln -s /etc/nginx/sites-available/boodfood /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Verificación Post-Despliegue

```bash
# Flask está funcionando
curl http://localhost:5001

# FastAPI está funcionando
curl http://localhost:3311/docs

# Base de datos conecta
mysql -h mysql.enlinea.sbs -P 3311 -u brandon -p -D f58_brandon -e "SELECT VERSION();"
```

---

## Estructura de Carpetas en Producción

```
/home/usuario/public_html/boodfood-fastapi/
├── src/
│   ├── app/           # Flask Frontend
│   └── fastapi_app/   # FastAPI REST API
├── config/            # Configuración
├── deployment/        # Scripts de despliegue
├── static/            # Assets
├── templates/         # Plantillas HTML
├── logs/              # Archivos de log
├── wsgi.py           # Entry point Flask
├── asgi.py           # Entry point FastAPI
├── requirements.txt
├── .env              # VARIABLES PRIVADAS (no commitear)
└── venv/             # Virtual environment
```

---

## URLs de Acceso en Producción

- **Frontend**: `https://tu-dominio.com`
- **API Docs**: `https://tu-dominio.com/docs`
- **API Base**: `https://tu-dominio.com/api/`

---

## Troubleshooting

### Puerto 5000/5001 en uso
```bash
lsof -i :5001
kill -9 <PID>
```

### Permisos de carpeta
```bash
chmod -R 755 /home/usuario/public_html/boodfood-fastapi
chmod -R 777 /home/usuario/public_html/boodfood-fastapi/static/uploads
chmod -R 777 /home/usuario/public_html/boodfood-fastapi/logs
```

### Ver logs
```bash
tail -f logs/flask.log
tail -f logs/fastapi.log
```

---

**¡Listo! Tu aplicación está lista para producción.** 🚀
