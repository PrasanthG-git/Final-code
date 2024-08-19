-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 06, 2023 at 12:30 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `info`
--

-- --------------------------------------------------------

--
-- Table structure for table `atmtb`
--

CREATE TABLE `atmtb` (
  `card_number` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `atmtb`
--

INSERT INTO `atmtb` (`card_number`) VALUES
('7777'),
('7777'),
('1234'),
('1234'),
('1234'),
('1234'),
('1234'),
('0001'),
('0001'),
('1212'),
('1212'),
('1212'),
('0007'),
('0007'),
('5552'),
('5552'),
('5552'),
('5552'),
('5552'),
('5552'),
('5552'),
('9999'),
('9999'),
('9999'),
('9999'),
('9999'),
('9999'),
('0001'),
('0001'),
('0001'),
('0007'),
('0007'),
('0007'),
('0611'),
('0611'),
('0611'),
('0611'),
('0611'),
('0611'),
('0611'),
('0611'),
('0611'),
('0611'),
('00005'),
('00005'),
('00005'),
('00005'),
('00005'),
('0000'),
('0000'),
('00005'),
('0000'),
('0000'),
('1010'),
('1011'),
('1011'),
('1011'),
('1011'),
('123489'),
('123456');

-- --------------------------------------------------------

--
-- Table structure for table `counts`
--

CREATE TABLE `counts` (
  `id` int(11) NOT NULL,
  `name` varchar(32) DEFAULT NULL,
  `count` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `counts`
--

INSERT INTO `counts` (`id`, `name`, `count`) VALUES
(1, 'DMK', '0'),
(2, 'ADMK', '0'),
(3, 'BMK', '0');

-- --------------------------------------------------------

--
-- Table structure for table `duplicate`
--

CREATE TABLE `duplicate` (
  `cardnum` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `duplicate`
--

INSERT INTO `duplicate` (`cardnum`) VALUES
('00005'),
('00005'),
('00005'),
('00005'),
('00005'),
('0000'),
('0000'),
('0005'),
('0005'),
('0005'),
('00005'),
('0000'),
('0000'),
('0000'),
('00005'),
('00005');

-- --------------------------------------------------------

--
-- Table structure for table `facetb`
--

CREATE TABLE `facetb` (
  `card` varchar(32) DEFAULT NULL,
  `un` varchar(32) DEFAULT NULL,
  `email` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `card` varchar(32) DEFAULT NULL,
  `un` varchar(32) DEFAULT NULL,
  `pnum` varchar(32) DEFAULT NULL,
  `add` varchar(32) DEFAULT NULL,
  `email` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`card`, `un`, `pnum`, `add`, `email`) VALUES
('00002', 'block', 'YdHTMsqTN38Xowz0hRIYSH04XOR7F20X', 'desChQm9U6GSRJjwjI6gdu4eKbj7MVWW', 'sdprotrichy2k23@gmail.com'),
('00004', 'pqrst', 'y1EfriA5RkrgW4Kf4kQNoFI3jCMr9Gf+', 'trZg9fCILlkquVAjSaM59Ib97YZWPdbe', 'abc@gmail.com'),
('00005', 'virat', '7JtR2XtYkY6W24FPOt3D22nPFz4kX4Pn', '7js3UevNr0SJYCSaZNhyMzN5iovhc0lS', 'sdprotrichy2k23@gmail.com'),
('0000', 'ts', 'KAhrKBy8uVs80667aQQtBPRoe2bfYfm/', 'DHawon+Y88YlbIk8ARiQAOJjdQTaSdRy', 'ts@gmail.com'),
('0000', 'ts', 'jBkL+cYWSe9R8TWQMdBkCRXHxYa6wEYP', 'wky8OSDObGnoKQwW60xVv1E8BCL8G0zp', 'ts@gmail.com'),
('12345', 'strak', 'I/H5IaB90RzeWqoJscjanxfVLa1X7NUA', 'P28NBURw2qVSF38s7q3BkNiTHPitOlur', 'sdprotrichy2k23@gmail.com'),
('17117', 'sri', '0YRPbfqDy3qrKttD6T7ucKIIsx/rty11', 'usoy6EEqbUZqKU9kbNLN1F6GUpYlOZJX', 'sdprotrichy2k23@gmail.com'),
('143', 'sri', 'RcqhJQ27hOlSqzZD6FL6U/8VVIxC2OTY', 'RQYGorLOcJSzNKhq/PpNgy7zLBokuMy/', 'sdprotrichy2k23@gmail.com'),
('0611', 'soundarya', 't+hsMRQfXOAdtInT6ym+WFnFCBOrkbci', 'yr5ogre4FXsFBWIlzxVFvUBBCJPQlzfj', 'sdprosolutions@gmail.com'),
('11112020', 'pranitha', '7fBjHHrCAouNoU6YcAaldhLr8Gae1UKA', 'I1bTkjwXcwUX+Y8NsTB51K2dotRLjBbo', 'sdprosolutions@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `counts`
--
ALTER TABLE `counts`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `counts`
--
ALTER TABLE `counts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
