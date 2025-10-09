-- Modificar la columna rol para incluir los nuevos roles
USE f58_brandon;

ALTER TABLE usuarios MODIFY COLUMN rol ENUM('usuario', 'administrador', 'restaurante', 'cliente', 'mesero', 'cocinero', 'cajero', 'admin') DEFAULT 'cliente';
