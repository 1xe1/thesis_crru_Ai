import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Register() {
  const [studentInfo, setStudentInfo] = useState({
    studentID: '',
    firstName: '',
    lastName: '',
    password: '',
    confirmPassword: '',
    faculty: '',
    department: '',
    licensePlate: ''
  });

  const [faculties, setFaculties] = useState([]);
  const [departments, setDepartments] = useState([]);

  useEffect(() => {
    const fetchFaculties = async () => {
      try {
        const response = await fetch('http://localhost:3000/api/faculties');
        const data = await response.json();
        setFaculties(data);
      } catch (error) {
        console.error('Error fetching faculties:', error);
      }
    };

    const fetchDepartments = async () => {
      try {
        const response = await fetch('http://localhost:3000/api/departments');
        const data = await response.json();
        setDepartments(data);
      } catch (error) {
        console.error('Error fetching departments:', error);
      }
    };

    fetchFaculties();
    fetchDepartments();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setStudentInfo({
      ...studentInfo,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (studentInfo.password !== studentInfo.confirmPassword) {
      alert('รหัสผ่านและการยืนยันรหัสผ่านไม่ตรงกัน');
      return;
    }

    try {
      const response = await fetch('http://localhost:3000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(studentInfo)
      });

      const result = await response.json();

      if (response.ok) {
        alert(result.message);
        // Redirect to login page
      } else {
        alert(result.error);
      }
    } catch (error) {
      console.error('Error during registration:', error);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-r from-pink-500 to-blue-700">
      <div className="bg-white p-10 w-full max-w-md rounded-lg shadow-xl text-center">
        <h2 className="mb-6 text-2xl font-bold">ลงทะเบียน</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <input
              type="text"
              name="studentID"
              placeholder="รหัสนักศึกษา"
              value={studentInfo.studentID}
              onChange={handleChange}
              required
              className="w-full p-3 border-b-2 border-gray-300 focus:border-blue-500 outline-none transition-colors"
            />
          </div>
          <div className="mb-6">
            <input
              type="text"
              name="firstName"
              placeholder="ชื่อ"
              value={studentInfo.firstName}
              onChange={handleChange}
              required
              className="w-full p-3 border-b-2 border-gray-300 focus:border-blue-500 outline-none transition-colors"
            />
          </div>
          <div className="mb-6">
            <input
              type="text"
              name="lastName"
              placeholder="นามสกุล"
              value={studentInfo.lastName}
              onChange={handleChange}
              required
              className="w-full p-3 border-b-2 border-gray-300 focus:border-blue-500 outline-none transition-colors"
            />
          </div>
          <div className="mb-6">
            <input
              type="password"
              name="password"
              placeholder="รหัสผ่าน"
              value={studentInfo.password}
              onChange={handleChange}
              required
              className="w-full p-3 border-b-2 border-gray-300 focus:border-blue-500 outline-none transition-colors"
            />
          </div>
          <div className="mb-6">
            <input
              type="password"
              name="confirmPassword"
              placeholder="ยืนยันรหัสผ่าน"
              value={studentInfo.confirmPassword}
              onChange={handleChange}
              required
              className="w-full p-3 border-b-2 border-gray-300 focus:border-blue-500 outline-none transition-colors"
            />
          </div>
          <div className="mb-6">
            <select
              name="faculty"
              value={studentInfo.faculty}
              onChange={handleChange}
              required
              className="w-full p-3 border-b-2 border-gray-300 focus:border-blue-500 outline-none transition-colors"
            >
              <option value="">เลือกคณะ</option>
              {faculties.map(faculty => (
                <option key={faculty.FacultyID} value={faculty.FacultyID}>
                  {faculty.FacultyName}
                </option>
              ))}
            </select>
          </div>
          <div className="mb-6">
            <select
              name="department"
              value={studentInfo.department}
              onChange={handleChange}
              required
              className="w-full p-3 border-b-2 border-gray-300 focus:border-blue-500 outline-none transition-colors"
            >
              <option value="">เลือกสาขา</option>
              {departments.map(department => (
                <option key={department.DepartmentID} value={department.DepartmentID}>
                  {department.DepartmentName}
                </option>
              ))}
            </select>
          </div>
          <div className="mb-6">
            <input
              type="text"
              name="licensePlate"
              placeholder="หมายเลขทะเบียนรถ"
              value={studentInfo.licensePlate}
              onChange={handleChange}
              required
              className="w-full p-3 border-b-2 border-gray-300 focus:border-blue-500 outline-none transition-colors"
            />
          </div>
          <button
            type="submit"
            className="w-4/5 p-3 bg-gradient-to-r from-blue-600 to-pink-500 text-white font-semibold rounded-lg hover:bg-gradient-to-r hover:from-pink-500 hover:to-blue-600 transition-colors"
          >
            สมัครสมาชิก
          </button>
          <Link to="/Login" className="block mt-6 text-blue-600 hover:underline">
            เข้าสู่ระบบ
          </Link>
        </form>
      </div>
    </div>
  );
}

export default Register;
