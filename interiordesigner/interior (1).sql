-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 20, 2025 at 10:43 AM
-- Server version: 10.6.15-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `interior`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add designer', 7, 'add_designer'),
(26, 'Can change designer', 7, 'change_designer'),
(27, 'Can delete designer', 7, 'delete_designer'),
(28, 'Can view designer', 7, 'view_designer'),
(29, 'Can add product', 8, 'add_product'),
(30, 'Can change product', 8, 'change_product'),
(31, 'Can delete product', 8, 'delete_product'),
(32, 'Can view product', 8, 'view_product'),
(33, 'Can add seller', 9, 'add_seller'),
(34, 'Can change seller', 9, 'change_seller'),
(35, 'Can delete seller', 9, 'delete_seller'),
(36, 'Can view seller', 9, 'view_seller'),
(37, 'Can add cart', 10, 'add_cart'),
(38, 'Can change cart', 10, 'change_cart'),
(39, 'Can delete cart', 10, 'delete_cart'),
(40, 'Can view cart', 10, 'view_cart'),
(41, 'Can add portfolio', 11, 'add_portfolio'),
(42, 'Can change portfolio', 11, 'change_portfolio'),
(43, 'Can delete portfolio', 11, 'delete_portfolio'),
(44, 'Can view portfolio', 11, 'view_portfolio'),
(45, 'Can add cart item', 12, 'add_cartitem'),
(46, 'Can change cart item', 12, 'change_cartitem'),
(47, 'Can delete cart item', 12, 'delete_cartitem'),
(48, 'Can view cart item', 12, 'view_cartitem'),
(49, 'Can add user profile', 13, 'add_userprofile'),
(50, 'Can change user profile', 13, 'change_userprofile'),
(51, 'Can delete user profile', 13, 'delete_userprofile'),
(52, 'Can view user profile', 13, 'view_userprofile'),
(53, 'Can add design', 14, 'add_design'),
(54, 'Can change design', 14, 'change_design'),
(55, 'Can delete design', 14, 'delete_design'),
(56, 'Can view design', 14, 'view_design'),
(57, 'Can add feedback', 15, 'add_feedback'),
(58, 'Can change feedback', 15, 'change_feedback'),
(59, 'Can delete feedback', 15, 'delete_feedback'),
(60, 'Can view feedback', 15, 'view_feedback'),
(61, 'Can add favorite', 16, 'add_favorite'),
(62, 'Can change favorite', 16, 'change_favorite'),
(63, 'Can delete favorite', 16, 'delete_favorite'),
(64, 'Can view favorite', 16, 'view_favorite'),
(65, 'Can add association', 17, 'add_association'),
(66, 'Can change association', 17, 'change_association'),
(67, 'Can delete association', 17, 'delete_association'),
(68, 'Can view association', 17, 'view_association'),
(69, 'Can add code', 18, 'add_code'),
(70, 'Can change code', 18, 'change_code'),
(71, 'Can delete code', 18, 'delete_code'),
(72, 'Can view code', 18, 'view_code'),
(73, 'Can add nonce', 19, 'add_nonce'),
(74, 'Can change nonce', 19, 'change_nonce'),
(75, 'Can delete nonce', 19, 'delete_nonce'),
(76, 'Can view nonce', 19, 'view_nonce'),
(77, 'Can add user social auth', 20, 'add_usersocialauth'),
(78, 'Can change user social auth', 20, 'change_usersocialauth'),
(79, 'Can delete user social auth', 20, 'delete_usersocialauth'),
(80, 'Can view user social auth', 20, 'view_usersocialauth'),
(81, 'Can add partial', 21, 'add_partial'),
(82, 'Can change partial', 21, 'change_partial'),
(83, 'Can delete partial', 21, 'delete_partial'),
(84, 'Can view partial', 21, 'view_partial'),
(85, 'Can add order item', 22, 'add_orderitem'),
(86, 'Can change order item', 22, 'change_orderitem'),
(87, 'Can delete order item', 22, 'delete_orderitem'),
(88, 'Can view order item', 22, 'view_orderitem'),
(89, 'Can add order', 23, 'add_order'),
(90, 'Can change order', 23, 'change_order'),
(91, 'Can delete order', 23, 'delete_order'),
(92, 'Can view order', 23, 'view_order'),
(93, 'Can add budget allocation', 24, 'add_budgetallocation'),
(94, 'Can change budget allocation', 24, 'change_budgetallocation'),
(95, 'Can delete budget allocation', 24, 'delete_budgetallocation'),
(96, 'Can view budget allocation', 24, 'view_budgetallocation'),
(97, 'Can add budget plan', 25, 'add_budgetplan'),
(98, 'Can change budget plan', 25, 'change_budgetplan'),
(99, 'Can delete budget plan', 25, 'delete_budgetplan'),
(100, 'Can view budget plan', 25, 'view_budgetplan'),
(101, 'Can add bundle deal', 26, 'add_bundledeal'),
(102, 'Can change bundle deal', 26, 'change_bundledeal'),
(103, 'Can delete bundle deal', 26, 'delete_bundledeal'),
(104, 'Can view bundle deal', 26, 'view_bundledeal');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$870000$W0SWfny2VWOF9Pvu0rtdC5$2FezF82sJqjrW9fIymFCtFDBIQmMTNSEMLsB/8P76lQ=', '2025-02-20 03:45:44.760556', 0, 'jerry', 'Jerry', 'James', 'jerryjames@gmail.com', 0, 1, '2025-02-13 04:50:02.108240'),
(2, 'pbkdf2_sha256$870000$D0c9d655qXW5ZcgZsnZ1oO$OYOcWkcz6BHzeFO55HPetHDGpCvawDhwJED6xITmUuk=', NULL, 0, 'Alantom', 'Alan', '', 'alan@gmail.com', 0, 1, '2025-02-13 04:52:05.508828'),
(3, 'pbkdf2_sha256$870000$npxwgy73IqYNX2f11HxvQ2$W8QvuDozC5uLLuPN2LH83KEZk69MvLKF+BKMACYVebY=', NULL, 0, 'Amaltom', 'Amal', '', 'amal@gmail.com', 0, 1, '2025-02-13 04:54:30.888580');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(24, 'InteriorApp', 'budgetallocation'),
(25, 'InteriorApp', 'budgetplan'),
(26, 'InteriorApp', 'bundledeal'),
(10, 'InteriorApp', 'cart'),
(12, 'InteriorApp', 'cartitem'),
(14, 'InteriorApp', 'design'),
(7, 'InteriorApp', 'designer'),
(16, 'InteriorApp', 'favorite'),
(15, 'InteriorApp', 'feedback'),
(23, 'InteriorApp', 'order'),
(22, 'InteriorApp', 'orderitem'),
(11, 'InteriorApp', 'portfolio'),
(8, 'InteriorApp', 'product'),
(9, 'InteriorApp', 'seller'),
(13, 'InteriorApp', 'userprofile'),
(6, 'sessions', 'session'),
(17, 'social_django', 'association'),
(18, 'social_django', 'code'),
(19, 'social_django', 'nonce'),
(21, 'social_django', 'partial'),
(20, 'social_django', 'usersocialauth');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-02-13 04:47:49.332357'),
(2, 'auth', '0001_initial', '2025-02-13 04:47:49.542547'),
(3, 'InteriorApp', '0001_initial', '2025-02-13 04:47:49.740695'),
(4, 'InteriorApp', '0002_remove_design_price_remove_userprofile_website_and_more', '2025-02-13 04:47:50.273552'),
(5, 'admin', '0001_initial', '2025-02-13 04:47:50.324389'),
(6, 'admin', '0002_logentry_remove_auto_add', '2025-02-13 04:47:50.333868'),
(7, 'admin', '0003_logentry_add_action_flag_choices', '2025-02-13 04:47:50.341264'),
(8, 'contenttypes', '0002_remove_content_type_name', '2025-02-13 04:47:50.380133'),
(9, 'auth', '0002_alter_permission_name_max_length', '2025-02-13 04:47:50.406818'),
(10, 'auth', '0003_alter_user_email_max_length', '2025-02-13 04:47:50.422758'),
(11, 'auth', '0004_alter_user_username_opts', '2025-02-13 04:47:50.430119'),
(12, 'auth', '0005_alter_user_last_login_null', '2025-02-13 04:47:50.453202'),
(13, 'auth', '0006_require_contenttypes_0002', '2025-02-13 04:47:50.454569'),
(14, 'auth', '0007_alter_validators_add_error_messages', '2025-02-13 04:47:50.460856'),
(15, 'auth', '0008_alter_user_username_max_length', '2025-02-13 04:47:50.477035'),
(16, 'auth', '0009_alter_user_last_name_max_length', '2025-02-13 04:47:50.493102'),
(17, 'auth', '0010_alter_group_name_max_length', '2025-02-13 04:47:50.514574'),
(18, 'auth', '0011_update_proxy_permissions', '2025-02-13 04:47:50.522710'),
(19, 'auth', '0012_alter_user_first_name_max_length', '2025-02-13 04:47:50.538974'),
(20, 'sessions', '0001_initial', '2025-02-13 04:47:50.559329'),
(21, 'default', '0001_initial', '2025-02-13 04:47:50.671835'),
(22, 'social_auth', '0001_initial', '2025-02-13 04:47:50.672934'),
(23, 'default', '0002_add_related_name', '2025-02-13 04:47:50.682305'),
(24, 'social_auth', '0002_add_related_name', '2025-02-13 04:47:50.683253'),
(25, 'default', '0003_alter_email_max_length', '2025-02-13 04:47:50.694376'),
(26, 'social_auth', '0003_alter_email_max_length', '2025-02-13 04:47:50.695395'),
(27, 'default', '0004_auto_20160423_0400', '2025-02-13 04:47:50.702865'),
(28, 'social_auth', '0004_auto_20160423_0400', '2025-02-13 04:47:50.704919'),
(29, 'social_auth', '0005_auto_20160727_2333', '2025-02-13 04:47:50.717985'),
(30, 'social_django', '0006_partial', '2025-02-13 04:47:50.742340'),
(31, 'social_django', '0007_code_timestamp', '2025-02-13 04:47:50.776786'),
(32, 'social_django', '0008_partial_timestamp', '2025-02-13 04:47:50.809429'),
(33, 'social_django', '0009_auto_20191118_0520', '2025-02-13 04:47:50.860401'),
(34, 'social_django', '0010_uid_db_index', '2025-02-13 04:47:50.878116'),
(35, 'social_django', '0011_alter_id_fields', '2025-02-13 04:47:50.989241'),
(36, 'social_django', '0012_usersocialauth_extra_data_new', '2025-02-13 04:47:51.035310'),
(37, 'social_django', '0013_migrate_extra_data', '2025-02-13 04:47:51.049916'),
(38, 'social_django', '0014_remove_usersocialauth_extra_data', '2025-02-13 04:47:51.077694'),
(39, 'social_django', '0015_rename_extra_data_new_usersocialauth_extra_data', '2025-02-13 04:47:51.105972'),
(40, 'social_django', '0016_alter_usersocialauth_extra_data', '2025-02-13 04:47:51.116091'),
(41, 'social_django', '0001_initial', '2025-02-13 04:47:51.117458'),
(42, 'social_django', '0004_auto_20160423_0400', '2025-02-13 04:47:51.118464'),
(43, 'social_django', '0005_auto_20160727_2333', '2025-02-13 04:47:51.119471'),
(44, 'social_django', '0002_add_related_name', '2025-02-13 04:47:51.120476'),
(45, 'social_django', '0003_alter_email_max_length', '2025-02-13 04:47:51.121481'),
(46, 'InteriorApp', '0003_remove_design_contact_number_and_more', '2025-02-13 08:15:57.483990'),
(47, 'InteriorApp', '0004_designer_user', '2025-02-13 08:21:26.453299'),
(48, 'InteriorApp', '0005_order_orderitem', '2025-02-13 09:37:35.436535'),
(49, 'InteriorApp', '0006_order_contact_number_order_razorpay_order_id_and_more', '2025-02-13 09:53:02.497620'),
(50, 'InteriorApp', '0007_budgetplan_budgetallocation', '2025-02-17 09:36:38.895615'),
(51, 'InteriorApp', '0008_remove_budgetplan_total_budget_and_more', '2025-02-17 10:04:29.277846'),
(52, 'InteriorApp', '0009_product_style', '2025-02-17 10:16:55.893116'),
(53, 'InteriorApp', '0010_alter_design_options_alter_favorite_options_and_more', '2025-02-17 10:32:50.346985'),
(54, 'InteriorApp', '0011_remove_design_category_design_area_size_and_more', '2025-02-18 03:37:01.008683'),
(55, 'InteriorApp', '0012_alter_product_category', '2025-02-18 08:38:54.053725');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('8tgrmnjia300lw79tpiqg2gddxpwv5m4', '.eJxVjrEOwyAQQ_-FuUIBlHDp2L3fgI7jrqStiBSSKeq_N0gZWo_2s-VdBdzWHLbKS5iSuiqjLr9eRHpxaUF6YnnMmuayLlPUDdFnWvV9Tvy-nezfQMaaj7aMoyBL55BkYBqkY4LkousjGHYEnoXQczzUE4mxYMWDMyJgWdqrds98vtKdO5g:1tkfrR:BzX7WFySfpm6E3_zJxYI8pYCiXXB4IYKBRQiHZJ5UII', '2025-02-20 08:55:17.193930'),
('ij4vg6hby6554kx6y3c2wbpsawn874lb', '.eJxVjrEOwyAQQ_-FuUIBlHDp2L3fgI7jrqStiBSSKeq_N0gZWo_2s-VdBdzWHLbKS5iSuiqjLr9eRHpxaUF6YnnMmuayLlPUDdFnWvV9Tvy-nezfQMaaj7aMoyBL55BkYBqkY4LkousjGHYEnoXQczzUE4mxYMWDMyJgWdqrds98vtKdO5g:1timRc:8WJ8IILklbu7F1prsIY7ev9MO-FZAFss9q1o6oAcUgo', '2025-02-15 03:32:48.263152'),
('siizzmj2545yp0ggqiyv6shc5fbfjzup', 'eyJzZWxsZXIiOiJBcnVucm95IiwiaWQiOjF9:1tl2l0:YaFtLZw6Gam5ser0doAdr6UlCdf91XzTKltbkqTs0C0', '2025-02-21 09:22:10.630962'),
('wavwdjbyfhno5wm69lj28fmf4l0aonb6', 'eyJzZWxsZXIiOiJBcnVucm95IiwiaWQiOjF9:1tkzKX:B5rjP5r70FlL5IU1-ZB9L6_F60Ngyw3U7uEd_y2cVNM', '2025-02-21 05:42:37.552589'),
('xqvd1b4qscvl1rlp4vg9giq4ok0ppl7j', '.eJxVjrEOwyAQQ_-FuUIBlHDp2L3fgI7jrqStiBSSKeq_N0gZWo_2s-VdBdzWHLbKS5iSuiqjLr9eRHpxaUF6YnnMmuayLlPUDdFnWvV9Tvy-nezfQMaaj7aMoyBL55BkYBqkY4LkousjGHYEnoXQczzUE4mxYMWDMyJgWdqrds98vtKdO5g:1tisWc:uy2lQqCcjrfUOwxCNrQv_2hVVL6sOxQ7blzSdPW9YAE', '2025-02-15 10:02:22.097294'),
('yw7osejj9m7bzerzgtu6eonmzfm0t740', '.eJxVjk0OwiAQhe_CuiGl2EJduvcMZBhmpFqLoe3KeHdLwkLf8v3lewsH-xbdvlJ2UxBnoUTz63nABy0lCHdYbkliWrY8eVkqsqarvKZA86V2_w4irPFY8zgyELcakAfCgVtCG7TXvbeKNFpDjGDIH-oRWXW2Y2O1YrYdcaEqeKoRmJ6vmTYKLuVQqfXp8wXTSEQN:1tjwYu:d-e6mr8tjCHvSyXvzCGIdY2tgfjDD9rfmGzlwT9p2tA', '2025-02-18 08:33:08.450272');

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_budgetallocation`
--

CREATE TABLE `interiorapp_budgetallocation` (
  `id` bigint(20) NOT NULL,
  `category` varchar(50) NOT NULL,
  `allocation_percentage` decimal(5,2) NOT NULL,
  `allocated_amount` decimal(10,2) NOT NULL,
  `budget_plan_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_budgetplan`
--

CREATE TABLE `interiorapp_budgetplan` (
  `id` bigint(20) NOT NULL,
  `room_type` varchar(50) NOT NULL,
  `area_size` decimal(8,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `design_style` varchar(50) DEFAULT NULL,
  `max_budget` decimal(10,2) NOT NULL,
  `min_budget` decimal(10,2) NOT NULL,
  `priority_features` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`priority_features`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interiorapp_budgetplan`
--

INSERT INTO `interiorapp_budgetplan` (`id`, `room_type`, `area_size`, `created_at`, `status`, `user_id`, `design_style`, `max_budget`, `min_budget`, `priority_features`) VALUES
(1, 'Living Room', 500.00, '2025-02-17 10:10:40.993183', 'active', 1, 'Modern', 5000.00, 1000.00, '[]'),
(2, 'Living Room', 5000.00, '2025-02-17 10:13:46.328273', 'active', 1, 'Modern', 10000.00, 1000.00, '[]'),
(3, 'Living Room', 3000.00, '2025-02-17 10:16:12.356273', 'active', 1, 'Modern', 10000.00, 5000.00, '[]'),
(4, 'Living Room', 2000.00, '2025-02-17 10:17:45.542979', 'active', 1, 'Modern', 10000.00, 1000.00, '[]'),
(5, 'Living Room', 2000.00, '2025-02-17 10:23:45.055042', 'active', 1, 'Modern', 10000.00, 500.00, '[]'),
(6, 'Living Room', 1000.00, '2025-02-17 10:28:45.628478', 'active', 1, 'Modern', 1000.00, 100.00, '[]'),
(7, 'Living Room', 1000.00, '2025-02-17 10:30:31.260285', 'active', 1, 'Modern', 10000.00, 1000.00, '[]'),
(8, 'Living Room', 2000.00, '2025-02-18 04:07:06.505578', 'active', 1, 'Modern', 3000.00, 1000.00, '[]'),
(9, 'Living Room', 2000.00, '2025-02-18 04:08:52.215133', 'active', 1, 'Modern', 3000.00, 1000.00, '[]'),
(10, 'Living Room', 2000.00, '2025-02-18 04:10:04.755301', 'active', 1, 'Modern', 3000.00, 1000.00, '[]'),
(11, 'Kitchen', 5000.00, '2025-02-18 04:29:55.738596', 'active', 1, 'Modern', 6000.00, 1000.00, '[]'),
(12, 'Kitchen', 5000.00, '2025-02-18 04:30:28.977136', 'active', 1, 'Modern', 6000.00, 1000.00, '[]'),
(13, 'Living Room', 2000.00, '2025-02-18 04:52:29.561223', 'active', 1, 'Modern', 2000.00, 1000.00, '[]'),
(14, 'Kitchen', 2000.00, '2025-02-18 04:52:44.096614', 'active', 1, 'Modern', 2000.00, 1000.00, '[]'),
(15, 'Kitchen', 2000.00, '2025-02-18 04:52:45.629909', 'active', 1, 'Modern', 2000.00, 1000.00, '[]'),
(16, 'Living Room', 2000.00, '2025-02-18 04:53:08.268205', 'active', 1, 'Modern', 2000.00, 1000.00, '[]'),
(17, 'Living Room', 2000.00, '2025-02-18 04:53:30.340360', 'active', 1, 'Modern', 6000.00, 1000.00, '[]'),
(18, 'Living Room', 2000.00, '2025-02-18 05:11:26.363182', 'active', 1, 'Modern', 100.00, 50.00, '[]'),
(19, 'Living Room', 2000.00, '2025-02-18 05:11:47.227724', 'active', 1, 'Modern', 6000.00, 1000.00, '[]');

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_bundledeal`
--

CREATE TABLE `interiorapp_bundledeal` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `discount_percentage` decimal(5,2) NOT NULL,
  `valid_until` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_bundledeal_products`
--

CREATE TABLE `interiorapp_bundledeal_products` (
  `id` bigint(20) NOT NULL,
  `bundledeal_id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_cart`
--

CREATE TABLE `interiorapp_cart` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interiorapp_cart`
--

INSERT INTO `interiorapp_cart` (`id`, `created_at`, `updated_at`, `user_id`) VALUES
(1, '2025-02-13 05:48:52.983941', '2025-02-13 05:48:52.983941', 1);

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_cartitem`
--

CREATE TABLE `interiorapp_cartitem` (
  `id` bigint(20) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL CHECK (`quantity` >= 0),
  `cart_id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interiorapp_cartitem`
--

INSERT INTO `interiorapp_cartitem` (`id`, `quantity`, `cart_id`, `product_id`, `created_at`, `updated_at`) VALUES
(63, 1, 1, 2, '2025-02-20 09:39:00.738945', '2025-02-20 09:39:00.807204');

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_design`
--

CREATE TABLE `interiorapp_design` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `design_name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `designer_id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `room_type` varchar(50) NOT NULL,
  `style` varchar(50) NOT NULL,
  `area_size` decimal(8,2) NOT NULL,
  `features` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`features`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interiorapp_design`
--

INSERT INTO `interiorapp_design` (`id`, `image`, `design_name`, `description`, `designer_id`, `created_at`, `price`, `room_type`, `style`, `area_size`, `features`) VALUES
(1, 'designs/hallway_6ziLXjW.jpeg', 'Hallway Design', 'hallway designs are really great and elegent', 3, '2025-02-13 08:23:05.626554', 0.00, '1', 'Modern', 0.00, '[]'),
(2, 'designs/living_room_axlNDO9.jpeg', 'Living Room Design', 'living room is a great design which attracts guests', 3, '2025-02-13 08:25:44.984277', 0.00, '1', 'Modern', 0.00, '[]'),
(3, 'designs/Bedroom-Design_PfHW0e9.jpeg', 'Bedroom Design', 'Bedroom designs are really attractive and mind blowing', 3, '2025-02-13 08:34:59.147571', 0.00, '1', 'Modern', 0.00, '[]'),
(4, 'designs/Bathroom-Design_Wme5AUq.jpeg', 'Bathroom Design', 'bathroom designs are fantastic mind blowing', 3, '2025-02-13 08:36:25.129721', 0.00, '1', 'Modern', 0.00, '[]'),
(5, 'designs/Kitchen-Design_CuD8b0O.jpeg', 'kitchen design', 'kitchen is a place where we cook and cooking is also a part of love which we show us to our own family and kitchen is a place makes the family more colorful and wonderful like the kitchen designs', 3, '2025-02-13 08:40:41.897859', 0.00, '1', 'Modern', 0.00, '[]'),
(6, 'design_images/living_room.jpeg', 'Hungarian Hill', 'hungarian hill is a modern type of living room ', 3, '2025-02-18 04:05:51.072158', 3000.00, 'Living Room', 'Modern', 2000.00, '[]'),
(7, 'design_images/Kitchen-Design.jpeg', 'Kitchen de Italiano', 'Kitchen de Italiano is a modern type of kitchen design which comes with attractive outlooks', 3, '2025-02-18 04:25:29.375638', 5000.00, 'Kitchen', 'Modern', 2000.00, '[]'),
(8, 'design_images/Bathroom-Design.jpeg', 'Shower Hill', 'Shower Hill is a type of modern bathroom design', 3, '2025-02-18 04:29:00.158956', 6000.00, 'Bathroom', 'Modern', 3000.00, '[]');

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_designer`
--

CREATE TABLE `interiorapp_designer` (
  `id` bigint(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(128) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interiorapp_designer`
--

INSERT INTO `interiorapp_designer` (`id`, `full_name`, `email`, `phone`, `username`, `password`, `user_id`) VALUES
(1, '', 'kiran@gmail.com', '', 'kiran', 'kiran@123', NULL),
(3, '', 'jeswin@gmail.com', '', 'jeswin', 'jeswin@123', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_favorite`
--

CREATE TABLE `interiorapp_favorite` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `design_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interiorapp_favorite`
--

INSERT INTO `interiorapp_favorite` (`id`, `created_at`, `design_id`, `user_id`) VALUES
(5, '2025-02-13 08:42:14.582763', 5, 1),
(6, '2025-02-14 10:02:27.406405', 2, 1),
(8, '2025-02-18 06:09:08.621448', 7, 1);

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_feedback`
--

CREATE TABLE `interiorapp_feedback` (
  `id` bigint(20) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_order`
--

CREATE TABLE `interiorapp_order` (
  `id` bigint(20) NOT NULL,
  `payment_id` varchar(100) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  `contact_number` varchar(15) DEFAULT NULL,
  `razorpay_order_id` varchar(100) DEFAULT NULL,
  `shipping_address` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interiorapp_order`
--

INSERT INTO `interiorapp_order` (`id`, `payment_id`, `amount`, `status`, `created_at`, `user_id`, `contact_number`, `razorpay_order_id`, `shipping_address`) VALUES
(1, 'pay_Pv9VOwfYHOJlfF', 70050.00, 'Completed', '2025-02-13 09:54:02.490798', 1, NULL, 'order_Pv9V9TEKVgbnbB', NULL),
(2, 'pay_Pv9aegHo84jiUF', 50.00, 'Completed', '2025-02-13 09:59:01.288998', 1, NULL, 'order_Pv9aM09Ya6NtSz', NULL),
(3, 'pay_Pv9lvzKxhFpaoo', 2050.00, 'Completed', '2025-02-13 10:09:41.430918', 1, NULL, 'order_Pv9llQ3p1zIWRv', NULL),
(4, 'pay_Pv9y8j2Z9CtNGX', 6050.00, 'Completed', '2025-02-13 10:21:14.551822', 1, NULL, 'order_Pv9xuN8zEIbJa0', NULL),
(5, 'pay_PvA40qvZiPMqkJ', 3050.00, 'Completed', '2025-02-13 10:26:48.022546', 1, NULL, 'order_PvA3qw1YQcbQlW', NULL),
(6, 'pay_PvAQ0sRZ6LPMrs', 8050.00, 'Completed', '2025-02-13 10:47:37.952842', 1, NULL, 'order_PvAPnZLfmTuC7W', NULL),
(7, 'pay_PvRZPcTU5W6QDF', 3050.00, 'Completed', '2025-02-14 03:34:20.807340', 1, NULL, 'order_PvRZCmYDnlOr1J', NULL),
(8, 'pay_PvRaaCROxlL9Le', 6050.00, 'Completed', '2025-02-14 03:35:27.623078', 1, NULL, 'order_PvRaPWIPlVWDVh', NULL),
(9, 'pay_PvRg3XmbML2vJA', 3050.00, 'Completed', '2025-02-14 03:40:38.208478', 1, NULL, 'order_PvRfo1nRm9ifgo', NULL),
(10, 'pay_PvRj7znLKPSQRI', 2050.00, 'Completed', '2025-02-14 03:43:32.586393', 1, NULL, 'order_PvRit8sAPa5Qn7', NULL),
(11, 'pay_PvSbE8roMMPQ0Z', 3050.00, 'Completed', '2025-02-14 04:34:45.749558', 1, NULL, 'order_PvSb2VYBqV6jvO', NULL),
(12, 'pay_PvSfu53iP6QlIX', 3050.00, 'Completed', '2025-02-14 04:39:11.179418', 1, NULL, 'order_PvSfgnvLxnumtY', NULL),
(13, 'pay_PvSgXvBKfoCLB6', 2050.00, 'Completed', '2025-02-14 04:39:47.732375', 1, NULL, 'order_PvSgNKaZ71rjWU', NULL),
(14, 'pay_PvSoEnhOZDI6tj', 3050.00, 'Completed', '2025-02-14 04:47:04.520486', 1, NULL, 'order_PvSo3g0SZGimvs', NULL),
(15, 'pay_PvSqUAjwMjBlUL', 5050.00, 'Completed', '2025-02-14 04:49:12.172121', 1, NULL, 'order_PvSqK8d0lYnGvK', NULL),
(16, 'pay_PvSwNcZ2OlQBJx', 3050.00, 'Completed', '2025-02-14 04:54:47.345924', 1, NULL, 'order_PvSw9GkPRZ3Ghs', NULL),
(17, 'pay_PvSxBcoTsFAtGt', 2050.00, 'Completed', '2025-02-14 04:55:32.790808', 1, NULL, 'order_PvSwz6zPQEvwV6', NULL),
(18, 'pay_PvTS4osHzblMEG', 3050.00, 'Completed', '2025-02-14 05:24:47.463134', 1, NULL, 'order_PvTRv1ir56fVV8', NULL),
(19, 'pay_PvTc75VEWIPtER', 6050.00, 'Completed', '2025-02-14 05:34:17.548400', 1, NULL, 'order_PvTbsm9CvZfsGG', NULL),
(20, 'pay_PvTclnHnAbinG9', 3050.00, 'Completed', '2025-02-14 05:34:54.754031', 1, NULL, 'order_PvTcbxlcDu7jOY', NULL),
(21, 'pay_PvTgGiFSssFSCB', 5050.00, 'Completed', '2025-02-14 05:38:13.431340', 1, NULL, 'order_PvTg5snDUwS1MS', NULL),
(22, 'pay_PvTk7ieLm2I1Uy', 3050.00, 'Completed', '2025-02-14 05:41:52.562845', 1, NULL, 'order_PvTjwr9I5WWRJ7', NULL),
(23, 'pay_PvTm0WT8z7JWTb', 9050.00, 'Completed', '2025-02-14 05:43:39.966855', 1, NULL, 'order_PvTlqMhOurjbjp', NULL),
(24, 'pay_PvWe3hR76gy9kz', 292050.00, 'Completed', '2025-02-14 08:32:12.822871', 1, NULL, 'order_PvWdiFl21Eh5R9', NULL),
(25, 'pay_PvWfSItMaNHomq', 2050.00, 'Completed', '2025-02-14 08:33:32.165354', 1, NULL, 'order_PvWfEuQGHtF7dC', NULL),
(26, 'pay_PvXJeKCenups8a', 2050.00, 'Completed', '2025-02-14 09:11:38.255888', 1, NULL, 'order_PvXJRJglDGxlkm', NULL),
(27, 'pay_PvYK0mzJcM4dmK', 8050.00, 'Completed', '2025-02-14 10:10:37.195013', 1, NULL, 'order_PvYJq4OjPD6tF3', NULL),
(28, 'pay_PvYMZ2WNC8LqR6', 5050.00, 'Completed', '2025-02-14 10:13:02.285665', 1, NULL, 'order_PvYMOINmnBGdvD', NULL),
(29, 'pay_PvYOhbkDikaRio', 2050.00, 'Completed', '2025-02-14 10:15:03.412415', 1, NULL, 'order_PvYOVxImfslUCL', NULL),
(30, 'pay_PwdHMIAzp4dIbb', 3050.00, 'Completed', '2025-02-17 03:40:33.675940', 1, NULL, 'order_PwdF9xT4HGKWGW', NULL),
(31, 'pay_PwgDrDOVPweEuT', 8050.00, 'Completed', '2025-02-17 06:33:20.870984', 1, NULL, 'order_PwgDctXNjKhyyx', NULL),
(32, 'pay_PwgcCzVkU6mpub', 3050.00, 'Completed', '2025-02-17 06:56:22.602561', 1, NULL, 'order_Pwgc3LGsf3h7Xg', NULL),
(33, 'pay_PwgfCtWDUuFcCW', 3050.00, 'Completed', '2025-02-17 06:59:12.922790', 1, NULL, 'order_Pwgf35iJBPJqLz', NULL),
(34, 'pay_PwiGQBSys79uKj', 2050.00, 'Completed', '2025-02-17 08:33:08.445272', 1, NULL, 'order_PwiFpoHDoLNicZ', NULL),
(35, 'pay_Px2zVUdhZjuWEe', 8050.00, 'Completed', '2025-02-18 04:49:42.152945', 1, NULL, 'order_Px2zLIyVvkEK2X', NULL),
(36, 'pay_Px3OM4FZHUaP7F', 3050.00, 'Completed', '2025-02-18 05:13:13.221645', 1, NULL, 'order_Px3OBWHjTpFKGw', NULL),
(37, 'pay_Px3iPxGXNoaiLu', 3050.00, 'Completed', '2025-02-18 05:32:12.716230', 1, NULL, 'order_Px3iH3vqpP1EMx', NULL),
(38, 'pay_PxWfVYNI8QdQej', 3050.00, 'Completed', '2025-02-19 09:51:32.528663', 1, NULL, 'order_PxWf26u8bnd1hG', NULL),
(39, 'pay_PxWinlNCJhdL0O', 2050.00, 'Completed', '2025-02-19 09:54:39.531651', 1, NULL, 'order_PxWic27u0bGhpm', NULL),
(40, 'pay_PxWltvDzUrWp53', 2050.00, 'Completed', '2025-02-19 09:57:35.501161', 1, NULL, 'order_PxWlhVaSRCuSpu', NULL),
(41, 'pay_PxWpS6511mlMjv', 3050.00, 'Completed', '2025-02-19 10:00:57.367830', 1, NULL, 'order_PxWpIu570m93Cb', NULL),
(42, 'pay_PxWs3Y9DBaP2Bz', 3050.00, 'Completed', '2025-02-19 10:03:25.196845', 1, NULL, 'order_PxWrre1JHbU86G', NULL),
(43, 'pay_PxWxHXLOBahZ7p', 3050.00, 'Completed', '2025-02-19 10:08:21.979502', 1, NULL, 'order_PxWx6wbsuiivFo', NULL),
(44, 'pay_PxX2iH1svpDD4O', 8050.00, 'Completed', '2025-02-19 10:13:30.889359', 1, NULL, 'order_PxX2WpTSEKCoFZ', NULL),
(45, 'pay_PxX6XNueOxrZEM', 2050.00, 'Completed', '2025-02-19 10:17:08.281941', 1, NULL, 'order_PxX6KyUxPSs5tY', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_orderitem`
--

CREATE TABLE `interiorapp_orderitem` (
  `id` bigint(20) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL CHECK (`quantity` >= 0),
  `price` decimal(10,2) NOT NULL,
  `order_id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interiorapp_orderitem`
--

INSERT INTO `interiorapp_orderitem` (`id`, `quantity`, `price`, `order_id`, `product_id`) VALUES
(1, 3, 3000.00, 1, 1),
(2, 17, 3000.00, 1, 3),
(3, 5, 2000.00, 1, 2),
(4, 1, 2000.00, 3, 2),
(5, 2, 3000.00, 4, 3),
(6, 1, 3000.00, 5, 3),
(7, 2, 3000.00, 6, 1),
(8, 1, 2000.00, 6, 2),
(9, 1, 3000.00, 7, 3),
(10, 2, 3000.00, 8, 3),
(11, 1, 3000.00, 9, 3),
(12, 1, 2000.00, 10, 2),
(13, 1, 3000.00, 11, 3),
(14, 1, 3000.00, 12, 3),
(15, 1, 2000.00, 13, 2),
(16, 1, 3000.00, 14, 3),
(17, 1, 2000.00, 15, 2),
(18, 1, 3000.00, 15, 1),
(19, 1, 3000.00, 16, 3),
(20, 1, 2000.00, 17, 2),
(21, 1, 3000.00, 18, 3),
(22, 2, 3000.00, 19, 3),
(23, 1, 3000.00, 20, 3),
(24, 1, 2000.00, 21, 2),
(25, 1, 3000.00, 21, 3),
(26, 1, 3000.00, 22, 3),
(27, 3, 3000.00, 23, 3),
(28, 2, 3000.00, 24, 3),
(29, 16, 3000.00, 24, 1),
(30, 119, 2000.00, 24, 2),
(31, 1, 2000.00, 25, 2),
(32, 1, 2000.00, 26, 2),
(33, 4, 2000.00, 27, 2),
(34, 1, 2000.00, 28, 2),
(35, 1, 3000.00, 28, 1),
(36, 1, 2000.00, 29, 2),
(37, 1, 3000.00, 30, 1),
(38, 1, 2000.00, 31, 2),
(39, 2, 3000.00, 31, 1),
(40, 1, 3000.00, 32, 1),
(41, 1, 3000.00, 33, 1),
(42, 1, 2000.00, 34, 2),
(43, 1, 2000.00, 35, 2),
(44, 2, 3000.00, 35, 1),
(45, 1, 3000.00, 36, 1),
(46, 1, 3000.00, 37, 1),
(47, 1, 3000.00, 38, 3),
(48, 1, 2000.00, 39, 2),
(49, 1, 2000.00, 40, 2),
(50, 1, 3000.00, 41, 1),
(51, 1, 3000.00, 42, 1),
(52, 1, 3000.00, 43, 1),
(53, 1, 2000.00, 44, 2),
(54, 1, 3000.00, 44, 1),
(55, 1, 3000.00, 44, 3),
(56, 1, 2000.00, 45, 2);

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_portfolio`
--

CREATE TABLE `interiorapp_portfolio` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_product`
--

CREATE TABLE `interiorapp_product` (
  `id` bigint(20) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int(10) UNSIGNED NOT NULL CHECK (`stock` >= 0),
  `image` varchar(100) DEFAULT NULL,
  `category` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `seller_id` bigint(20) NOT NULL,
  `style` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interiorapp_product`
--

INSERT INTO `interiorapp_product` (`id`, `product_name`, `description`, `price`, `stock`, `image`, `category`, `created_at`, `updated_at`, `seller_id`, `style`) VALUES
(1, 'Home decor ', 'Home decor is a great product', 3000.00, 12, 'product_images/hanging_decor_item_7eb1dQp.jpeg', '', '2025-02-13 04:57:58.564656', '2025-02-18 04:30:19.134252', 1, 'Modern'),
(2, 'Sofa', 'sofa is a great product', 2000.00, 12, 'product_images/sofa_QdX3tMB.jpeg', '', '2025-02-13 06:01:36.964091', '2025-02-14 04:34:51.141901', 1, 'Modern'),
(3, 'Chair ', 'chair is a great product', 3000.00, 10, 'product_images/chair_SAespkD.jpeg', '', '2025-02-13 06:02:35.661878', '2025-02-18 09:29:03.010033', 1, 'Modern'),
(4, 'Bulb', 'nsjjscjsjcjcjcckkcqjcqwc', 290.00, 22, 'product_images/Crompton_bulb_K0intin.jpeg', '', '2025-02-20 05:59:39.500139', '2025-02-20 05:59:39.502664', 1, 'Modern'),
(5, 'Home Decor', 'ghkjghcghfdgfhdmcfh', 600.00, 4, 'product_images/hanging_decor_item_ZaIm3Nz.jpeg', 'Decor_Items', '2025-02-20 06:55:18.401907', '2025-02-20 06:55:18.401907', 1, 'Modern'),
(6, 'Bulb', 'gfgfdagfdsghjfhgsfjaghsfhgdsfsgdjfdfas', 200.00, 12, 'product_images/MI_smart_LED_color_bulb_8qrUzzg.jpeg', 'Lighting', '2025-02-20 06:56:41.206728', '2025-02-20 06:56:41.206728', 1, 'Modern'),
(7, 'MI LED Bulb', 'An \"ML bulb\" most likely refers to a light bulb that utilizes machine learning technology, potentially allowing for features like adaptive brightness based on ambient light conditions, energy usage monitoring, or even personalized lighting settings, all controlled through a smart home system or app; essentially, a \"smart bulb\" with advanced machine learning capabilities to optimize lighting based on user behavior and environment. ', 350.00, 11, 'product_images/mi_led.jpg', 'Lighting', '2025-02-20 09:23:08.275065', '2025-02-20 09:23:08.275065', 1, 'Modern');

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_seller`
--

CREATE TABLE `interiorapp_seller` (
  `id` bigint(20) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `company` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interiorapp_seller`
--

INSERT INTO `interiorapp_seller` (`id`, `username`, `email`, `name`, `phone`, `company`, `password`, `is_active`, `is_admin`) VALUES
(1, 'Arunroy', 'arun@gmail.com', 'Arun', '9089786755', 'Bata', 'Arunroy@123', 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `interiorapp_userprofile`
--

CREATE TABLE `interiorapp_userprofile` (
  `id` bigint(20) NOT NULL,
  `bio` longtext NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `phone` varchar(15) NOT NULL,
  `is_designer` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interiorapp_userprofile`
--

INSERT INTO `interiorapp_userprofile` (`id`, `bio`, `profile_picture`, `phone`, `is_designer`, `user_id`) VALUES
(1, '', 'profile_pics/designer2.jpg', '9098878909', 1, 2),
(2, '', 'profile_pics/designer1.jpg', '8909678978', 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_association`
--

CREATE TABLE `social_auth_association` (
  `id` bigint(20) NOT NULL,
  `server_url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` varchar(255) NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_code`
--

CREATE TABLE `social_auth_code` (
  `id` bigint(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `code` varchar(32) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_nonce`
--

CREATE TABLE `social_auth_nonce` (
  `id` bigint(20) NOT NULL,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(65) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_partial`
--

CREATE TABLE `social_auth_partial` (
  `id` bigint(20) NOT NULL,
  `token` varchar(32) NOT NULL,
  `next_step` smallint(5) UNSIGNED NOT NULL CHECK (`next_step` >= 0),
  `backend` varchar(32) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`data`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_usersocialauth`
--

CREATE TABLE `social_auth_usersocialauth` (
  `id` bigint(20) NOT NULL,
  `provider` varchar(32) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `extra_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`extra_data`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `interiorapp_budgetallocation`
--
ALTER TABLE `interiorapp_budgetallocation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InteriorApp_budgetal_budget_plan_id_725cc173_fk_InteriorA` (`budget_plan_id`);

--
-- Indexes for table `interiorapp_budgetplan`
--
ALTER TABLE `interiorapp_budgetplan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InteriorApp_budgetplan_user_id_bdf9976c_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `interiorapp_bundledeal`
--
ALTER TABLE `interiorapp_bundledeal`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `interiorapp_bundledeal_products`
--
ALTER TABLE `interiorapp_bundledeal_products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `InteriorApp_bundledeal_p_bundledeal_id_product_id_055d9ce8_uniq` (`bundledeal_id`,`product_id`),
  ADD KEY `InteriorApp_bundlede_product_id_cb69dd67_fk_InteriorA` (`product_id`);

--
-- Indexes for table `interiorapp_cart`
--
ALTER TABLE `interiorapp_cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InteriorApp_cart_user_id_be73a496_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `interiorapp_cartitem`
--
ALTER TABLE `interiorapp_cartitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InteriorApp_cartitem_cart_id_7c5004ed_fk_InteriorApp_cart_id` (`cart_id`),
  ADD KEY `InteriorApp_cartitem_product_id_da9c07e3_fk_InteriorA` (`product_id`);

--
-- Indexes for table `interiorapp_design`
--
ALTER TABLE `interiorapp_design`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InteriorApp_design_designer_id_efb36a37_fk_InteriorA` (`designer_id`);

--
-- Indexes for table `interiorapp_designer`
--
ALTER TABLE `interiorapp_designer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `interiorapp_favorite`
--
ALTER TABLE `interiorapp_favorite`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `InteriorApp_favorite_user_id_design_id_aa81d4e2_uniq` (`user_id`,`design_id`),
  ADD KEY `InteriorApp_favorite_design_id_fa63d4a6_fk_InteriorApp_design_id` (`design_id`);

--
-- Indexes for table `interiorapp_feedback`
--
ALTER TABLE `interiorapp_feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InteriorApp_feedback_user_id_695ac61d_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `interiorapp_order`
--
ALTER TABLE `interiorapp_order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InteriorApp_order_user_id_dcbc0779_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `interiorapp_orderitem`
--
ALTER TABLE `interiorapp_orderitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InteriorApp_orderitem_order_id_3f69c7ca_fk_InteriorApp_order_id` (`order_id`),
  ADD KEY `InteriorApp_orderite_product_id_73c0dadb_fk_InteriorA` (`product_id`);

--
-- Indexes for table `interiorapp_portfolio`
--
ALTER TABLE `interiorapp_portfolio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InteriorApp_portfolio_user_id_e21e7252_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `interiorapp_product`
--
ALTER TABLE `interiorapp_product`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InteriorApp_product_seller_id_362dae11_fk_InteriorApp_seller_id` (`seller_id`);

--
-- Indexes for table `interiorapp_seller`
--
ALTER TABLE `interiorapp_seller`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `interiorapp_userprofile`
--
ALTER TABLE `interiorapp_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `social_auth_association`
--
ALTER TABLE `social_auth_association`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_association_server_url_handle_078befa2_uniq` (`server_url`,`handle`);

--
-- Indexes for table `social_auth_code`
--
ALTER TABLE `social_auth_code`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_code_email_code_801b2d02_uniq` (`email`,`code`),
  ADD KEY `social_auth_code_code_a2393167` (`code`),
  ADD KEY `social_auth_code_timestamp_176b341f` (`timestamp`);

--
-- Indexes for table `social_auth_nonce`
--
ALTER TABLE `social_auth_nonce`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_nonce_server_url_timestamp_salt_f6284463_uniq` (`server_url`,`timestamp`,`salt`);

--
-- Indexes for table `social_auth_partial`
--
ALTER TABLE `social_auth_partial`
  ADD PRIMARY KEY (`id`),
  ADD KEY `social_auth_partial_token_3017fea3` (`token`),
  ADD KEY `social_auth_partial_timestamp_50f2119f` (`timestamp`);

--
-- Indexes for table `social_auth_usersocialauth`
--
ALTER TABLE `social_auth_usersocialauth`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_usersocialauth_provider_uid_e6b5e668_uniq` (`provider`,`uid`),
  ADD KEY `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` (`user_id`),
  ADD KEY `social_auth_usersocialauth_uid_796e51dc` (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=105;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT for table `interiorapp_budgetallocation`
--
ALTER TABLE `interiorapp_budgetallocation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `interiorapp_budgetplan`
--
ALTER TABLE `interiorapp_budgetplan`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `interiorapp_bundledeal`
--
ALTER TABLE `interiorapp_bundledeal`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `interiorapp_bundledeal_products`
--
ALTER TABLE `interiorapp_bundledeal_products`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `interiorapp_cart`
--
ALTER TABLE `interiorapp_cart`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `interiorapp_cartitem`
--
ALTER TABLE `interiorapp_cartitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `interiorapp_design`
--
ALTER TABLE `interiorapp_design`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `interiorapp_designer`
--
ALTER TABLE `interiorapp_designer`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `interiorapp_favorite`
--
ALTER TABLE `interiorapp_favorite`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `interiorapp_feedback`
--
ALTER TABLE `interiorapp_feedback`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `interiorapp_order`
--
ALTER TABLE `interiorapp_order`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `interiorapp_orderitem`
--
ALTER TABLE `interiorapp_orderitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `interiorapp_portfolio`
--
ALTER TABLE `interiorapp_portfolio`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `interiorapp_product`
--
ALTER TABLE `interiorapp_product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `interiorapp_seller`
--
ALTER TABLE `interiorapp_seller`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `interiorapp_userprofile`
--
ALTER TABLE `interiorapp_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `social_auth_association`
--
ALTER TABLE `social_auth_association`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_code`
--
ALTER TABLE `social_auth_code`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_nonce`
--
ALTER TABLE `social_auth_nonce`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_partial`
--
ALTER TABLE `social_auth_partial`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_usersocialauth`
--
ALTER TABLE `social_auth_usersocialauth`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `interiorapp_budgetallocation`
--
ALTER TABLE `interiorapp_budgetallocation`
  ADD CONSTRAINT `InteriorApp_budgetal_budget_plan_id_725cc173_fk_InteriorA` FOREIGN KEY (`budget_plan_id`) REFERENCES `interiorapp_budgetplan` (`id`);

--
-- Constraints for table `interiorapp_budgetplan`
--
ALTER TABLE `interiorapp_budgetplan`
  ADD CONSTRAINT `InteriorApp_budgetplan_user_id_bdf9976c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `interiorapp_bundledeal_products`
--
ALTER TABLE `interiorapp_bundledeal_products`
  ADD CONSTRAINT `InteriorApp_bundlede_bundledeal_id_0e15e33c_fk_InteriorA` FOREIGN KEY (`bundledeal_id`) REFERENCES `interiorapp_bundledeal` (`id`),
  ADD CONSTRAINT `InteriorApp_bundlede_product_id_cb69dd67_fk_InteriorA` FOREIGN KEY (`product_id`) REFERENCES `interiorapp_product` (`id`);

--
-- Constraints for table `interiorapp_cart`
--
ALTER TABLE `interiorapp_cart`
  ADD CONSTRAINT `InteriorApp_cart_user_id_be73a496_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `interiorapp_cartitem`
--
ALTER TABLE `interiorapp_cartitem`
  ADD CONSTRAINT `InteriorApp_cartitem_cart_id_7c5004ed_fk_InteriorApp_cart_id` FOREIGN KEY (`cart_id`) REFERENCES `interiorapp_cart` (`id`),
  ADD CONSTRAINT `InteriorApp_cartitem_product_id_da9c07e3_fk_InteriorA` FOREIGN KEY (`product_id`) REFERENCES `interiorapp_product` (`id`);

--
-- Constraints for table `interiorapp_design`
--
ALTER TABLE `interiorapp_design`
  ADD CONSTRAINT `InteriorApp_design_designer_id_efb36a37_fk_InteriorA` FOREIGN KEY (`designer_id`) REFERENCES `interiorapp_designer` (`id`);

--
-- Constraints for table `interiorapp_designer`
--
ALTER TABLE `interiorapp_designer`
  ADD CONSTRAINT `InteriorApp_designer_user_id_f131e74e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `interiorapp_favorite`
--
ALTER TABLE `interiorapp_favorite`
  ADD CONSTRAINT `InteriorApp_favorite_design_id_fa63d4a6_fk_InteriorApp_design_id` FOREIGN KEY (`design_id`) REFERENCES `interiorapp_design` (`id`),
  ADD CONSTRAINT `InteriorApp_favorite_user_id_32307446_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `interiorapp_feedback`
--
ALTER TABLE `interiorapp_feedback`
  ADD CONSTRAINT `InteriorApp_feedback_user_id_695ac61d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `interiorapp_order`
--
ALTER TABLE `interiorapp_order`
  ADD CONSTRAINT `InteriorApp_order_user_id_dcbc0779_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `interiorapp_orderitem`
--
ALTER TABLE `interiorapp_orderitem`
  ADD CONSTRAINT `InteriorApp_orderite_product_id_73c0dadb_fk_InteriorA` FOREIGN KEY (`product_id`) REFERENCES `interiorapp_product` (`id`),
  ADD CONSTRAINT `InteriorApp_orderitem_order_id_3f69c7ca_fk_InteriorApp_order_id` FOREIGN KEY (`order_id`) REFERENCES `interiorapp_order` (`id`);

--
-- Constraints for table `interiorapp_portfolio`
--
ALTER TABLE `interiorapp_portfolio`
  ADD CONSTRAINT `InteriorApp_portfolio_user_id_e21e7252_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `interiorapp_product`
--
ALTER TABLE `interiorapp_product`
  ADD CONSTRAINT `InteriorApp_product_seller_id_362dae11_fk_InteriorApp_seller_id` FOREIGN KEY (`seller_id`) REFERENCES `interiorapp_seller` (`id`);

--
-- Constraints for table `interiorapp_userprofile`
--
ALTER TABLE `interiorapp_userprofile`
  ADD CONSTRAINT `InteriorApp_userprofile_user_id_086249fe_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `social_auth_usersocialauth`
--
ALTER TABLE `social_auth_usersocialauth`
  ADD CONSTRAINT `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
