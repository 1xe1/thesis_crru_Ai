/*
 Navicat Premium Dump SQL

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 100432 (10.4.32-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : helmetaidata

 Target Server Type    : MySQL
 Target Server Version : 100432 (10.4.32-MariaDB)
 File Encoding         : 65001

 Date: 30/08/2024 01:49:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for departments
-- ----------------------------
DROP TABLE IF EXISTS `departments`;
CREATE TABLE `departments`  (
  `DepartmentID` int NOT NULL COMMENT 'รหัสสาขาวิชา',
  `DepartmentName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'ชื่อสาขาวิชา',
  `FacultyID` int NULL DEFAULT NULL COMMENT 'รหัสคณะ (Foreign Key)',
  PRIMARY KEY (`DepartmentID`) USING BTREE,
  INDEX `FacultyID`(`FacultyID` ASC) USING BTREE,
  CONSTRAINT `departments_ibfk_1` FOREIGN KEY (`FacultyID`) REFERENCES `faculties` (`FacultyID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'ตารางสำหรับจัดเก็บข้อมูลสาขาวิชา' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of departments
-- ----------------------------
INSERT INTO `departments` VALUES (1, 'วิศวกรรมคอมพิวเตอร์', 1);
INSERT INTO `departments` VALUES (2, 'วิศวกรรมเครื่องกล', 1);
INSERT INTO `departments` VALUES (3, 'การจัดการ', 2);
INSERT INTO `departments` VALUES (4, 'การตลาด', 2);
INSERT INTO `departments` VALUES (5, 'พัฒนาการเกษตร', 3);
INSERT INTO `departments` VALUES (6, 'สัตว์ศาสตร์', 3);

-- ----------------------------
-- Table structure for faculties
-- ----------------------------
DROP TABLE IF EXISTS `faculties`;
CREATE TABLE `faculties`  (
  `FacultyID` int NOT NULL COMMENT 'รหัสคณะ',
  `FacultyName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'ชื่อคณะ',
  PRIMARY KEY (`FacultyID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'ตารางสำหรับจัดเก็บข้อมูลคณะ' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of faculties
-- ----------------------------
INSERT INTO `faculties` VALUES (1, 'คณะวิศวกรรมศาสตร์');
INSERT INTO `faculties` VALUES (2, 'คณะบริหารธุรกิจ');
INSERT INTO `faculties` VALUES (3, 'คณะเกษตรศาสตร์');

-- ----------------------------
-- Table structure for helmetdetection
-- ----------------------------
DROP TABLE IF EXISTS `helmetdetection`;
CREATE TABLE `helmetdetection`  (
  `DetectionID` int NOT NULL AUTO_INCREMENT COMMENT 'รหัสการตรวจจับ (Primary Key)',
  `StudentID` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'รหัสนักศึกษา (Foreign Key)',
  `DetectionTime` datetime NOT NULL COMMENT 'เวลาการตรวจจับ',
  `ImageURL` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT 'ลิงค์หรือที่อยู่ของภาพการตรวจจับ',
  PRIMARY KEY (`DetectionID`) USING BTREE,
  INDEX `StudentID`(`StudentID` ASC) USING BTREE,
  CONSTRAINT `helmetdetection_ibfk_1` FOREIGN KEY (`StudentID`) REFERENCES `students` (`StudentID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 81 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'ตารางสำหรับจัดเก็บข้อมูลการตรวจจับหมวกกันน็อก' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of helmetdetection
-- ----------------------------
INSERT INTO `helmetdetection` VALUES (1, 'S001', '2024-08-29 08:00:00', 'http://example.com/image1.jpg');
INSERT INTO `helmetdetection` VALUES (2, 'S001', '2024-08-29 08:30:00', 'http://example.com/image2.jpg');
INSERT INTO `helmetdetection` VALUES (3, 'S001', '2024-08-29 09:00:00', 'http://example.com/image3.jpg');
INSERT INTO `helmetdetection` VALUES (4, 'S002', '2024-08-29 09:00:00', 'http://example.com/image4.jpg');
INSERT INTO `helmetdetection` VALUES (5, 'S002', '2024-08-29 09:30:00', 'http://example.com/image5.jpg');
INSERT INTO `helmetdetection` VALUES (6, 'S002', '2024-08-29 10:00:00', 'http://example.com/image6.jpg');
INSERT INTO `helmetdetection` VALUES (7, 'S003', '2024-08-29 10:00:00', 'http://example.com/image7.jpg');
INSERT INTO `helmetdetection` VALUES (8, 'S003', '2024-08-29 10:30:00', 'http://example.com/image8.jpg');
INSERT INTO `helmetdetection` VALUES (9, 'S003', '2024-08-29 11:00:00', 'http://example.com/image9.jpg');
INSERT INTO `helmetdetection` VALUES (10, 'S003', '2024-08-29 11:30:00', 'http://example.com/image10.jpg');
INSERT INTO `helmetdetection` VALUES (11, 'S004', '2024-08-29 12:00:00', 'http://example.com/image11.jpg');
INSERT INTO `helmetdetection` VALUES (12, 'S004', '2024-08-29 12:30:00', 'http://example.com/image12.jpg');
INSERT INTO `helmetdetection` VALUES (13, 'S004', '2024-08-29 13:00:00', 'http://example.com/image13.jpg');
INSERT INTO `helmetdetection` VALUES (14, 'S005', '2024-08-29 13:30:00', 'http://example.com/image14.jpg');
INSERT INTO `helmetdetection` VALUES (15, 'S005', '2024-08-29 14:00:00', 'http://example.com/image15.jpg');
INSERT INTO `helmetdetection` VALUES (16, 'S005', '2024-08-29 14:30:00', 'http://example.com/image16.jpg');
INSERT INTO `helmetdetection` VALUES (17, 'S005', '2024-08-29 15:00:00', 'http://example.com/image17.jpg');
INSERT INTO `helmetdetection` VALUES (18, 'S006', '2024-08-29 15:30:00', 'http://example.com/image18.jpg');
INSERT INTO `helmetdetection` VALUES (19, 'S006', '2024-08-29 16:00:00', 'http://example.com/image19.jpg');
INSERT INTO `helmetdetection` VALUES (20, 'S006', '2024-08-29 16:30:00', 'http://example.com/image20.jpg');
INSERT INTO `helmetdetection` VALUES (21, '641463021', '2024-08-29 22:29:28', 'http://example.com/image20.jpg');
INSERT INTO `helmetdetection` VALUES (22, '641463021', '2024-07-24 22:38:30', 'http://example.com/image20.jpg');
INSERT INTO `helmetdetection` VALUES (23, '641463021', '2024-08-28 22:38:30', 'http://example.com/image20.jpg');
INSERT INTO `helmetdetection` VALUES (24, '641463021', '2024-08-29 22:29:28', 'http://example.com/image20.jpg');
INSERT INTO `helmetdetection` VALUES (25, '641463022', '2024-06-19 23:13:00', NULL);
INSERT INTO `helmetdetection` VALUES (26, '641463022', '2024-06-26 23:13:23', NULL);
INSERT INTO `helmetdetection` VALUES (27, '641463021', '2024-08-30 00:25:35', NULL);
INSERT INTO `helmetdetection` VALUES (28, '641463022', '2024-08-30 00:41:12', NULL);

-- ----------------------------
-- Table structure for students
-- ----------------------------
DROP TABLE IF EXISTS `students`;
CREATE TABLE `students`  (
  `StudentID` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'รหัสนักศึกษา',
  `FirstName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'ชื่อนักศึกษา',
  `LastName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'นามสกุลนักศึกษา',
  `FacultyID` int NULL DEFAULT NULL COMMENT 'รหัสคณะ (Foreign Key)',
  `DepartmentID` int NULL DEFAULT NULL COMMENT 'รหัสสาขาวิชา (Foreign Key)',
  `PasswordHash` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'รหัสผ่านที่เข้ารหัสแล้ว',
  `StudentStatus` enum('กำลังศึกษา','ออกจากการศึกษา') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'กำลังศึกษา' COMMENT 'สถานะการศึกษา',
  `LicensePlate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'หมายเลขทะเบียนรถ',
  PRIMARY KEY (`StudentID`) USING BTREE,
  INDEX `FacultyID`(`FacultyID` ASC) USING BTREE,
  INDEX `DepartmentID`(`DepartmentID` ASC) USING BTREE,
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`FacultyID`) REFERENCES `faculties` (`FacultyID`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `students_ibfk_2` FOREIGN KEY (`DepartmentID`) REFERENCES `departments` (`DepartmentID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'ตารางสำหรับจัดเก็บข้อมูลนักศึกษา' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of students
-- ----------------------------
INSERT INTO `students` VALUES ('641463021', 'anun', 'namwong', 1, 2, '$2b$10$p7tz7H7uMGYWwUigmWJRV.jBuw.Gv9KJn1F1vVBwFj4b1gg7.J9iW', 'กำลังศึกษา', 'กธ1669');
INSERT INTO `students` VALUES ('641463022', 'ทดสอบ', 'สอบทด', 1, 3, '$2b$10$Nd3nTqBoMLRbx6HWvo82FuH8yYrNgmt89Y2ic5/OPcgxstdR8L8jO', 'กำลังศึกษา', 'ฌม125');
INSERT INTO `students` VALUES ('641463023', 'ทดสอบ1', 'สอบทด1', 1, 3, '$2b$10$N1dx2/vdbeyCauN6SS96BelQ/w5HJCkZrgSw8mDcmZMwdX6ro9z0u', 'กำลังศึกษา', 'กรท45');
INSERT INTO `students` VALUES ('S001', 'สมชาย', 'ดี', 1, 1, '$2b$10$p7tz7H7uMGYWwUigmWJRV.jBuw.Gv9KJn1F1vVBwFj4b1gg7.J9iW', 'กำลังศึกษา', '1A1234');
INSERT INTO `students` VALUES ('S002', 'สมหญิง', 'ดี', 1, 2, '$2b$10$p7tz7H7uMGYWwUigmWJRV.jBuw.Gv9KJn1F1vVBwFj4b1gg7.J9iW', 'กำลังศึกษา', '2B2345');
INSERT INTO `students` VALUES ('S003', 'สมศรี', 'ดี', 2, 1, '$2b$10$p7tz7H7uMGYWwUigmWJRV.jBuw.Gv9KJn1F1vVBwFj4b1gg7.J9iW', 'ออกจากการศึกษา', '3C3456');
INSERT INTO `students` VALUES ('S004', 'สมเกียรติ', 'ดี', 2, 2, '$2b$10$p7tz7H7uMGYWwUigmWJRV.jBuw.Gv9KJn1F1vVBwFj4b1gg7.J9iW', 'กำลังศึกษา', '4D4567');
INSERT INTO `students` VALUES ('S005', 'สมพงษ์', 'ดี', 3, 1, '$2b$10$p7tz7H7uMGYWwUigmWJRV.jBuw.Gv9KJn1F1vVBwFj4b1gg7.J9iW', 'กำลังศึกษา', '5E5678');
INSERT INTO `students` VALUES ('S006', 'สมปอง', 'ดี', 3, 2, '$2b$10$p7tz7H7uMGYWwUigmWJRV.jBuw.Gv9KJn1F1vVBwFj4b1gg7.J9iW', 'กำลังศึกษา', '6F6789');
INSERT INTO `students` VALUES ('S007', 'สมบัติ', 'ดี', 1, 1, '$2b$10$p7tz7H7uMGYWwUigmWJRV.jBuw.Gv9KJn1F1vVBwFj4b1gg7.J9iW', 'ออกจากการศึกษา', '7G7890');
INSERT INTO `students` VALUES ('S008', 'สมพร', 'ดี', 1, 2, '$2b$10$p7tz7H7uMGYWwUigmWJRV.jBuw.Gv9KJn1F1vVBwFj4b1gg7.J9iW', 'กำลังศึกษา', '8H8901');
INSERT INTO `students` VALUES ('S009', 'สมเพียร', 'ดี', 2, 1, '$2b$10$p7tz7H7uMGYWwUigmWJRV.jBuw.Gv9KJn1F1vVBwFj4b1gg7.J9iWa', 'กำลังศึกษา', '9I9012');
INSERT INTO `students` VALUES ('S010', 'สมอรรถ', 'ดี', 2, 2, 'hashedpassword10', 'กำลังศึกษา', '10J012');

SET FOREIGN_KEY_CHECKS = 1;
