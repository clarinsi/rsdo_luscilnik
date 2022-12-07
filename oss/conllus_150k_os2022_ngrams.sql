CREATE DATABASE  IF NOT EXISTS `conllus_150k` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `conllus_150k`;
-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 164.8.252.72    Database: conllus_150k
-- ------------------------------------------------------
-- Server version	5.5.5-10.5.4-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `os2022_ngrams`
--

DROP TABLE IF EXISTS `os2022_ngrams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `os2022_ngrams` (
  `file_id` int(11) NOT NULL,
  `sent_id` float(12,10) NOT NULL,
  `ngram_len` int(11) NOT NULL,
  `frequency_g_t` int(11) NOT NULL,
  `gram_text` text CHARACTER SET utf8 COLLATE utf8_slovenian_ci NOT NULL,
  `lemma_text` text CHARACTER SET utf8 COLLATE utf8_slovenian_ci NOT NULL,
  `upos_text` text CHARACTER SET utf8 COLLATE utf8_slovenian_ci NOT NULL,
  `xpos_text` text CHARACTER SET utf8 COLLATE utf8_slovenian_ci NOT NULL
) ENGINE=Columnstore DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-07  5:58:52
