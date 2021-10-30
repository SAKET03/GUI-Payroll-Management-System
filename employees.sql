-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 10, 2021 at 06:40 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `emp_id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contact_no` varchar(25) NOT NULL,
  `address` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(100) NOT NULL,
  `bank_name` varchar(100) NOT NULL,
  `account_no` varchar(100) NOT NULL,
  `department` varchar(100) NOT NULL,
  `position` varchar(100) NOT NULL,
  `basic_salary` double NOT NULL,
  `hra` double NOT NULL,
  `oa` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`emp_id`, `name`, `email`, `contact_no`, `address`, `city`, `state`, `dob`, `gender`, `bank_name`, `account_no`, `department`, `position`, `basic_salary`, `hra`, `oa`) VALUES
('emp_1029', 'Rudy J Wooten', '8y5j6itqtk@temporary-mail.net', '2517431632', '666 Joyce Street', 'Monroeville', 'Alabama', '1994-08-18', 'Male', 'Rustler Steak House', '5420222376742723', 'Catering', 'Full-time', 15000, 5000, 5100),
('emp_1082', 'Eric J Clark', 'jhuwp5sr2g@temporary-mail.net', '4806613625', '4077 Dye Street', 'Scottsdale', 'Arizona', '1986-03-16', 'Male', 'Angel\'s', '4532175916550071', 'Catering', 'Part-time', 15000, 5000, 5100),
('emp_1253', 'Sherrie K Phillips', 'iw57q8yo32@temporary-mail.net', '3363948941', '3095 Havanna Street', 'Greensboro', 'North Carolina', '1986-03-28', 'Female', 'Morville', '5481458267365275', 'Security', 'Cheif', 22000, 12000, 2000),
('emp_1282', 'Shawn T Cornish', 'kieran1983@yahoo.com', '1630756658', '4033 Concord Street', 'GRAND LEDGE', 'Michigan', '1963-09-04', 'Male', 'Weathervane', '4485324009812058', 'PR', 'HOD', 24000, 14000, 4000),
('emp_1338', 'James T Moore', 'dyoohzmj63c@temporary-mail.net', '9095023632', '3394 Brooke Street', 'CORONA', 'California', '1986-10-12', 'Male', 'Blue Boar Cafeterias', '4916565641578429', 'Creatives', 'Intern', 11000, 4000, 1100),
('emp_1346', 'Sharon R Southard', 'jjkuo3odhmn@temporary-mail.net', '8603638581', '2858 Foley Street', 'HARTFORD', 'Connecticut', '1989-04-23', 'Female', 'Dreamscape Garden Care', '4929395138909951', 'HR', 'HOD', 25000, 15000, 5000),
('emp_1357', 'Josephine A Jones', 'cbc8pm1yk3p@temporary-mail.net', '5208874611', '813 Polk Street', 'Tucson', 'Arizona', '1957-06-19', 'Female', 'Avant Garde Appraisal Group', '5456700108736482', 'Marketing', 'HOD', 22000, 12000, 2000),
('emp_1375', 'Harry A Syed', 'mle17unmtvr@temporary-mail.net', '3309602612', '3816 Horner Street', 'Wooster', 'Ohio', '1996-01-26', 'Male', 'Burstein-Applebee', '5232279863906995', 'Tech', 'Intern', 12000, 2000, 2100),
('emp_1436', 'Dona G Garcia', '1ecc5chm47h@temporary-mail.net', '5204059854', '2388 Keyser Ridge Road', 'North Carolina', 'Greensboro', '1964-07-09', 'Female', 'Steak and Ale', '5270598872210187', 'Tech', 'HOD', 27000, 17000, 7000),
('emp_1720', 'Jeffrey M Young', 'c3b0xc5ixpb@temporary-mail.net', '4028564193', '2133 Bungalow Road', 'Brock', 'Nebraska', '1986-08-10', 'Male', 'Checker Auto Parts', '4485382479201400', 'Logistics', 'Contractor', 21000, 11000, 1000);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`emp_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
