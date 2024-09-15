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

 Date: 30/08/2024 01:49:33
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
-- Table structure for faculties
-- ----------------------------
DROP TABLE IF EXISTS `faculties`;
CREATE TABLE `faculties`  (
  `FacultyID` int NOT NULL COMMENT 'รหัสคณะ',
  `FacultyName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'ชื่อคณะ',
  PRIMARY KEY (`FacultyID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'ตารางสำหรับจัดเก็บข้อมูลคณะ' ROW_FORMAT = DYNAMIC;

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

SET FOREIGN_KEY_CHECKS = 1;
