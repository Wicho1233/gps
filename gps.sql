
CREATE DATABASE gps_manhattan CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
 USE gps_manhattan;

-- --------------------------------------------------------
-- Tabla: casetas
-- --------------------------------------------------------
CREATE TABLE `casetas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `latitud` decimal(10,7) NOT NULL,
  `longitud` decimal(10,7) NOT NULL,
  `costo` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Datos de casetas (31 registros)
INSERT INTO `casetas` (`id`, `nombre`, `latitud`, `longitud`, `costo`) VALUES
(1, 'Caseta San Marcos', 19.1726000, -98.3214000, 145.00),
(2, 'Caseta Amozoc', 19.0323000, -98.0860000, 85.00),
(3, 'Caseta Tepotzotlán', 19.7012000, -99.2256000, 168.00),
(4, 'Caseta Atlacomulco', 19.7956000, -99.8765000, 95.00),
(5, 'Caseta Maravatío', 19.8765000, -100.4321000, 78.00),
(6, 'Caseta Acámbaro', 20.0543000, -100.7234000, 120.00),
(7, 'Caseta Tepotzotlán Norte', 19.7234000, -99.2345000, 156.00),
(8, 'Caseta San Juan del Río', 20.3876000, -99.9876000, 89.00),
(9, 'Caseta San Luis Potosí', 21.9876000, -100.8765000, 112.00),
(10, 'Caseta Matehuala', 23.6543000, -100.5432000, 78.00),
(11, 'Caseta San Luis Potosí Norte', 22.5432000, -100.9876000, 134.00),
(12, 'Caseta Saltillo', 25.4321000, -100.9876000, 98.00),
(13, 'Caseta El Castillo', 25.6789000, -100.5432000, 45.00),
(14, 'Caseta Los Chorros', 25.7890000, -100.6543000, 52.00),
(15, 'Caseta Cuernavaca', 19.0123000, -99.2345000, 87.00),
(16, 'Caseta Tepoztlán', 18.9876000, -99.1234000, 65.00),
(17, 'Caseta Orizaba', 18.8765000, -97.0987000, 145.00),
(18, 'Caseta Córdoba', 18.9234000, -96.9876000, 89.00),
(19, 'Caseta Veracruz', 19.1234000, -96.2345000, 76.00),
(20, 'Caseta Tehuacán', 18.4567000, -97.4567000, 112.00),
(21, 'Caseta Oaxaca', 17.9876000, -96.8765000, 95.00),
(22, 'Caseta Tepic', 21.5678000, -104.8765000, 134.00),
(23, 'Caseta León', 21.1234000, -101.6543000, 98.00),
(24, 'Caseta Aguascalientes', 21.8765000, -102.3456000, 76.00),
(25, 'Caseta Zacatecas', 22.7654000, -102.5678000, 89.00),
(26, 'Caseta Reynosa', 26.0987000, -98.3456000, 156.00),
(27, 'Caseta Nuevo Laredo', 27.6543000, -99.5678000, 178.00),
(28, 'Caseta Valladolid', 20.6789000, -88.2345000, 145.00),
(29, 'Caseta Mérida', 20.9876000, -89.5678000, 89.00),
(30, 'Caseta Rosarito', 32.3456000, -117.0987000, 65.00),
(31, 'Caseta Ensenada', 31.8765000, -116.6543000, 78.00);

-- --------------------------------------------------------
-- Tabla: zonas_rojas (con coordenadas)
-- --------------------------------------------------------
CREATE TABLE `zonas_rojas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `nivel_riesgo` int(11) NOT NULL,
  `latitud` decimal(10,7) DEFAULT NULL,
  `longitud` decimal(10,7) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Datos de zonas rojas (63 registros con coordenadas aproximadas)
INSERT INTO `zonas_rojas` (`id`, `nombre`, `nivel_riesgo`, `latitud`, `longitud`) VALUES
(1, 'Ecatepec - Zona Oriente', 8, 19.6018000, -99.0441000),
(2, 'Ecatepec - Zona Norte', 7, 19.6277000, -99.0387000),
(3, 'Ecatepec - Las Américas', 9, 19.5923000, -99.0347000),
(4, 'Chimalhuacán - Centro', 8, 19.4216000, -98.9508000),
(5, 'Chimalhuacán - Xochitenco', 7, 19.4092000, -98.9431000),
(6, 'Nezahualcóyotl - Bordo', 8, 19.4006000, -99.0146000),
(7, 'Nezahualcóyotl - Periferico', 7, 19.3951000, -99.0053000),
(8, 'Tultitlán - Centro', 6, 19.6469000, -99.1697000),
(9, 'Coacalco - Zona Industrial', 6, 19.6336000, -99.1097000),
(10, 'CDMX - Tepito', 9, 19.4452000, -99.1358000),
(11, 'CDMX - Iztapalapa', 8, 19.3595000, -99.0941000),
(12, 'CDMX - Ecatepec', 8, 19.5594000, -99.0510000),
(13, 'CDMX - Nezahualcóyotl', 7, 19.4050000, -99.0140000),
(14, 'CDMX - La Merced', 7, 19.4282000, -99.1234000),
(15, 'CDMX - Morelos', 8, 19.4348000, -99.1366000),
(16, 'Puebla - San Manuel', 7, 19.0685000, -98.2045000),
(17, 'Puebla - La Margarita', 6, 19.0496000, -98.1882000),
(18, 'Puebla - Amalucan', 6, 19.0631000, -98.1759000),
(19, 'Puebla - Zona Centro', 5, 19.0434000, -98.1988000),
(20, 'Puebla - Xonaca', 7, 19.0552000, -98.1869000),
(21, 'Veracruz - Centro Histórico', 6, 19.1903000, -96.1418000),
(22, 'Veracruz - Las Brisas', 7, 19.1798000, -96.1255000),
(23, 'Veracruz - Ejido', 6, 19.1959000, -96.1538000),
(24, 'Xalapa - Centro', 5, 19.5273000, -96.9166000),
(25, 'Xalapa - Colonia Popular', 6, 19.5354000, -96.9255000),
(26, 'Guadalajara - Centro', 6, 20.6751000, -103.3496000),
(27, 'Guadalajara - Oblatos', 8, 20.6893000, -103.3274000),
(28, 'Guadalajara - San Juan de Dios', 7, 20.6763000, -103.3414000),
(29, 'Zapopan - Las Aguilas', 6, 20.7194000, -103.4075000),
(30, 'Tlaquepaque - Centro', 6, 20.6326000, -103.3103000),
(31, 'Monterrey - Centro', 5, 25.6795000, -100.3180000),
(32, 'Monterrey - Independencia', 7, 25.6896000, -100.3366000),
(33, 'Monterrey - San Bernabé', 8, 25.7044000, -100.3573000),
(34, 'Monterrey - Topo Chico', 7, 25.7012000, -100.3388000),
(35, 'Monterrey - La Fama', 6, 25.6941000, -100.3489000),
(36, 'León - Centro', 5, 21.1216000, -101.6843000),
(37, 'León - San Juan Bosco', 6, 21.1386000, -101.6979000),
(38, 'León - 10 de Mayo', 6, 21.1189000, -101.6770000),
(39, 'Irapuato - Centro', 5, 20.6739000, -101.3566000),
(40, 'Celaya - Zona Centro', 5, 20.5248000, -100.8141000),
(41, 'Salamanca - Zona Norte', 6, 20.5739000, -101.2030000),
(42, 'Cuernavaca - Centro', 5, 18.9188000, -99.2346000),
(43, 'Cuernavaca - Colonia Popular', 6, 18.9273000, -99.2452000),
(44, 'Tepoztlán - Centro', 4, 18.9851000, -99.0985000),
(45, 'Yautepec - Centro', 6, 18.8740000, -99.0676000),
(46, 'Chilpancingo - Centro', 7, 17.5508000, -99.5002000),
(47, 'Chilpancingo - Colonia Popular', 8, 17.5623000, -99.5087000),
(48, 'Chilpancingo - Zona Norte', 7, 17.5574000, -99.4950000),
(49, 'Nuevo Laredo - Centro', 9, 27.4863000, -99.5044000),
(50, 'Nuevo Laredo - Colonia Popular', 10, 27.4901000, -99.5187000),
(51, 'Reynosa - Centro', 9, 26.0858000, -98.2799000),
(52, 'Reynosa - Colonia Popular', 10, 26.0926000, -98.2905000),
(53, 'Matamoros - Centro', 9, 25.8738000, -97.5005000),
(54, 'Matamoros - Colonia Popular', 9, 25.8842000, -97.5126000),
(55, 'Culiacán - Centro', 8, 24.8091000, -107.3890000),
(56, 'Culiacán - Colonia Popular', 9, 24.8203000, -107.4011000),
(57, 'Mazatlán - Centro', 7, 23.2367000, -106.4305000),
(58, 'Mazatlán - Zona Norte', 8, 23.2545000, -106.4399000),
(59, 'Tijuana - Centro', 6, 32.5209000, -117.0248000),
(60, 'Tijuana - Zona Norte', 8, 32.5373000, -117.0396000),
(61, 'Tijuana - Otay', 7, 32.5500000, -116.9800000),
(62, 'Tijuana - Colonia Popular', 8, 32.5350000, -117.0180000),
(63, 'Ensenada - Centro', 5, 31.8572000, -116.6277000);

-- --------------------------------------------------------
-- Tabla: restricciones_vehiculo (opcional, para futura extensión)
-- --------------------------------------------------------
CREATE TABLE `restricciones_vehiculo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_vehiculo` varchar(20) NOT NULL,
  `arista_id` int(11) NOT NULL,
  `permitido` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Datos de ejemplo
INSERT INTO `restricciones_vehiculo` (`id`, `tipo_vehiculo`, `arista_id`, `permitido`) VALUES
(1, 'carga', 1, 0),
(2, 'carga', 2, 0),
(3, 'carga', 3, 0),
(4, 'carga', 4, 0),
(5, 'carga', 5, 0),
(6, 'autobus', 6, 0),
(7, 'autobus', 7, 0),
(8, 'autobus', 8, 0),
(9, 'carro', 9, 0),
(10, 'carga', 9, 0),
(11, 'autobus', 9, 0);

-- --------------------------------------------------------
-- Fin del script
-- --------------------------------------------------------