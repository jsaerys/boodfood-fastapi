# 📤 Pasos para Subir a GitHub y Desplegar

## Paso 1: Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `boodfood-fastapi`
3. Descripción: "Sistema de gestión de restaurante con FastAPI y Flask"
4. Elige "Public" o "Private" según prefieras
5. NO inicialices con README (ya lo tenemos)
6. Haz clic en "Create repository"

---

## Paso 2: Configurar Git localmente en PowerShell

```powershell
# Abre PowerShell en la carpeta del proyecto
cd C:\Users\CGAO\Desktop\boodfood-fastapi-main

# Configurar Git con tu usuario (primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@gmail.com"

# Inicializar repositorio (si no está)
git init

# Añadir todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit: BoodFood Frontend (Flask) y API (FastAPI)"

# Cambiar rama principal a 'main' (si está en master)
git branch -M main

# Añadir el origin remoto (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/boodfood-fastapi.git

# Hacer push (te pedirá contraseña o token)
git push -u origin main
```

---

## Paso 3: Autenticación en GitHub desde PowerShell

GitHub requiere **Personal Access Token** (no contraseña):

1. Ve a https://github.com/settings/tokens/new
2. Dale un nombre: `boodfood-deploy`
3. Selecciona permisos: `repo` (acceso completo a repos)
4. Haz clic en "Generate token"
5. **Copia el token** (no lo verás de nuevo)

### Usar el token en PowerShell:

```powershell
# Cuando Git te pida la contraseña, usa el token:
git push -u origin main
# Username: TU_USUARIO
# Password: tu_token_aqui (pega el que acabas de copiar)
```

---

## Paso 4: Configurar credenciales de Git para que no pida de nuevo

```powershell
# Opción A: Almacenar credenciales en Windows (recomendado)
git config --global credential.helper wincred

# Ahora Git recordará tu token

# Opción B: Si usas SSH (más seguro, pero más config)
# Genera clave SSH y configúrala en GitHub Settings > SSH keys
```

---

## Paso 5: Verificar que el push fue exitoso

1. Ve a https://github.com/TU_USUARIO/boodfood-fastapi
2. Deberías ver todos tus archivos

---

## Paso 6: Conectar en cool.enlinea.sbs

### Opción A: Si cool.enlinea.sbs tiene "Import from Git"

1. En el panel de cool.enlinea.sbs, busca "Import from Git" o "Deploy from Repository"
2. Pega: `https://github.com/TU_USUARIO/boodfood-fastapi.git`
3. Selecciona rama: `main`
4. Crea **dos aplicaciones:**

#### Aplicación 1: Frontend
- Nombre: `boodfood-frontend`
- Comando: `python run_frontend.py`
- Puerto: `8000`
- Variables de entorno: (cargar del `.env`)

#### Aplicación 2: API
- Nombre: `boodfood-api`
- Comando: `python -m uvicorn fastapi_app.asgi:app --host 0.0.0.0 --port 3311 --workers 4`
- Puerto: `3311`
- Variables de entorno: (cargar del `.env`)

---

### Opción B: Si cool.enlinea.sbs NO tiene Import from Git (despliegue manual)

1. En el panel, busca "SSH Terminal" o "File Manager"
2. Ejecuta estos comandos:

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/boodfood-fastapi.git
cd boodfood-fastapi

# 2. Ejecutar script de despliegue
bash deploy.sh production

# 3. Crear archivo .env con credenciales
nano .env
# Edita DATABASE_URL y credenciales

# 4. Ejecutar los servicios (ver instrucciones en DEPLOY_COOL_ENLINEA.md)
```

---

## Paso 7: Verificar que todo funciona

### En cool.enlinea.sbs:

```bash
# Frontend
curl http://tu-dominio.com:8000

# API
curl http://tu-dominio.com:3311/api

# Swagger (documentación)
curl http://tu-dominio.com:3311/api/docs
```

---

## Próximos pushes (actualizaciones)

Si haces cambios locales y quieres actualizar el servidor:

```powershell
# Desde tu carpeta local
git add .
git commit -m "Descripción del cambio"
git push origin main

# En el servidor cool.enlinea.sbs (si está configurado con CI/CD)
# La app se redesplegará automáticamente
# Si no, entra en SSH y ejecuta:
# git pull origin main
# systemctl restart boodfood-frontend boodfood-api
```

---

## Resumen de lo que subiste

| Carpeta/Archivo | Contenido |
|-----------------|-----------|
| `fastapi_app/` | API REST (FastAPI) |
| `routes/` | Rutas Flask (Frontend) |
| `templates/` | HTML del frontend |
| `static/` | CSS, JS, uploads |
| `scripts/` | Utilidades (init_db.py, etc.) |
| `run_frontend.py` | ✨ Inicia Flask en puerto 8000 |
| `fastapi_app/asgi.py` | ✨ Punto entrada API (Uvicorn) |
| `requirements.txt` | Todas las dependencias |
| `docker-compose.split.yml` | Despliegue con Docker (opcional) |
| `.env.example` | Plantilla de variables |
| `deploy.sh` / `deploy.bat` | Scripts automáticos |
| `README_DEPLOYMENT.md` | Guía completa |
| `DEPLOY_COOL_ENLINEA.md` | Guía específica para tu hosting |

---

## ¿Necesitas ayuda?

- ¿Error de autenticación?: Regenera el token en https://github.com/settings/tokens
- ¿Puerto 8000/3311 ocupado?: Cambia los puertos en `run_frontend.py` y `docker-compose.split.yml`
- ¿Base de datos no conecta?: Verifica credenciales en `.env` y que MySQL esté corriendo

¡Listo para desplegar! 🚀
