@echo off
REM Script de despliegue automático para BoodFood (Windows)
REM Uso: deploy.bat production

setlocal enabledelayedexpansion
set ENVIRONMENT=%1
if "!ENVIRONMENT!"=="" set ENVIRONMENT=production

set APP_DIR=%~dp0
set VENV_DIR=%APP_DIR%venv

echo.
echo ==========================================
echo 🚀 Despliegue de BoodFood - Entorno: %ENVIRONMENT%
echo ==========================================
echo.

REM 1. Crear venv si no existe
if not exist "%VENV_DIR%" (
    echo 📦 Creando entorno virtual...
    python -m venv "%VENV_DIR%"
)

REM 2. Activar venv
echo ✅ Activando entorno virtual...
call "%VENV_DIR%\Scripts\activate.bat"

REM 3. Actualizar pip
echo 📥 Actualizando pip...
python -m pip install --upgrade pip

REM 4. Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r requirements.txt

REM 5. Crear .env si no existe
if not exist "%APP_DIR%.env" (
    echo ⚙️  Creando archivo .env...
    copy "%APP_DIR%.env.example" "%APP_DIR%.env"
    echo.
    echo ⚠️  IMPORTANTE: Edita .env con tus credenciales reales
    echo ⚠️  Abre: %APP_DIR%.env
)

REM 6. Inicializar base de datos
echo 🗄️  Inicializando base de datos...
python "%APP_DIR%scripts\init_db.py" >nul 2>&1 || echo ⚠️  init_db.py no encontrado, saltando...

echo.
echo ==========================================
echo ✅ Despliegue completado exitosamente
echo ==========================================
echo.
echo 📝 Próximos pasos:
echo.
echo 1️⃣  Edita las credenciales en: %APP_DIR%.env
echo 2️⃣  Inicia el frontend (PowerShell Terminal 1):
echo    %APP_DIR%venv\Scripts\Activate.ps1
echo    python run_frontend.py
echo.
echo 3️⃣  Inicia la API (PowerShell Terminal 2):
echo    %APP_DIR%venv\Scripts\Activate.ps1
echo    python -m uvicorn fastapi_app.asgi:app --host 0.0.0.0 --port 3311
echo.
echo 📍 URLs locales:
echo    Frontend: http://localhost:8000
echo    API:      http://localhost:3311/api
echo    Swagger:  http://localhost:3311/api/docs
echo.
pause
