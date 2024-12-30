-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 30, 2024 at 05:46 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pembayaran_listrik`
--

-- --------------------------------------------------------

--
-- Table structure for table `pelanggan`
--

CREATE TABLE `pelanggan` (
  `id_pelanggan` int(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nomor_kwh` int(20) NOT NULL,
  `nomor_va` int(32) NOT NULL,
  `nama_pelanggan` varchar(255) NOT NULL,
  `alamat` text NOT NULL,
  `id_tarif` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pelanggan`
--

INSERT INTO `pelanggan` (`id_pelanggan`, `email`, `password`, `nomor_kwh`, `nomor_va`, `nama_pelanggan`, `alamat`, `id_tarif`) VALUES
(3, 'Salahudinkoliq10@gmail.com', '56650c0be1d954974c26764821d9ed628100d2e2e023f633ccc6b8073ec70c81', 0, 0, 'kholikcipuden', '', 0),
(4, 'salahudinkoliq18@gmail.com', 'eae7c20842851784161968cff1b6b3630fe2cf0bc526f7bd45f7e57775623f9d', 0, 0, 'salahudin', '', 0),
(5, 'salahudinkoliq19@gmail.com', '0b1f7c327273f71c42c898d78a00cf34c1487540f4c1061b7e91af980354aeb8', 0, 0, 'prase', '', 0),
(6, 'user12@gmail.com', '50133b4def1d1d7bada7c7a2fa41a63b338ebb4ca1f2e74681802e59b344e1c0', 0, 0, 'user', '', 0),
(7, 'user13@gmail.com', '56650c0be1d954974c26764821d9ed628100d2e2e023f633ccc6b8073ec70c81', 0, 2147483647, 'salahudin12', 'bekasi regensi 1 blok j5 / 46', 0);

--
-- Triggers `pelanggan`
--
DELIMITER $$
CREATE TRIGGER `deleteDataPelanggan` AFTER DELETE ON `pelanggan` FOR EACH ROW BEGIN
	DELETE FROM account WHERE nama = OLD.nama_pelanggan;
END
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pelanggan`
--
ALTER TABLE `pelanggan`
  ADD PRIMARY KEY (`id_pelanggan`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pelanggan`
--
ALTER TABLE `pelanggan`
  MODIFY `id_pelanggan` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
