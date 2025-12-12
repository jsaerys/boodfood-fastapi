# ✅ Checklist Pre-Despliegue - BoodFood

## Verificación Técnica

- [x] Python 3.8+ instalado
- [x] Git configurado con GitHub
- [x] Estructura de carpetas reorganizada
- [x] Todos los imports corregidos (Flask y FastAPI)
- [x] Base de datos MySQL conectada (mysql.enlinea.sbs:3311)
- [x] Flask arranca sin errores en puerto 5001
- [x] FastAPI arranca sin errores en puerto 3311
- [x] SQLAlchemy conecta y mapea todas las tablas
- [x] Requirements.txt actualizado con todas las dependencias

## Configuración

- [x] config.py configurada con credenciales correctas
- [x] .env.example creado
- [x] Variables de entorno definidas
- [x] Rutas de archivos estáticas correctas
- [x] Carpeta de uploads configurada

## Documentación

- [x] DEPLOYMENT_GUIDE.md creado (instrucciones detalladas)
- [x] README_PRODUCTION.md creado (guía rápida)
- [x] Script deploy.sh creado
- [x] Comentarios en código donde sea necesario

## Seguridad

- [x] SECRET_KEY configurada
- [x] JWT_SECRET_KEY configurada
- [x] Credenciales de BD no en código (en config.py con variables de entorno)
- [x] Debug deshabilitado en producción
- [x] CORS configurado
- [x] Validación de input con Pydantic

## Testing Pre-Despliegue

```bash
# ✅ Todos estos comandos pasaron:
python -m uvicorn asgi:app --host 0.0.0.0 --port 3311
# Resultado: FastAPI running on http://0.0.0.0:3311 ✅

python wsgi.py
# Resultado: Flask running on http://localhost:5001 ✅

python -c "from src.app.app import create_app; print('Flask imports OK')"
# Resultado: Flask imports OK ✅

python -c "from src.fastapi_app import create_fastapi_app; print('FastAPI imports OK')"
# Resultado: FastAPI imports OK ✅
```

## Despliegue - Opciones

### Opción A: cool.enlinea.sbs (Recomendado)
1. [ ] Acceder a panel de cool.enlinea.sbs
2. [ ] Crear aplicación Node.js o Custom
3. [ ] Conectar repositorio GitHub: jsaerys/boodfood-fastapi
4. [ ] Configurar variables de entorno (copiar de .env)
5. [ ] Configurar comando de inicio:
   - Flask: `python wsgi.py`
   - FastAPI: `python -m uvicorn asgi:app --host 0.0.0.0 --port 3311`
6. [ ] Desplegar

### Opción B: VPS/Servidor Propio
1. [ ] SSH al servidor
2. [ ] Clonar repo: `git clone https://github.com/jsaerys/boodfood-fastapi.git`
3. [ ] Ejecutar: `chmod +x deploy.sh && ./deploy.sh`
4. [ ] Configurar Supervisor (ver DEPLOYMENT_GUIDE.md)
5. [ ] Configurar Nginx reverso proxy
6. [ ] Obtener certificado SSL (Let's Encrypt)
7. [ ] Iniciar servicios

## URLs de Acceso

Después del despliegue, accesible en:

```
Frontend:      https://tu-dominio.com
API Docs:      https://tu-dominio.com/docs
API Base:      https://tu-dominio.com/api/
Admin Panel:   https://tu-dominio.com/admin
Swagger UI:    https://tu-dominio.com/api/swagger
```

## Monitoreo Post-Despliegue

- [ ] Verificar que frontend carga correctamente
- [ ] Verificar que /docs muestra la documentación de FastAPI
- [ ] Probar login con credenciales de prueba
- [ ] Crear un pedido de prueba
- [ ] Revisar logs de errores
- [ ] Verificar que WebSockets funcionan (Flask-SocketIO)
- [ ] Probar endpoints de API con curl:
  ```bash
  curl https://tu-dominio.com/api/menu
  curl -X POST https://tu-dominio.com/api/auth/login -H "Content-Type: application/json" -d '{"email":"test@test.com","password":"test"}'
  ```

## Troubleshooting Rápido

**Error de conexión a BD:**
- Verificar credentials en config.py
- Verificar que mysql.enlinea.sbs:3311 es accesible
- Comprobar usuario/password de Brandon

**Puerto en uso:**
- Cambiar puerto en wsgi.py o asgi.py
- O matar proceso: `lsof -i :5001` y `kill -9 <PID>`

**Imports fallan:**
- Verificar que .venv está activado
- Ejecutar: `pip install -r requirements.txt`
- Verificar que src/__init__.py existe

**Logs para debugging:**
- Flask: `tail -f logs/flask.log`
- FastAPI: `tail -f logs/fastapi.log`

---

## Final Checklist

- [x] Código compilable sin errores
- [x] Base de datos conecta
- [x] Ambos servicios (Flask + FastAPI) funcionan localmente
- [x] GitHub actualizado
- [x] Documentación completa
- [x] Variables sensibles en .env (no en código)
- [x] Ready for production ✅

**Status**: ✅ LISTO PARA DESPLEGAR

---

**Fecha**: Diciembre 12, 2025  
**Rama**: main  
**Commit**: fa2d5d1 (Fix: Correct all import paths for reorganized project structure)
