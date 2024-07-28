-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 28, 2024 at 09:06 PM
-- Server version: 10.1.36-MariaDB
-- PHP Version: 5.6.38

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
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
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `id` int(11) NOT NULL,
  `nama` text NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `id_level` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`id`, `nama`, `email`, `password`, `id_level`) VALUES
(3, 'admin', 'admin@gmail.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 1),
(7, 'kholikcipuden', 'Salahudinkoliq10@gmail.com', '56650c0be1d954974c26764821d9ed628100d2e2e023f633ccc6b8073ec70c81', 2),
(8, 'salahudin', 'salahudinkoliq18@gmail.com', 'eae7c20842851784161968cff1b6b3630fe2cf0bc526f7bd45f7e57775623f9d', 2),
(9, 'prase', 'salahudinkoliq19@gmail.com', '0b1f7c327273f71c42c898d78a00cf34c1487540f4c1061b7e91af980354aeb8', 2),
(10, 'user', 'user12@gmail.com', '50133b4def1d1d7bada7c7a2fa41a63b338ebb4ca1f2e74681802e59b344e1c0', 2);

--
-- Triggers `account`
--
DELIMITER $$
CREATE TRIGGER `updateDataPelanggan` AFTER INSERT ON `account` FOR EACH ROW BEGIN
	IF NEW.id_level = 2 THEN
        INSERT INTO pelanggan (nama_pelanggan, email, password)
        VALUES (NEW.nama, NEW.email, NEW.password);
    END IF;

END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `level`
--

CREATE TABLE `level` (
  `id` int(11) NOT NULL,
  `nama_level` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `level`
--

INSERT INTO `level` (`id`, `nama_level`) VALUES
(1, 'admin'),
(2, 'user');

-- --------------------------------------------------------

--
-- Table structure for table `pelanggan`
--

CREATE TABLE `pelanggan` (
  `id_pelanggan` int(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nomor_kwh` int(20) NOT NULL,
  `nama_pelanggan` varchar(255) NOT NULL,
  `alamat` text NOT NULL,
  `id_tarif` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pelanggan`
--

INSERT INTO `pelanggan` (`id_pelanggan`, `email`, `password`, `nomor_kwh`, `nama_pelanggan`, `alamat`, `id_tarif`) VALUES
(3, 'Salahudinkoliq10@gmail.com', '56650c0be1d954974c26764821d9ed628100d2e2e023f633ccc6b8073ec70c81', 0, 'kholikcipuden', '', 0),
(4, 'salahudinkoliq18@gmail.com', 'eae7c20842851784161968cff1b6b3630fe2cf0bc526f7bd45f7e57775623f9d', 0, 'salahudin', '', 0),
(5, 'salahudinkoliq19@gmail.com', '0b1f7c327273f71c42c898d78a00cf34c1487540f4c1061b7e91af980354aeb8', 0, 'prase', '', 0),
(6, 'user12@gmail.com', '50133b4def1d1d7bada7c7a2fa41a63b338ebb4ca1f2e74681802e59b344e1c0', 0, 'user', '', 0);

--
-- Triggers `pelanggan`
--
DELIMITER $$
CREATE TRIGGER `deleteDataPelanggan` AFTER DELETE ON `pelanggan` FOR EACH ROW BEGIN
	DELETE FROM account WHERE nama = OLD.nama_pelanggan;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `pembayaran`
--

CREATE TABLE `pembayaran` (
  `id_pembayaran` int(11) NOT NULL,
  `id_tagihan` int(11) NOT NULL,
  `id_pelanggan` int(20) NOT NULL,
  `tanggal_pembayaran` date NOT NULL,
  `bulan_bayar` int(20) NOT NULL,
  `bayar_admin` int(20) NOT NULL,
  `total_bayar` int(20) NOT NULL,
  `id_user` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `penggunaan`
--

CREATE TABLE `penggunaan` (
  `id_penggunaan` int(20) NOT NULL,
  `nama_pelanggan` varchar(255) NOT NULL,
  `tanggal_pengecekan` date NOT NULL,
  `bulan` varchar(255) NOT NULL,
  `tahun` year(4) NOT NULL,
  `meter_awal` int(20) NOT NULL,
  `meter_akhir` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `penggunaan`
--

INSERT INTO `penggunaan` (`id_penggunaan`, `nama_pelanggan`, `tanggal_pengecekan`, `bulan`, `tahun`, `meter_awal`, `meter_akhir`) VALUES
(2, 'salahudin', '2024-07-16', 'Maret', 2002, 100, 1000),
(3, 'user', '2024-07-16', 'Juli', 0000, 100, 10000000),
(4, 'kholikcipuden', '2003-05-12', 'Mei', 2003, 85, 10000);

-- --------------------------------------------------------

--
-- Table structure for table `tagihan`
--

CREATE TABLE `tagihan` (
  `id_tagihan` int(20) NOT NULL,
  `id_penggunaan` int(20) NOT NULL,
  `id_pelanggan` int(20) NOT NULL,
  `bulan` varchar(255) NOT NULL,
  `tahun` year(4) NOT NULL,
  `jumlah_meter` int(20) NOT NULL,
  `status` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tarif`
--

CREATE TABLE `tarif` (
  `id_tarif` int(20) NOT NULL,
  `daya` int(20) NOT NULL,
  `tarifperkwh` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tarif`
--

INSERT INTO `tarif` (`id_tarif`, `daya`, `tarifperkwh`) VALUES
(6, 900, 2500),
(7, 2500, 12000),
(8, 8900, 1200);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`id`),
  ADD KEY `relasi_level` (`id_level`);

--
-- Indexes for table `level`
--
ALTER TABLE `level`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pelanggan`
--
ALTER TABLE `pelanggan`
  ADD PRIMARY KEY (`id_pelanggan`);

--
-- Indexes for table `pembayaran`
--
ALTER TABLE `pembayaran`
  ADD PRIMARY KEY (`id_pembayaran`);

--
-- Indexes for table `penggunaan`
--
ALTER TABLE `penggunaan`
  ADD PRIMARY KEY (`id_penggunaan`);

--
-- Indexes for table `tagihan`
--
ALTER TABLE `tagihan`
  ADD PRIMARY KEY (`id_tagihan`);

--
-- Indexes for table `tarif`
--
ALTER TABLE `tarif`
  ADD PRIMARY KEY (`id_tarif`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `level`
--
ALTER TABLE `level`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `pelanggan`
--
ALTER TABLE `pelanggan`
  MODIFY `id_pelanggan` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `pembayaran`
--
ALTER TABLE `pembayaran`
  MODIFY `id_pembayaran` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `penggunaan`
--
ALTER TABLE `penggunaan`
  MODIFY `id_penggunaan` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `tagihan`
--
ALTER TABLE `tagihan`
  MODIFY `id_tagihan` int(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tarif`
--
ALTER TABLE `tarif`
  MODIFY `id_tarif` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account`
--
ALTER TABLE `account`
  ADD CONSTRAINT `relasi_level` FOREIGN KEY (`id_level`) REFERENCES `level` (`id`) ON DELETE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
