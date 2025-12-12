# Usar imagen oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Crear directorios necesarios
RUN mkdir -p static/uploads/menu static/uploads/users

# Exponer puerto
EXPOSE 3311

# Comando para ejecutar la aplicación FastAPI
CMD ["python", "-m", "uvicorn", "fastapi_app.asgi:app", "--host", "0.0.0.0", "--port", "3311"]
