-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: SIRS26SCOREBOARD
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
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
  `username` varchar(100) NOT NULL,
  `group_id` int(6) NOT NULL,
  `points` int(15) DEFAULT '0',
  `num_vul` int(10) DEFAULT '0',
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`username`)
) ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Scoreboard`
--

LOCK TABLES `Scoreboard` WRITE;
/*!40000 ALTER TABLE `Scoreboard` DISABLE KEYS */;
INSERT INTO `Scoreboard` VALUES ('Admin',1,0,0,'2019-11-15 23:22:47'),('Kevin',1,0,0,'2019-11-15 23:23:47'),('TiagoM',1,0,0,'2019-11-15 23:24:47'),('TiagoS',1,0,0,'2019-11-15 23:25:47'), ('Admin2',2,0,0,'2019-11-15 23:26:47'),('Kevin2',2,0,0,'2019-11-15 23:27:47'),('TiagoM2',2,0,0,'2019-11-15 23:28:47'),('TiagoS2',2,0,0,'2019-11-15 23:29:47');
/*!40000 ALTER TABLE `Scoreboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Vulnerability`
--

DROP TABLE IF EXISTS `Vulnerability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Vulnerability` (
  `username` varchar(100) NOT NULL,
  `fingerprint` varchar(500) NOT NULL,
  `name_vul` varchar(100) NOT NULL,
  `insert_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`username`, `fingerprint`, `name_vul` )
) ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Vulnerability`
--

LOCK TABLES `Vulnerability` WRITE;
/*!40000 ALTER TABLE `Vulnerability` DISABLE KEYS */;
INSERT INTO `Vulnerability` VALUES ('TiagoM','b660931c82376a6bfc852930ea1c6c0d451069baec3c1f51cf15b07982091496be27212030d88c182685c80229232e41f738094b4424eec2c104061233c61aff','BufferOverflow','2019-11-15 23:18:47'),('TiagoM','b660931c82376a6bfc852930ea1c6c0d451069baec3c1f51cf15b07982091496be27212030d88c182685c80229232e41f738094b4424eec2c104061233c61aff','RaceCondition','2019-11-16 23:18:47');
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

-- Dump completed on 2019-11-15 18:21:58
