#!/bin/bash
# Script de despliegue para BoodFood en producción
# Uso: chmod +x deploy.sh && ./deploy.sh

set -e  # Exit on error

echo "🚀 Iniciando despliegue de BoodFood..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Activar venv
echo -e "${YELLOW}1. Activando entorno virtual...${NC}"
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}❌ Entorno virtual no encontrado. Creando...${NC}"
    python3 -m venv venv
    source venv/bin/activate
fi

# 2. Instalar dependencias
echo -e "${YELLOW}2. Instalando dependencias...${NC}"
pip install -q -r requirements.txt

# 3. Verificar configuración
echo -e "${YELLOW}3. Verificando configuración...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Archivo .env no encontrado. Creando desde ejemplo...${NC}"
    cp .env.example .env
    echo -e "${RED}⚠️  IMPORTANTE: Edita .env con tus credenciales de producción${NC}"
fi

# 4. Crear carpetas necesarias
echo -e "${YELLOW}4. Creando carpetas necesarias...${NC}"
mkdir -p logs
mkdir -p static/uploads/menu
mkdir -p static/uploads/users
chmod 777 logs
chmod 777 static/uploads

# 5. Verificar conexión a BD
echo -e "${YELLOW}5. Verificando conexión a base de datos...${NC}"
python3 << 'EOF'
from config.config import Config
from src.app.models import db
try:
    # Intentar obtener una conexión
    result = db.engine.execute("SELECT 1")
    print("✅ Base de datos conectada correctamente")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    exit(1)
EOF

# 6. Verificar imports
echo -e "${YELLOW}6. Verificando que los imports funcionan...${NC}"
python3 -c "from src.app.app import create_app; from src.fastapi_app import create_fastapi_app; print('✅ Imports correctos')"

echo -e "${GREEN}✅ Despliegue completado exitosamente!${NC}"
echo ""
echo "📋 Próximos pasos:"
echo "  1. Edita .env con tus credenciales de producción"
echo "  2. Ejecuta Flask:  python wsgi.py"
echo "  3. Ejecuta FastAPI: python -m uvicorn asgi:app --host 0.0.0.0 --port 3311"
echo ""
echo "📖 Para más información, ver DEPLOYMENT_GUIDE.md"
