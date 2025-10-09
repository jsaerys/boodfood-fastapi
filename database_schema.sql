-- Base de Datos BoodFood
-- Base de datos: f58_brandon

USE f58_brandon;

-- Tabla de usuarios (clientes y personal)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    rol ENUM('cliente', 'mesero', 'cocinero', 'cajero', 'admin') DEFAULT 'cliente',
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de mesas
CREATE TABLE IF NOT EXISTS mesas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT UNIQUE NOT NULL,
    capacidad INT NOT NULL,
    ubicacion VARCHAR(50),
    disponible BOOLEAN DEFAULT TRUE,
    tipo ENUM('interior', 'terraza', 'vip') DEFAULT 'interior'
);

-- Tabla de meseros
CREATE TABLE IF NOT EXISTS meseros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    nombre VARCHAR(100) NOT NULL,
    foto VARCHAR(255),
    especialidad VARCHAR(100),
    disponible BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- Tabla de categorías del menú
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    orden INT DEFAULT 0
);

-- Tabla de items del menú
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    categoria_id INT,
    imagen VARCHAR(255),
    disponible BOOLEAN DEFAULT TRUE,
    tipo ENUM('comida', 'bebida', 'postre', 'entrada') NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);

-- Tabla de servicios adicionales
CREATE TABLE IF NOT EXISTS servicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    tipo ENUM('piscina', 'billar', 'evento', 'otro') NOT NULL,
    capacidad INT,
    disponible BOOLEAN DEFAULT TRUE
);

-- Tabla de reservas
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    mesa_id INT,
    mesero_id INT,
    servicio_id INT,
    fecha_reserva DATETIME NOT NULL,
    num_personas INT NOT NULL,
    estado ENUM('pendiente', 'confirmada', 'cancelada', 'completada') DEFAULT 'pendiente',
    notas TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (mesa_id) REFERENCES mesas(id) ON DELETE SET NULL,
    FOREIGN KEY (mesero_id) REFERENCES meseros(id) ON DELETE SET NULL,
    FOREIGN KEY (servicio_id) REFERENCES servicios(id) ON DELETE SET NULL
);

-- Tabla de pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    mesa_id INT,
    tipo ENUM('mesa', 'piscina', 'domicilio') NOT NULL,
    estado ENUM('pendiente', 'preparando', 'listo', 'entregado', 'cancelado') DEFAULT 'pendiente',
    total DECIMAL(10, 2) DEFAULT 0.00,
    direccion_domicilio TEXT,
    notas TEXT,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (mesa_id) REFERENCES mesas(id) ON DELETE SET NULL
);

-- Tabla de items de pedidos
CREATE TABLE IF NOT EXISTS pedido_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    notas TEXT,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
);

-- Tabla de facturas
CREATE TABLE IF NOT EXISTS facturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    mesa_id INT,
    usuario_id INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    estado ENUM('pendiente', 'pagada', 'cancelada') DEFAULT 'pendiente',
    metodo_pago VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_pago TIMESTAMP NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (mesa_id) REFERENCES mesas(id) ON DELETE SET NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de inventario
CREATE TABLE IF NOT EXISTS inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    cantidad DECIMAL(10, 2) NOT NULL,
    unidad VARCHAR(20) NOT NULL,
    precio_unitario DECIMAL(10, 2),
    stock_minimo DECIMAL(10, 2) DEFAULT 0,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de movimientos de inventario
CREATE TABLE IF NOT EXISTS inventario_movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inventario_id INT NOT NULL,
    tipo ENUM('entrada', 'salida') NOT NULL,
    cantidad DECIMAL(10, 2) NOT NULL,
    usuario_id INT,
    notas TEXT,
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (inventario_id) REFERENCES inventario(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- Insertar categorías por defecto
INSERT INTO categorias (nombre, descripcion, orden) VALUES
('Entradas', 'Aperitivos y entradas', 1),
('Platos Principales', 'Platos fuertes', 2),
('Bebidas', 'Bebidas frías y calientes', 3),
('Postres', 'Dulces y postres', 4),
('Cócteles', 'Bebidas alcohólicas', 5);

-- Insertar mesas de ejemplo
INSERT INTO mesas (numero, capacidad, ubicacion, tipo) VALUES
(1, 4, 'Interior', 'interior'),
(2, 4, 'Interior', 'interior'),
(3, 2, 'Interior', 'interior'),
(4, 6, 'Terraza', 'terraza'),
(5, 8, 'Terraza', 'vip'),
(6, 4, 'Terraza', 'terraza');

-- Insertar servicios de ejemplo
INSERT INTO servicios (nombre, descripcion, precio, tipo, capacidad) VALUES
('Entrada Piscina', 'Acceso a la piscina por día', 15000.00, 'piscina', 50),
('Mesa de Billar', 'Alquiler de mesa de billar por hora', 10000.00, 'billar', 4),
('Salón de Eventos', 'Alquiler de salón para eventos privados', 500000.00, 'evento', 100);

-- El usuario administrador se creará mediante el script init_db.py
