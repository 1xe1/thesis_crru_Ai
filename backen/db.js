const mysql = require('mysql2');

// สร้างการเชื่อมต่อกับฐานข้อมูล MySQL
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',       // ใช้ชื่อผู้ใช้ฐานข้อมูลของคุณ
  password: '',       // ใช้รหัสผ่านฐานข้อมูลของคุณ
  database: 'helmetaidata' // ชื่อฐานข้อมูลที่คุณต้องการเชื่อมต่อ
});

// เชื่อมต่อกับฐานข้อมูล
connection.connect((err) => {
  if (err) {
    console.error('การเชื่อมต่อฐานข้อมูลล้มเหลว:', err.stack);
    return;
  }
  console.log('เชื่อมต่อฐานข้อมูลสำเร็จ');
});

module.exports = connection;
