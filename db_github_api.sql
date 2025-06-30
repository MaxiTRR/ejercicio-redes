-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-06-2025 a las 17:00:56
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db_github_api`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `followers`
--

CREATE TABLE `followers` (
  `id` int(11) NOT NULL,
  `login` varchar(255) NOT NULL,
  `html_url` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `followers`
--

INSERT INTO `followers` (`id`, `login`, `html_url`) VALUES
(2, 'luisdatc', 'https://github.com/luisdatc');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `repositorios`
--

CREATE TABLE `repositorios` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `html_url` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `repositorios`
--

INSERT INTO `repositorios` (`id`, `name`, `html_url`) VALUES
(16, 'Proyecto_final', 'https://github.com/MaxiTRR/Proyecto_final'),
(17, 'ejercicio-redes', 'https://github.com/MaxiTRR/ejercicio-redes'),
(18, 'ejer_redes_ifts4_2025', 'https://github.com/MaxiTRR/ejer_redes_ifts4_2025'),
(19, 'Repo_prueba', 'https://github.com/MaxiTRR/Repo_prueba'),
(20, 'Seminario2025_Maxi_Torres', 'https://github.com/MaxiTRR/Seminario2025_Maxi_Torres'),
(21, 'Proyecto_final', 'https://github.com/MaxiTRR/Proyecto_final'),
(22, 'ejercicio-redes', 'https://github.com/MaxiTRR/ejercicio-redes'),
(23, 'ejer_redes_ifts4_2025', 'https://github.com/MaxiTRR/ejer_redes_ifts4_2025'),
(24, 'Repo_prueba', 'https://github.com/MaxiTRR/Repo_prueba'),
(25, 'Seminario2025_Maxi_Torres', 'https://github.com/MaxiTRR/Seminario2025_Maxi_Torres');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `followers`
--
ALTER TABLE `followers`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `repositorios`
--
ALTER TABLE `repositorios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `followers`
--
ALTER TABLE `followers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `repositorios`
--
ALTER TABLE `repositorios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
