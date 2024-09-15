import React, { useState, useEffect } from "react";
import StudentDetailsModal from "./StudentDetailsModal";

const Students = () => {
  const [students, setStudents] = useState([]);
  const [faculties, setFaculties] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [selectedFaculty, setSelectedFaculty] = useState("");
  const [selectedDepartment, setSelectedDepartment] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [studentDetails, setStudentDetails] = useState(null);

  useEffect(() => {
    fetch("http://localhost:3000/api/students")
      .then((response) => response.json())
      .then((data) => setStudents(data));

    fetch("http://localhost:3000/api/faculties")
      .then((response) => response.json())
      .then((data) => setFaculties(data));

    fetch("http://localhost:3000/api/departments")
      .then((response) => response.json())
      .then((data) => setDepartments(data));
  }, []);

  const filteredStudents = students
    .filter(
      (student) =>
        (selectedFaculty
          ? student.FacultyID === parseInt(selectedFaculty)
          : true) &&
        (selectedDepartment
          ? student.DepartmentID === parseInt(selectedDepartment)
          : true) &&
        (searchQuery
          ? student.FirstName.toLowerCase().includes(
              searchQuery.toLowerCase()
            ) ||
            student.LastName.toLowerCase().includes(
              searchQuery.toLowerCase()
            ) ||
            student.StudentID.toString().includes(searchQuery)
          : true)
    )
    .map((student) => ({
      ...student,
      facultyName:
        faculties.find((faculty) => faculty.FacultyID === student.FacultyID)
          ?.FacultyName || "ไม่ระบุ",
      departmentName:
        departments.find(
          (department) => department.DepartmentID === student.DepartmentID
        )?.DepartmentName || "ไม่ระบุ",
    }));

  const totalPages = Math.ceil(filteredStudents.length / itemsPerPage);
  const paginatedStudents = filteredStudents.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const viewDetails = (studentID) => {
    fetch(`http://localhost:3000/api/student/${studentID}`)
      .then((response) => response.json())
      .then((data) => {
        setStudentDetails({
          student: data.student,
          helmetDetections: data.helmetDetections,
        });
        setSelectedStudent(studentID);
      });
  };

  const closeModal = () => {
    setSelectedStudent(null);
    setStudentDetails(null);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">ข้อมูลนักศึกษา</h1>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">ค้นหา:</label>
        <input
          type="text"
          className="block w-full p-2 border border-gray-300 rounded"
          placeholder="ค้นหาชื่อหรือนามสกุลหรือรหัสนักศึกษา"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">คณะ:</label>
        <select
          className="block w-full p-2 border border-gray-300 rounded"
          value={selectedFaculty}
          onChange={(e) => setSelectedFaculty(e.target.value)}
        >
          <option value="">ทั้งหมด</option>
          {faculties.map((faculty) => (
            <option key={faculty.FacultyID} value={faculty.FacultyID}>
              {faculty.FacultyName}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">สาขาวิชา:</label>
        <select
          className="block w-full p-2 border border-gray-300 rounded"
          value={selectedDepartment}
          onChange={(e) => setSelectedDepartment(e.target.value)}
        >
          <option value="">ทั้งหมด</option>
          {departments.map((department) => (
            <option
              key={department.DepartmentID}
              value={department.DepartmentID}
            >
              {department.DepartmentName}
            </option>
          ))}
        </select>
      </div>

      <table className="min-w-full bg-white border border-gray-200 rounded-lg shadow-md">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b">รหัสนักศึกษา</th>
            <th className="py-2 px-4 border-b">ชื่อ</th>
            <th className="py-2 px-4 border-b">นามสกุล</th>
            <th className="py-2 px-4 border-b">สถานะ</th>
            <th className="py-2 px-4 border-b">คณะ</th>
            <th className="py-2 px-4 border-b">สาขาวิชา</th>
            <th className="py-2 px-4 border-b">รายละเอียด</th>
          </tr>
        </thead>
        <tbody>
          {paginatedStudents.map((student) => (
            <tr key={student.StudentID}>
              <td className="py-2 px-4 border-b">{student.StudentID}</td>
              <td className="py-2 px-4 border-b">{student.FirstName}</td>
              <td className="py-2 px-4 border-b">{student.LastName}</td>
              <td className="py-2 px-4 border-b">{student.StudentStatus}</td>
              <td className="py-2 px-4 border-b">{student.facultyName}</td>
              <td className="py-2 px-4 border-b">{student.departmentName}</td>
              <td className="py-2 px-4 border-b">
                <button
                  className="bg-blue-500 text-white py-1 px-2 rounded"
                  onClick={() => viewDetails(student.StudentID)}
                >
                  ดูรายละเอียด
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="mt-4">
        <button
          className="bg-blue-500 text-white py-2 px-4 rounded mr-2"
          disabled={currentPage === 1}
          onClick={() => setCurrentPage(currentPage - 1)}
        >
          ก่อนหน้า
        </button>
        <button
          className="bg-blue-500 text-white py-2 px-4 rounded"
          disabled={currentPage === totalPages}
          onClick={() => setCurrentPage(currentPage + 1)}
        >
          ถัดไป
        </button>
      </div>

      {selectedStudent && studentDetails && (
        <StudentDetailsModal
          studentDetails={studentDetails}
          onClose={closeModal}
        />
      )}
    </div>
  );
};

export default Students;
