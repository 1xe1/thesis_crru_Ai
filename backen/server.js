const express = require("express");
const cors = require("cors");
const connection = require("./db"); // Import database connection
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken"); // Import jwt for token generation
const secretKey = "CRRU"; // Replace with a secure key
const XLSX = require("xlsx"); // Import xlsx package

const app = express();
const port = 3000;

// Use cors middleware
app.use(cors());

// Middleware for JSON body parsing
app.use(express.json());

// Endpoint to get student data
app.get("/api/students", (req, res) => {
  const { facultyID, departmentID } = req.query;

  let query = "SELECT * FROM students WHERE 1=1";
  let params = [];

  if (facultyID) {
    query += " AND FacultyID = ?";
    params.push(parseInt(facultyID));
  }

  if (departmentID) {
    query += " AND DepartmentID = ?";
    params.push(parseInt(departmentID));
  }

  console.log("Executing query:", query, "with params:", params);

  connection.query(query, params, (error, results) => {
    if (error) {
      console.error("Database error:", error);
      return res.status(500).json({ error: "เกิดข้อผิดพลาดในการดึงข้อมูล" });
    }
    console.log("Query results:", results);
    res.json(results);
  });
});

// Endpoint to get detailed student information
app.get("/api/student/:id", (req, res) => {
  const studentID = req.params.id;

  const studentQuery = "SELECT * FROM students WHERE StudentID = ?";
  const studentParams = [studentID];

  const helmetDetectionQuery =
    "SELECT * FROM helmetdetection WHERE StudentID = ?";

  connection.query(
    studentQuery,
    studentParams,
    (studentError, studentResults) => {
      if (studentError) {
        console.error("Database error:", studentError);
        return res
          .status(500)
          .json({ error: "เกิดข้อผิดพลาดในการดึงข้อมูลนักศึกษา" });
      }

      if (studentResults.length === 0) {
        return res.status(404).json({ error: "ไม่พบข้อมูลนักศึกษา" });
      }

      const studentData = studentResults[0];

      connection.query(
        helmetDetectionQuery,
        studentParams,
        (helmetDetectionError, helmetDetectionResults) => {
          if (helmetDetectionError) {
            console.error("Database error:", helmetDetectionError);
            return res
              .status(500)
              .json({
                error: "เกิดข้อผิดพลาดในการดึงข้อมูลการตรวจจับหมวกกันน็อก",
              });
          }

          res.json({
            student: studentData,
            helmetDetections: helmetDetectionResults,
          });
        }
      );
    }
  );
});

// Endpoint to get faculty data
app.get("/api/faculties", (req, res) => {
  connection.query("SELECT * FROM faculties", (error, results) => {
    if (error) {
      return res.status(500).json({ error: "เกิดข้อผิดพลาดในการดึงข้อมูล" });
    }
    res.json(results);
  });
});

// Endpoint to get department data
app.get("/api/departments", (req, res) => {
  connection.query("SELECT * FROM departments", (error, results) => {
    if (error) {
      return res.status(500).json({ error: "เกิดข้อผิดพลาดในการดึงข้อมูล" });
    }
    res.json(results);
  });
});

// Login endpoint
app.post("/api/login", (req, res) => {
  const { studentID, password } = req.body;

  const query = "SELECT * FROM students WHERE StudentID = ?";
  connection.query(query, [studentID], async (error, results) => {
    if (error) {
      return res.status(500).json({ error: "Database error" });
    }

    if (results.length === 0) {
      return res.status(401).json({ error: "Invalid StudentID or Password" });
    }

    const student = results[0];

    // Compare the provided password with the stored hashed password
    const validPassword = await bcrypt.compare(password, student.PasswordHash);

    if (!validPassword) {
      return res.status(401).json({ error: "Invalid StudentID or Password" });
    }

    // Create a token with the student's ID and a 1-hour expiration time
    const token = jwt.sign({ id: student.StudentID }, secretKey, {
      expiresIn: "1h",
    });

    // Return the token and the student information
    res.json({ token, student });
  });
});

// Register endpoint
app.post("/api/register", async (req, res) => {
  try {
    const {
      studentID,
      firstName,
      lastName,
      password,
      confirmPassword,
      faculty,
      department,
      licensePlate,
    } = req.body;

    // Check if passwords match
    if (password !== confirmPassword) {
      return res
        .status(400)
        .json({ error: "รหัสผ่านและการยืนยันรหัสผ่านไม่ตรงกัน" });
    }

    // Hash the password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Insert into the database
    const query =
      "INSERT INTO students (StudentID, FirstName, LastName, PasswordHash, FacultyID, DepartmentID, LicensePlate) VALUES (?, ?, ?, ?, ?, ?, ?)";
    const params = [
      studentID,
      firstName,
      lastName,
      hashedPassword,
      faculty,
      department,
      licensePlate,
    ];

    connection.query(query, params, (error) => {
      if (error) {
        console.error("Error inserting student data:", error);
        return res
          .status(500)
          .json({ error: "เกิดข้อผิดพลาดในการลงทะเบียนนักศึกษา" });
      }

      // Registration successful
      res.status(201).json({ message: "ลงทะเบียนสำเร็จ" });
    });
  } catch (err) {
    console.error("Unexpected error:", err);
    res.status(500).json({ error: "เกิดข้อผิดพลาดที่ไม่คาดคิด" });
  }
});

// Add this endpoint to get user-specific statistics
app.get('/api/user/statistics', (req, res) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  jwt.verify(token, secretKey, (err, decoded) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }

    const studentID = decoded.id;

    // Example queries for statistics
    const todayQuery = 'SELECT COUNT(*) AS count FROM helmetdetection WHERE StudentID = ? AND DATE(DetectionTime) = CURDATE()';
    const monthQuery = 'SELECT COUNT(*) AS count FROM helmetdetection WHERE StudentID = ? AND YEAR(DetectionTime) = YEAR(CURDATE()) AND MONTH(DetectionTime) = MONTH(CURDATE())';
    const allTimeQuery = 'SELECT COUNT(*) AS count FROM helmetdetection WHERE StudentID = ?';

    connection.query(todayQuery, [studentID], (error, todayResults) => {
      if (error) return res.status(500).json({ error: 'Database error' });

      connection.query(monthQuery, [studentID], (error, monthResults) => {
        if (error) return res.status(500).json({ error: 'Database error' });

        connection.query(allTimeQuery, [studentID], (error, allTimeResults) => {
          if (error) return res.status(500).json({ error: 'Database error' });

          res.json({
            today: todayResults[0].count,
            month: monthResults[0].count,
            allTime: allTimeResults[0].count
          });
        });
      });
    });
  });
});

// Endpoint to get statistics data
app.get("/api/statistics", (req, res) => {
  // Replace these queries with your actual database queries to get the data
  const todayQuery =
    "SELECT COUNT(*) AS count FROM helmetdetection WHERE DATE(DetectionTime) = CURDATE()";
  const thisMonthQuery =
    "SELECT COUNT(*) AS count FROM helmetdetection WHERE MONTH(DetectionTime) = MONTH(CURDATE()) AND YEAR(DetectionTime) = YEAR(CURDATE())";
  const allTimeQuery = "SELECT COUNT(*) AS count FROM helmetdetection";
  const monthlyDataQuery = `
    SELECT MONTH(DetectionTime) AS month, COUNT(*) AS count
    FROM helmetdetection
    WHERE YEAR(DetectionTime) = YEAR(CURDATE())
    GROUP BY MONTH(DetectionTime)
    ORDER BY MONTH(DetectionTime)
  `;

  connection.query(todayQuery, (todayError, todayResults) => {
    if (todayError) {
      return res.status(500).json({ error: "Error fetching today's data" });
    }

    connection.query(thisMonthQuery, (thisMonthError, thisMonthResults) => {
      if (thisMonthError) {
        return res
          .status(500)
          .json({ error: "Error fetching this month's data" });
      }

      connection.query(allTimeQuery, (allTimeError, allTimeResults) => {
        if (allTimeError) {
          return res
            .status(500)
            .json({ error: "Error fetching all-time data" });
        }

        connection.query(
          monthlyDataQuery,
          (monthlyDataError, monthlyDataResults) => {
            if (monthlyDataError) {
              return res
                .status(500)
                .json({ error: "Error fetching monthly data" });
            }

            const months = [];
            const counts = [];
            monthlyDataResults.forEach((row) => {
              months.push(row.month);
              counts.push(row.count);
            });

            res.json({
              today: todayResults[0].count,
              thisMonth: thisMonthResults[0].count,
              allTime: allTimeResults[0].count,
              monthlyData: {
                labels: months.map((month) => `เดือน ${month}`),
                datasets: [
                  {
                    label: "จำนวนการตรวจจับรายเดือน",
                    data: counts,
                    borderColor: "rgba(75, 192, 192, 1)",
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderWidth: 1,
                  },
                ],
              },
            });
          }
        );
      });
    });
  });
});


// Start the server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
