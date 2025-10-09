-- Script para agregar columnas faltantes a la base de datos existente
USE f58_brandon;

-- Intentar agregar columnas (ignorar si ya existen)
ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE;
ALTER TABLE usuarios ADD COLUMN fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
