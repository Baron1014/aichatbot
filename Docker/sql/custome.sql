-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: aichatbox
-- ------------------------------------------------------
-- Server version	8.0.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `hw1`
--
CREATE DATABASE aichatbot;
CREATE USER 'root'@'playlab-aichatbot-flask.aichatbot_default' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON aichatbot.* TO 'root'@'playlab-aichatbot-flask.aichatbot_default';
CREATE USER 'root'@'172.%.%.%' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON aichatbot.* TO 'root'@'172.%.%.%';
CREATE USER 'root'@'%' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON aichatbot.* TO 'root'@'%';

FLUSH PRIVILEGES;
USE aichatbot;
DROP TABLE IF EXISTS `hw1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hw1` (
  `ID` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0',
  `Name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `Department` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `Enrollment` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `LineID` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hw1`
--

LOCK TABLES `hw1` WRITE;
/*!40000 ALTER TABLE `hw1` DISABLE KEYS */;
INSERT INTO `hw1` VALUES ('E54062058','Olivia Hanson','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E94061199','Myrtle Dobbs','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E24084208','Wayne Larson','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F74081022','Michael Williams','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E24086640','John Serrano','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F64086177','Donna Fraga','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F84061090','Sandra Moreland','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F74082264','Adelina Williams','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('B14051145','Shawn Leflore','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('AN4074716','Russell Phelan','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E94066115','Jim Brown','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('AN4096027','Otis Dorsey','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('I34061035','Rene Easterling','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H24071265','Diana Witte','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('C14094071','Kevin Garcia','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E64066339','William Jose','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F24066014','Michelle Foster','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H24061260','Craig Poe','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E54064026','Deshawn Farabaugh','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H24064048','Luther Sweet','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('AN4074724','Gordon Harrell','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F74082010','Cassandra Dallas','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('D54081611','Cassandra Morris','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('D24091131','Leonard Gregg','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('AN4096750','Milagros Mohamed','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H34071128','Shannon Woodward','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('C14064084','Harry Robinson','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('B24051294','Arlie Montgomery','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E84081244','Sandy Barnes','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F74094724','Leo Stephenson','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H24061074','Larry Burkholder','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('C24066096','Ramona Stockman','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F24086103','Linda Hill','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F14066169','Dawn Leclair','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F74066331','Rocco Dame','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E24072065','Thomas Richey','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E54066133','Josephine Collins','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('C64061044','Kenneth Benevides','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E84061139','Mauricio Ford','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('AN4096019','Dana Mann','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('I84066108','Mary Hudspeth','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E54062058','Nellie Ravenell','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H24066121','Lance Farrell','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F04066159','Lori Lewis','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F64066096','Oliver Rucker','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('N66094409','Charles Block','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H44061280','Preston Schauble','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F84066058','Linda Accardo','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H34071160','Eric Dimaggio','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('AICA00001','Stanley Perez','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H24071184','Bernard Latson','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F74084012','Sheri Valentine','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('C14066298','Joshua Derringer','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('C34084711','Brian Hunt','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H54064078','Robert Sheroan','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F04066052','Belinda Ridley','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F84064064','Jack Clark','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('D84089039','Mary Anderson','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('C14066191','Joseph Smith','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('E14071295','Jennifer Raebel','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('LA6051116','James Jones','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H24089048','Darlene Dube','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('C14064084','James Gilley','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H34061199','Robert Giacomini','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F74082141','Mollie Beegle','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F74081137','Cindy Fowler','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('H24061024','Paul Borg','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F44061220','Paula Williams','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F74096352','Lewis Hernandez','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('C24071203','Nathan Martinez','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('F74066161','Geraldine Labbie','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('C64099518','Jean Schultz','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫'),('B54066067','Oscar Hoffer','系所尚未填寫','入學方式尚未填寫','LINEID尚未填寫');
/*!40000 ALTER TABLE `hw1` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-04 21:25:59
