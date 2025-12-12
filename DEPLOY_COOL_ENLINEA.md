# 🚀 Instrucciones de Despliegue en cool.enlinea.sbs

## Resumen de lo que tienes

Tu proyecto BoodFood está dividido en **dos partes independientes**:

1. **Frontend** (Flask + SocketIO): Interfaz web para clientes, personal de cocina, caja
   - Puerto: `8000`
   - Archivo de inicio: `run_frontend.py`
   
2. **API REST** (FastAPI): API para integrar con terceros o aplicaciones móviles
   - Puerto: `3311`
   - Archivo de inicio: `fastapi_app/asgi.py` (via Uvicorn)

3. **Base de Datos** (MySQL): Almacena toda la información
   - Puerto: `3306`

---

## Opción Más Fácil: Usar Git + Panel de cool.enlinea.sbs

### Si cool.enlinea.sbs soporta despliegue por Git:

1. **Sube el proyecto a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "BoodFood - Frontend y API"
   git remote add origin https://github.com/TU_USUARIO/boodfood-fastapi.git
   git push -u origin main
   ```

2. **En el panel de cool.enlinea.sbs:**
   - Selecciona "Importar desde Git"
   - Pega la URL: `https://github.com/TU_USUARIO/boodfood-fastapi.git`
   - Selecciona rama: `main`
   - Tipo de aplicación: **Python**
   - Comando de inicio (Frontend):
     ```
     python run_frontend.py
     ```
   - Puertos expuestos: `8000`
   
3. **Para la API, repite el proceso:**
   - Mismo repositorio
   - Comando de inicio (API):
     ```
     python -m uvicorn fastapi_app.asgi:app --host 0.0.0.0 --port 3311
     ```
   - Puertos expuestos: `3311`

---

## Opción Manual: Clonar y Ejecutar

Si el panel no soporta Git automáticamente:

### En la terminal del servidor cool.enlinea.sbs:

```bash
# 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/boodfood-fastapi.git
cd boodfood-fastapi

# 2. Ejecutar script de despliegue
bash deploy.sh production

# 3. Crear .env con credenciales reales
nano .env
# Edita DATABASE_URL con tus credenciales MySQL

# 4. En terminal 1 - Ejecutar Frontend
source venv/bin/activate
python run_frontend.py

# 5. En terminal 2 - Ejecutar API
source venv/bin/activate
python -m uvicorn fastapi_app.asgi:app --host 0.0.0.0 --port 3311 --workers 4

# 6. En terminal 3 - Usar Supervisor para mantener servicios activos
sudo supervisorctl status
```

---

## Archivos Clave Incluidos

| Archivo | Descripción |
|---------|------------|
| `run_frontend.py` | Inicia Flask + SocketIO en puerto 8000 |
| `fastapi_app/asgi.py` | Punto de entrada para Uvicorn (API) |
| `requirements.txt` | Todas las dependencias Python |
| `.env.example` | Plantilla de variables de entorno |
| `deploy.sh` | Script automático de despliegue (Linux) |
| `deploy.bat` | Script automático de despliegue (Windows) |
| `docker-compose.split.yml` | Para despliegue con Docker (opcional) |
| `Dockerfile.frontend` | Para containerizar solo el frontend |
| `Dockerfile` | Para containerizar solo la API |
| `README_DEPLOYMENT.md` | Guía completa de despliegue |

---

## Checklist Pre-Despliegue

- [ ] Código subido a GitHub/GitLab
- [ ] `.env` configurado con credenciales reales de MySQL
- [ ] Base de datos MySQL creada y accesible
- [ ] Puerto 8000 disponible (Frontend)
- [ ] Puerto 3311 disponible (API)
- [ ] Python 3.11+ instalado en el servidor
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] Logs configurados y monitoreados

---

## URLs Post-Despliegue

Reemplaza `tu-dominio.com` con tu dominio real en cool.enlinea.sbs:

- **Frontend**: https://tu-dominio.com:8000 (o sin puerto si está detrás de Nginx)
- **API**: https://tu-dominio.com:3311/api (o `/api` si Nginx redirige)
- **Swagger**: https://tu-dominio.com:3311/api/docs

---

## Configurar Nginx como Reverse Proxy (Opcional)

Si cool.enlinea.sbs usa Nginx, configura esto en `/etc/nginx/sites-available/boodfood`:

```nginx
upstream frontend {
    server 127.0.0.1:8000;
}

upstream api {
    server 127.0.0.1:3311;
}

server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # API
    location /api {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Luego actívalo:
```bash
sudo ln -s /etc/nginx/sites-available/boodfood /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Asegúrate de activar el venv e instalar dependencias
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Connection refused" a la base de datos
```bash
# Verifica que MySQL esté corriendo
mysql -u boodfood -p boodfood123 -h localhost boodfood

# Si está en otro servidor, actualiza .env:
# DATABASE_URL=mysql+pymysql://boodfood:boodfood123@IP_MySQL:3306/boodfood
```

### Los servicios se cierran inesperadamente
```bash
# Usa Supervisor o Systemd para mantenerlos activos (ver README_DEPLOYMENT.md)
# O ejecuta en tmux/screen:
tmux new -d -s frontend "python run_frontend.py"
tmux new -d -s api "python -m uvicorn fastapi_app.asgi:app --port 3311"
```

---

## Soporte y Documentación

- Ver `README_DEPLOYMENT.md` para opciones avanzadas
- Ver `README.md` para información general del proyecto
- Logs: `/var/log/boodfood-*.log` (si usas Supervisor)

¡Listo para desplegar! 🚀
