-- Creación de la base de datos
CREATE SCHEMA IF NOT EXISTS tienda_pitico DEFAULT CHARACTER SET utf8;
USE tienda_pitico;

-- Tabla Categoría
CREATE TABLE IF NOT EXISTS categoria (
  id_categoria INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  PRIMARY KEY (id_categoria)
) ENGINE = InnoDB;

-- Tabla Artículos
CREATE TABLE IF NOT EXISTS articulos (
  codigo_barras CHAR(13) NOT NULL,
  nombre VARCHAR(150) NOT NULL,
  precio FLOAT NOT NULL,
  existencia INT NOT NULL,
  unidad VARCHAR(45) NULL,
  descripcion VARCHAR(150) NULL,
  id_categoria INT NOT NULL,
  PRIMARY KEY (codigo_barras),
  INDEX categoria1_idx (id_categoria ASC) VISIBLE,
  CONSTRAINT categoria1
    FOREIGN KEY (id_categoria)
    REFERENCES categoria (id_categoria)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Tabla Clientes
CREATE TABLE IF NOT EXISTS clientes (
  telefono CHAR(10) NOT NULL,
  nombre VARCHAR(150) NOT NULL,
  apellido VARCHAR(150) NOT NULL,
  email VARCHAR(100) NULL,
  direccion VARCHAR(100) NULL,
  PRIMARY KEY (telefono)
) ENGINE = InnoDB;


-- Tabla Empleados
CREATE TABLE IF NOT EXISTS empleados (
  id_empleado INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(150) NOT NULL,
  apellido VARCHAR(45) NOT NULL,
  telefono CHAR(10) NULL,
  email VARCHAR(100) NULL,
  direccion VARCHAR(100) NULL,
  puesto VARCHAR(50) NOT NULL,
  sueldo FLOAT NOT NULL,
  estatus VARCHAR(45) NOT NULL,
  contraseña VARCHAR(80) NOT NULL,
  PRIMARY KEY (id_empleado)
) ENGINE = InnoDB;

-- Tabla Proveedor
CREATE TABLE IF NOT EXISTS proveedor (
  id_proveedor INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(80) NOT NULL,
  contacto VARCHAR(100) NOT NULL,
  telefono CHAR(10) NOT NULL,
  email VARCHAR(150) NULL,
  direccion VARCHAR(150) NULL,
  PRIMARY KEY (id_proveedor)
) ENGINE = InnoDB;

-- Tabla Ventas 
CREATE TABLE IF NOT EXISTS ventas (
  id_venta INT NOT NULL AUTO_INCREMENT,
  fecha DATETIME NULL,
  total FLOAT NOT NULL,
  id_empleado INT NOT NULL,
  telefono CHAR(10) NOT NULL,
  forma_pago VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (id_venta),
  INDEX empleados1_idx (id_empleado ASC) VISIBLE,
  INDEX clientes1_idx (telefono ASC) VISIBLE,
  CONSTRAINT empleados1
    FOREIGN KEY (id_empleado)
    REFERENCES empleados (id_empleado)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT clientes1
    FOREIGN KEY (telefono)
    REFERENCES clientes (telefono)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Tabla Detalles de Venta 
CREATE TABLE IF NOT EXISTS detalles_de_venta (
  codigo_barras CHAR(13) NOT NULL,
  id_venta INT NOT NULL,
  cantidad INT NOT NULL,
  precio_unitario FLOAT NOT NULL,
  subtotal FLOAT NOT NULL,
  PRIMARY KEY (codigo_barras, id_venta),
  INDEX fk_detalles_de_venta_ventas1_idx (id_venta ASC) VISIBLE,
  INDEX articulos1_idx (codigo_barras ASC) VISIBLE,
  CONSTRAINT fk_detalles_de_venta_ventas1
    FOREIGN KEY (id_venta)
    REFERENCES ventas (id_venta)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT articulos1
    FOREIGN KEY (codigo_barras)
    REFERENCES articulos (codigo_barras)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Tabla Compras
CREATE TABLE IF NOT EXISTS compras (
  id_compra INT NOT NULL AUTO_INCREMENT,
  fecha DATETIME NULL,
  total FLOAT NOT NULL,
  id_proveedor INT NOT NULL,
  PRIMARY KEY (id_compra),
  INDEX proveedor1_idx (id_proveedor ASC) VISIBLE,
  CONSTRAINT proveedor1
    FOREIGN KEY (id_proveedor)
    REFERENCES proveedor (id_proveedor)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Tabla Detalles de Compra 
CREATE TABLE IF NOT EXISTS detalles_de_compra (
  id_compra INT NOT NULL,
  codigo_barras CHAR(13) NOT NULL,
  cantidad INT NOT NULL,
  precio_unitario FLOAT NOT NULL,
  subtotal FLOAT NOT NULL,
  PRIMARY KEY (id_compra, codigo_barras),
  INDEX fk_detalles_de_compra_compras1_idx (id_compra ASC) VISIBLE,
  INDEX articulos2_idx (codigo_barras ASC) VISIBLE,
  CONSTRAINT fk_detalles_de_compra_compras1
    FOREIGN KEY (id_compra)
    REFERENCES compras (id_compra)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT articulos2
    FOREIGN KEY (codigo_barras)
    REFERENCES articulos (codigo_barras)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Tabla Inventario
CREATE TABLE IF NOT EXISTS inventario (
    codigo_barras CHAR(13) NOT NULL,
    cantidad INT NOT NULL,
    fecha_actualizacion DATETIME NULL,
    PRIMARY KEY (codigo_barras),
    INDEX articulos3_idx (codigo_barras ASC) VISIBLE,
    CONSTRAINT articulos3
        FOREIGN KEY (codigo_barras)
        REFERENCES articulos (codigo_barras)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
) ENGINE = InnoDB;

INSERT INTO categoria (nombre) VALUES 
('Bebidas'),
('Salchichoneria'),
('Legumbres');

INSERT INTO articulos (codigo_barras, nombre, precio, existencia, unidad, descripcion, id_categoria) VALUES
('7501055307906', 'Agua Natural Ciel 600ml', 14.00, 80, 'ml', 'Agua purificada embotellada',  1),
('7501055333868', 'Jugo del valle Manzana 1ltr', 17.50, 60, 'ltr', 'Jugo natural con azúcar',  1),
('7501055304745', 'Coca-Cola 3ltr', 53.00, 40, 'ltr', 'Refresco de cola',  1),
('7894900053630', 'Refresco fanta sabor uva 600 ml', 18.00, 40, 'ml', 'Refresco sabor uva',  1),
('7503027753629', 'Volt Yellow Energy 473 ml', 12.25, 23, 'ml', 'Bebida energética yellow sabor guarana',  1),
('7501013174038', 'Jugo de mango Jumex 450 ml', 15.90, 46, 'ml', 'Nectar de mango',  1),
('7501020553161', 'Leche Yomi sabor vainilla 1ltr', 30.90, 62, 'ltr', 'Leche sabor vainilla',  1);

INSERT INTO articulos (codigo_barras, nombre, precio, existencia, unidad, descripcion, id_categoria) VALUES
('7501040000218', 'Salchicha Pavo FUD 266g', 18.90, 50, 'Paquete', 'Salchicha cocida tipo FUD', 2),
('7501040027307', 'Chorizo vegetariano San Rafael 200g', 38.00, 40, 'Paquete', 'Chorizo vegetariano elaborado con alubias y proteína de chícharo', 2),
('7501325703599', 'Jamón lunch de pavo KIR 220g', 23.80, 30, 'Paquete', 'Elaborado con carne de pavo de alta calidad,', 2),
('7501040005428', 'Tocino ahumado rebanado fud 250g', 80.80, 30, 'Paquete', 'Tocino con un delicioso sabor ahumado', 2),
('7501040027413', 'Jamon real de pavo san rafael 250g', 57.90, 70, 'Paquete', 'Jabon de pavo', 2),
('7501147512133', 'Tocino ahumado kir 250g', 99.90, 84, 'Paquete', 'Rebanadas de tocino ahumado', 2),
('7501057720253', 'Salchicha de pavo zwan 500g', 53.90, 120, 'Paquete', 'Salchicha hecha de carne de pavo de calidad premium', 2);

INSERT INTO articulos (codigo_barras, nombre, precio, existencia, unidad, descripcion, id_categoria) VALUES
('7501071301049', 'Frijol Negro 900g', 64.90, 70, 'Bolsa', 'Frijol seco negro', 3),
('7501018310295', 'Lenteja la Moderna 200g', 27.00, 65, 'Bolsa', 'Lenteja granel', 3),
('7501003100450', 'Garbanzo Herdez 400g', 25.00, 60, 'Bolsa', 'Grano seco de garbanzo', 3),
('7501037310056', 'Ensalada de legumbres Herdez 215 g', 15.00, 30, 'lata', 'Mezcla enlatada de legumbres cocidas', 3),
('7501047200734', 'Haba pelada la Merced 500g', 19.50, 15, 'Bolsa', 'Maíz palomero La Merced', 3),
('7501071300790', 'Frijol Verde Valle flor de mayo 900g', 59.00, 90, 'Bolsa', 'Frijol flor de mayo', 3);

INSERT INTO clientes (telefono, nombre, apellido, email, direccion) VALUES
('9611234567', 'Carlos', 'Ramírez', 'carlos.ramirez@gmail.com', 'Calle 5 #123, Centro'),
('9617654321', 'María', 'González', 'maria.gonzalez@gmail.com', 'Av. Insurgentes Sur 456'),
('9616789123', 'Luis', 'Hernández', 'luis.hernandez@gmail.com', 'Col. Roma Norte #78'),
('9612214833', 'Angel', 'Cruz', 'angelin@gmail.com', 'Av. Hidalgo #90'),
('9613711416', 'Lucia', 'Palacios', 'palacios.luci@gmail.com', 'Col. Juan Crispin #31'),
('0000000000', 'Cliente General', '');

INSERT INTO empleados (nombre, apellido, telefono, email, direccion, puesto, sueldo, estatus, contraseña) VALUES
('Ana', 'Lopez', '9611122334', 'ana.lopez@gmail.com', 'Calle Reforma 100', 'Cajera', 3200.00, 'Activo', '18765'),
('Jorge', 'Martínez', '9612233445', 'jorge.martinez@gmail.com', 'Col. Del Valle #200', 'Limpieza', 1500.00, 'Activo', '24516'),
('Elena', 'Sánchez', '9613344556', 'elena.sanchez@gmail.com', 'Zona Centro #321', 'Supervisor', 3600.00, 'Activo', '98612');

INSERT INTO proveedor (nombre, contacto, telefono, email, direccion) VALUES
('Distribuidora Coca-Cola FEMSA', 'Pedro Jiménez', '9617891234', 'cocaCola@bebidasmx.com', 'Bodega 12, Naucalpan'),
('Sigma', 'Laura Torres', '9614321987', 'contacto@sigma.com', 'Av. Industrial 789, Ecatepec'),
('Grupo la Moderna', 'Andrés Morales', '9619876543', 'rsmoderna@lamoderna.com', 'Camino Real 321, Puebla');

INSERT INTO inventario (codigo_barras, cantidad, fecha_actualizacion) VALUES
('7501055307906', 80, STR_TO_DATE('25/04/2025 14:30:00', '%d/%m/%Y %H:%i:%s')),
('7501055333868', 60, STR_TO_DATE('25/04/2025 11:24:12', '%d/%m/%Y %H:%i:%s')),
('7501055304745', 40, STR_TO_DATE('29/04/2025 09:18:54', '%d/%m/%Y %H:%i:%s')),
('7894900053630', 40, STR_TO_DATE('28/05/2025 14:41:40', '%d/%m/%Y %H:%i:%s')),
('7503027753629', 23, STR_TO_DATE('28/05/2025 14:48:59', '%d/%m/%Y %H:%i:%s')),
('7501013174038', 46, STR_TO_DATE('28/05/2025 15:21:59', '%d/%m/%Y %H:%i:%s')),
('7501020553161', 62, STR_TO_DATE('28/05/2025 15:49:01', '%d/%m/%Y %H:%i:%s')),
('7501040000218', 50, STR_TO_DATE('05/05/2025 13:30:40', '%d/%m/%Y %H:%i:%s')),
('7501040027307', 40, STR_TO_DATE('05/05/2025 10:15:34', '%d/%m/%Y %H:%i:%s')),
('7501325703599', 30, STR_TO_DATE('05/05/2025 12:29:11', '%d/%m/%Y %H:%i:%s')),
('7501040005428', 30, STR_TO_DATE('30/05/2025 10:29:11', '%d/%m/%Y %H:%i:%s')),
('7501040027413', 70, STR_TO_DATE('30/05/2025 11:09:11', '%d/%m/%Y %H:%i:%s')),
('7501147512133', 84, STR_TO_DATE('30/05/2025 12:10:30', '%d/%m/%Y %H:%i:%s')),
('7501057720253', 120, STR_TO_DATE('30/05/2025 12:21:32', '%d/%m/%Y %H:%i:%s')),
('7501071301049', 70, STR_TO_DATE('14/05/2025 11:31:02', '%d/%m/%Y %H:%i:%s')),
('7501018310295', 65, STR_TO_DATE('14/05/2025 14:41:40', '%d/%m/%Y %H:%i:%s')),
('7501003100450', 60, STR_TO_DATE('14/05/2025 12:14:32', '%d/%m/%Y %H:%i:%s')),
('7501037310056', 30, STR_TO_DATE('29/05/2025 12:41:13', '%d/%m/%Y %H:%i:%s')),
('7501047200734', 15, STR_TO_DATE('29/05/2025 11:21:10', '%d/%m/%Y %H:%i:%s')),
('7501071300790', 90, STR_TO_DATE('29/05/2025 10:07:19', '%d/%m/%Y %H:%i:%s'));


