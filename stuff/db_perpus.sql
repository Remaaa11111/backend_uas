-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 09, 2025 at 04:08 PM
-- Server version: 8.0.30
-- PHP Version: 8.4.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_perpus`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id_buku` int NOT NULL,
  `judul` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `penulis` varchar(100) NOT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `cover_image` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `harga` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `stok_buku` int NOT NULL,
  `deskripsi` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` enum('available','not available') NOT NULL DEFAULT 'available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id_buku`, `judul`, `penulis`, `genre`, `cover_image`, `harga`, `created_at`, `stok_buku`, `deskripsi`, `status`) VALUES
(17, 'Working Effectively With Legacy Code', 'Michael Feathers', 'Novel', 'https://images-na.ssl-images-amazon.com/images/I/51yS8PYs03L._SX258_BO1,204,203,200_.jpg', '10000', '2025-07-09 07:36:07', 1, 'Di tengah tumpukan kode lama yang rapuh dan tak bertuan, seorang programmer berjuang menjaga sistem tetap hidup tanpa menghancurkan segalanya. Ini adalah kisah teknis penuh ketegangan, di mana setiap baris perubahan bisa menjadi penyelamat atau malapetaka.', 'available'),
(33, 'The Sandman', 'Neil Gaiman', 'Comic', 'https://upload.wikimedia.org/wikipedia/en/8/85/Sandman_no.1_%28Modern_Age%29.comiccover.jpg', '10000', '2025-07-09 14:48:59', 3, 'Seri fantasi gelap yang mengisahkan Morpheus, dewa mimpi, dalam perjuangannya setelah lepas dari kurungan selama satu abad. Kaya akan simbolisme dan mitologi.', 'available'),
(34, 'Knowledge Encyclopedia: Science!', 'DK Publishing', 'Encyclopedia', 'https://m.media-amazon.com/images/I/91iNILVHQYL._SY522_.jpg', '10000', '2025-07-09 14:53:45', 1, 'Buku ensiklopedia visual penuh gambar dan infografis yang menjelaskan konsep-konsep sains dari atom hingga luar angkasa. Cocok untuk pelajar maupun dewasa.', 'available'),
(35, 'Steve Jobs', 'Walter Isaacson', 'Biography', 'https://res.cloudinary.com/bloomsbury-atlas/image/upload/w_360,c_scale,dpr_1.5/jackets/9781610694971.jpg', '10000', '2025-07-09 14:58:02', 1, 'Biografi resmi Steve Jobs berdasarkan lebih dari 40 wawancara. Menggambarkan sisi visioner, keras kepala, dan jenius dari pendiri Apple tersebut.', 'available'),
(36, 'A Short History of Nearly Everything', 'Bill Bryson', 'Science', 'https://m.media-amazon.com/images/I/71yt6mN5HuL._SL1500_.jpg', '10000', '2025-07-09 14:59:16', 1, 'Buku sains populer yang menjelaskan sejarah dan perkembangan ilmu pengetahuan dari asal-usul alam semesta hingga manusia, dengan humor dan gaya bercerita menarik.', 'available'),
(37, 'Everything You Need to Ace Science in One Big Fat Notebook', 'Workman Publishing', 'Education', 'https://m.media-amazon.com/images/I/71+QMjYtd-L._SL1500_.jpg', '10000', '2025-07-09 15:00:41', 1, 'Buku ringkasan pelajaran IPA untuk SMP/SMA. Menjelaskan topik-topik dengan cara sederhana, penuh catatan, diagram, dan ilustrasi.', 'available'),
(38, 'Gone Girl', 'Gillian Flynn', 'Mystery', 'https://cdn0-production-images-kly.akamaized.net/koHkISfw90Rp5S5yaQkw5vrX5w4=/1280x1706/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/4336752/original/010035600_1677239140-Gone_Girl_1.jpg', '10000', '2025-07-09 15:01:49', 1, 'Thriller psikologis tentang hilangnya seorang istri, dan sang suami menjadi tersangka utama. Penuh plot twist dan narasi yang menggugah.', 'available'),
(39, 'Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'History', 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1703329310i/23692271.jpg', '10000', '2025-07-09 15:03:09', 1, 'Menelusuri sejarah umat manusia dari Homo sapiens awal hingga era globalisasi. Menjelaskan bagaimana budaya, politik, dan ekonomi terbentuk.', 'available'),
(40, 'The Case for Christ', 'Lee Strobel', 'Religion', 'https://m.media-amazon.com/images/I/71McrITcpNL._SL1500_.jpg', '10000', '2025-07-09 15:04:31', 1, 'Jurnalis investigatif mencari bukti historis dan ilmiah tentang keberadaan Yesus Kristus. Ditulis dengan pendekatan logis dan apologetik.', 'available'),
(41, '7 Prajurit Bapak', 'Wulan Nuramalia', 'Novel', 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1650690791i/60865069.jpg', '10000', '2025-07-09 15:07:00', 1, 'Novel ini mengisahkan kehidupan keluarga pensiunan tentara dan perjuangan tujuh anak lelakinya. Tema utamanya adalah mengejar mimpi, penghargaan terhadap keluarga, serta tanggung jawab pribadi dalam menghadapi tekanan sosial dan tradisi .', 'available');

-- --------------------------------------------------------

--
-- Table structure for table `history_log`
--

CREATE TABLE `history_log` (
  `id_log` int NOT NULL,
  `id_peminjaman` int NOT NULL,
  `status` enum('dipinjam','returned','canceled') NOT NULL,
  `waktu` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `keterangan` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `history_log`
--

INSERT INTO `history_log` (`id_log`, `id_peminjaman`, `status`, `waktu`, `keterangan`) VALUES
(17, 46, 'dipinjam', '2025-07-09 14:05:18', 'Peminjaman dibuat dengan status dipinjam'),
(18, 46, 'returned', '2025-07-09 14:05:29', 'Status diubah ke returned'),
(19, 47, 'dipinjam', '2025-07-09 14:26:55', 'Peminjaman dibuat dengan status dipinjam'),
(20, 48, 'dipinjam', '2025-07-09 14:27:10', 'Peminjaman dibuat dengan status dipinjam'),
(21, 47, 'returned', '2025-07-09 15:20:30', 'Status diubah ke returned'),
(22, 49, 'dipinjam', '2025-07-09 15:20:53', 'Peminjaman dibuat dengan status dipinjam'),
(23, 50, 'dipinjam', '2025-07-09 15:50:49', 'Peminjaman dibuat dengan status dipinjam');

-- --------------------------------------------------------

--
-- Table structure for table `loans`
--

CREATE TABLE `loans` (
  `id_peminjaman` int NOT NULL,
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  `tanggal_pinjam` date NOT NULL,
  `tanggal_kembali` date NOT NULL,
  `status` enum('scheduled','borrowed','returned','overdue') DEFAULT 'borrowed',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `loans`
--

INSERT INTO `loans` (`id_peminjaman`, `user_id`, `book_id`, `tanggal_pinjam`, `tanggal_kembali`, `status`, `created_at`) VALUES
(46, 5, 17, '2025-07-09', '2025-07-09', 'returned', '2025-07-09 14:05:18'),
(47, 5, 17, '2025-07-09', '2025-07-09', 'returned', '2025-07-09 14:26:55'),
(48, 5, 17, '2025-07-09', '2025-07-16', 'borrowed', '2025-07-09 14:27:10'),
(49, 6, 17, '2025-07-09', '2025-07-16', 'borrowed', '2025-07-09 15:20:53'),
(50, 5, 39, '2025-07-09', '2025-07-16', 'borrowed', '2025-07-09 15:50:49');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `email` varchar(100) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `alamat` varchar(255) DEFAULT NULL,
  `avatar_url` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'member',
  `status` varchar(50) DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `nama`, `phone`, `alamat`, `avatar_url`, `password`, `role`, `status`) VALUES
(5, 'trisna@gmail.com', 'trisna', '081703036551', 'gang beo', 'https://i.pinimg.com/736x/b2/ce/e5/b2cee58c6063e8b50f597a3b6db7cb83.jpg', '$2b$12$SeFeF8ug7OCCaQP0M.7acu1gj257S4rR8HiL7GbrDdwbGDboevzoy', 'member', 'active'),
(6, 'admin@gmail.com', 'admin', '08170220334', 'gangbeo', 'https://i.pinimg.com/originals/bb/89/e8/bb89e879322828b386983c50d14e7fa1.jpg', '$2b$12$OY3qAXObrvZKIOKsYxCZ.e4y4qyh5rWBY98vadSfxfU0PFXpxbh4m', 'admin', 'active'),
(23, 'gitaa@gmail.com', 'amaragita', '1122333333', NULL, NULL, '$2b$12$uqFDropxzXBPGY/cW.eEGOan99fJaQ4SNrJNttZSorYq/X2n1EQTq', 'user', 'active'),
(24, 'sucitra@gmail.com', 'sucitra', '123456789', NULL, NULL, '$2b$12$GLagOGMAOEGUi9e1AeM22eqHJYlA/ul9SfahxMjQcDDeK9wA3tI/6', 'user', 'active'),
(25, 'teguh@gmail.com', 'teguh', '1122333333', NULL, NULL, '$2b$12$LZIXCa4pvriJ2dAElVgeHeQSOmMRQRQ7J/skfd.Y/U7w1UOaufAWW', 'user', 'active');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id_buku`);

--
-- Indexes for table `history_log`
--
ALTER TABLE `history_log`
  ADD PRIMARY KEY (`id_log`),
  ADD KEY `id_peminjaman` (`id_peminjaman`);

--
-- Indexes for table `loans`
--
ALTER TABLE `loans`
  ADD PRIMARY KEY (`id_peminjaman`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id_buku` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `history_log`
--
ALTER TABLE `history_log`
  MODIFY `id_log` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `loans`
--
ALTER TABLE `loans`
  MODIFY `id_peminjaman` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `history_log`
--
ALTER TABLE `history_log`
  ADD CONSTRAINT `history_log_ibfk_1` FOREIGN KEY (`id_peminjaman`) REFERENCES `loans` (`id_peminjaman`) ON DELETE CASCADE;

--
-- Constraints for table `loans`
--
ALTER TABLE `loans`
  ADD CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `loans_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id_buku`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
