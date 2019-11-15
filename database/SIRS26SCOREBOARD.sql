-- MySQL dump 10.17  Distrib 10.3.18-MariaDB, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: SIRS26SCOREBOARD
-- ------------------------------------------------------
-- Server version	10.3.18-MariaDB-1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Scoreboard`
--

DROP TABLE IF EXISTS `Scoreboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Scoreboard` (
  `user_id` int(6) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `group_id` int(6) NOT NULL,
  `points` int(15) DEFAULT 0,
  `num_vul` int(10) DEFAULT 0,
  `last_update` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Scoreboard`
--

LOCK TABLES `Scoreboard` WRITE;
/*!40000 ALTER TABLE `Scoreboard` DISABLE KEYS */;
INSERT INTO `Scoreboard` VALUES (2,'Kevin',1,0,0,'2019-11-14 15:38:49'),(3,'TiagoM',1,0,0,'2019-11-14 15:38:49'),(4,'TiagoS',1,0,0,'2019-11-14 15:38:49'),(6,'Kevin2',2,0,0,'2019-11-14 15:38:49'),(7,'TiagoM2',2,0,0,'2019-11-14 15:38:49'),(8,'TiagoS2',2,0,0,'2019-11-14 15:38:50');
/*!40000 ALTER TABLE `Scoreboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Vulnerability`
--

DROP TABLE IF EXISTS `Vulnerability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Vulnerability` (
  `id_vul` int(6) NOT NULL AUTO_INCREMENT,
  `user_id` int(6) NOT NULL,
  `fingerprint` varchar(30) NOT NULL,
  `name_vul` varchar(60) NOT NULL,
  `insert_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id_vul`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Vulnerability`
--

LOCK TABLES `Vulnerability` WRITE;
/*!40000 ALTER TABLE `Vulnerability` DISABLE KEYS */;
/*!40000 ALTER TABLE `Vulnerability` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-14 15:39:15
