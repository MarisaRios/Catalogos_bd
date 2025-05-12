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
