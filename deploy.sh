#!/bin/bash
# Script de despliegue automático para BoodFood
# Uso: ./deploy.sh <entorno>
# Ejemplo: ./deploy.sh production

set -e

ENVIRONMENT=${1:-production}
APP_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
VENV_DIR="$APP_DIR/venv"

echo "=========================================="
echo "🚀 Despliegue de BoodFood - Entorno: $ENVIRONMENT"
echo "=========================================="

# 1. Crear venv si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv "$VENV_DIR"
fi

# 2. Activar venv
echo "✅ Activando entorno virtual..."
source "$VENV_DIR/bin/activate"

# 3. Actualizar pip
echo "📥 Actualizando pip..."
pip install --upgrade pip

# 4. Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# 5. Crear .env si no existe
if [ ! -f "$APP_DIR/.env" ]; then
    echo "⚙️  Creando archivo .env..."
    cp "$APP_DIR/.env.example" "$APP_DIR/.env"
    echo "⚠️  IMPORTANTE: Edita .env con tus credenciales reales"
    echo "⚠️  nano $APP_DIR/.env"
fi

# 6. Cargar variables de entorno
set -a
source "$APP_DIR/.env"
set +a

# 7. Inicializar base de datos
echo "🗄️  Inicializando base de datos..."
python "$APP_DIR/scripts/init_db.py" || echo "⚠️  init_db.py no encontrado, saltando..."

# 8. Mostrar status
echo ""
echo "=========================================="
echo "✅ Despliegue completado exitosamente"
echo "=========================================="
echo ""
echo "📝 Próximos pasos:"
echo ""
echo "1️⃣  Edita las credenciales en: .env"
echo "2️⃣  Inicia el frontend (Terminal 1):"
echo "   source $VENV_DIR/bin/activate"
echo "   python run_frontend.py"
echo ""
echo "3️⃣  Inicia la API (Terminal 2):"
echo "   source $VENV_DIR/bin/activate"
echo "   python -m uvicorn fastapi_app.asgi:app --host 0.0.0.0 --port 3311"
echo ""
echo "📍 URLs locales:"
echo "   Frontend: http://localhost:8000"
echo "   API:      http://localhost:3311/api"
echo "   Swagger:  http://localhost:3311/api/docs"
echo ""
