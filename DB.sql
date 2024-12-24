DROP DATABASE IF EXISTS `PragmaTest`;

-- Crea la base de datos si no existe.
CREATE DATABASE IF NOT EXISTS `PragmaTest`;

-- Selecciona la base de datos para trabajar en ella.
USE `PragmaTest`;

-- Dimensión de usuarios
CREATE TABLE `dim_user` (
	`id` INT UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
	`user_key` INT UNIQUE NOT NULL
);

-- Dimensión de tiempo
CREATE TABLE `dim_time` (
	`id` INT UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
	`date` DATE UNIQUE NOT NULL,
	`year` INT NOT NULL,
	`semester` TINYINT NOT NULL COMMENT '1: Primer semestre, 2: Segundo semestre',
	`trimester` TINYINT NOT NULL COMMENT '1 a 4: Trimestres del año',
	`month` TINYINT NOT NULL COMMENT '1 a 12: Meses del año'
);

-- Hechos de ventas
CREATE TABLE `facts_sales` (
	`id` INT UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
	`user_id` INT NOT NULL,
	`time_id` INT NOT NULL,
	`price` DECIMAL(10, 2) NOT NULL COMMENT 'Monto de las ventas',
	FOREIGN KEY (`user_id`) REFERENCES `dim_user`(`id`),
	FOREIGN KEY (`time_id`) REFERENCES `dim_time`(`id`)
);