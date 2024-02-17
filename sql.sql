-- --------------------------------------------------------
-- 主机:                           192.168.1.15
-- 服务器版本:                        8.2.0 - MySQL Community Server - GPL
-- 服务器操作系统:                      Linux
-- HeidiSQL 版本:                  12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 导出 python 的数据库结构
CREATE DATABASE IF NOT EXISTS `python` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `python`;

-- 导出  表 python.user 结构
CREATE TABLE IF NOT EXISTS `user` (
  `username` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `userid` int DEFAULT NULL,
  `password` text COLLATE utf8mb4_general_ci NOT NULL COMMENT '哈希密码',
  `email` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '邮箱',
  `init_time` int NOT NULL COMMENT '用户注册时间-时间戳'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='存放用户信息';

-- 正在导出表  python.user 的数据：~0 rows (大约)
REPLACE INTO `user` (`username`, `userid`, `password`, `email`, `init_time`) VALUES
	('Paimon', 1, '1e0e61ce9c025449ba68208e1cbda565a7300d3a02db6b5b79fe88578b38d774', 'abb1234aabb@gmail.com', 1707994288);

-- 导出  表 python.votes 结构
CREATE TABLE IF NOT EXISTS `votes` (
  `vote_id` int NOT NULL COMMENT '投票项目ID',
  `title` text COLLATE utf8mb4_general_ci NOT NULL COMMENT '投票标题',
  `neirong` text COLLATE utf8mb4_general_ci NOT NULL COMMENT '投票内容描述',
  `chooses` json NOT NULL COMMENT '投票选项',
  `text` text COLLATE utf8mb4_general_ci COMMENT '注释 可选',
  `start_time` int NOT NULL COMMENT '开始时间',
  `end_time` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='投票数据表';

-- 正在导出表  python.votes 的数据：~0 rows (大约)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
