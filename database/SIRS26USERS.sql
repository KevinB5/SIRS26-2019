-- MySQL dump 10.17  Distrib 10.3.18-MariaDB, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: SIRS26USERS
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
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `user_id` int(6) NOT NULL AUTO_INCREMENT,
  `auth_type` int(6) NOT NULL,
  `group_id` int(6) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`user_id`)
) ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,1,1,'Admin','$2b$14$hCxmngO9Fnz9t4Rd5AKnCuD9Iy3ctlBm5xMU.jhQoVPE1dP6GKzG2','2019-11-13 19:14:05'),(2,2,1,'Kevin','$2b$14$Ru6ojLgvdA5s456IeyNf9e.8CCret718RtXmqRkrVQDkH8iDDV7qy','2019-11-13 19:15:05'),(3,2,1,'TiagoM','$2b$14$zwheXPO9IFicA4riui7kJ.vdNrIhT8ysQKzqWMHSF/5CnYl/1J4ZW','2019-11-13 19:16:05'),(4,2,1,'TiagoS','$2b$14$P67CRnQgKWaqmVfrDPMFzOMqZALmRGUkmzfIkkS2Y4Zx4xT/6E7ju','2019-11-13 19:17:05'),(5,1,2,'Admin2','$2b$14$fNta/GHYvomVWB.D3WEehu8HjOSNS/VLIOD/cXluoxs6QoGrdbh7K','2019-11-13 19:18:05'),(6,2,2,'Kevin2','$2b$14$pDkQ3vIyJbvNk/vMmhPEkuNycZboxpWLHDud558AL/kgB.qBt73dK','2019-11-13 19:19:05'),(7,2,2,'TiagoM2','$2b$14$So.bZutvYimYGwNHa/GQB.Mgh.f0SF2dhTTNpJPYTsuJVydvfFUYq','2019-11-13 19:20:05'),(8,2,2,'TiagoS2','$2b$14$YtPlYpv9pLiyo0MZd1GV5OgYt8LRYMAiXFpQuum8T4slpFudMnUwm','2019-11-13 19:21:05');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-14 15:20:18
