import React, { useState, useEffect } from 'react';

// Format date and time
const formatDate = (dateString) => {
  if (!dateString) return 'ไม่ระบุ'; // Handle empty or invalid date
  const date = new Date(dateString);
  return isNaN(date.getTime()) ? 'ไม่ระบุ' : date.toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' });
};

const formatTime = (dateString) => {
  if (!dateString) return 'ไม่ระบุ'; // Handle empty or invalid date
  const date = new Date(dateString);
  return isNaN(date.getTime()) ? 'ไม่ระบุ' : date.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' });
};

const StudentDetailsModal = ({ studentDetails, onClose }) => {
  const [visibleDetections, setVisibleDetections] = useState(5);

  // Use effect to log the studentDetails for debugging
  useEffect(() => {
    console.log('Student Details:', studentDetails);
  }, [studentDetails]);

  if (!studentDetails) return null;

  const { student, helmetDetections } = studentDetails;

  // Ensure helmetDetections is an array and log it for debugging
  const detections = Array.isArray(helmetDetections) ? helmetDetections : [];
  console.log('Helmet Detections:', detections);

  const loadMoreDetections = () => {
    setVisibleDetections((prev) => prev + 5);
  };

  return (
    <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-4 rounded-lg w-1/2 max-w-4xl relative">
        <button
          className="absolute top-2 right-2 text-gray-600 hover:text-gray-800"
          onClick={onClose}
        >
          &times;
        </button>
        <h2 className="text-xl font-bold mb-4">รายละเอียดนักศึกษา</h2>
        <div className="mb-4">
          <p><strong>รหัสนักศึกษา:</strong> {student.StudentID}</p>
          <p><strong>ชื่อ:</strong> {student.FirstName}</p>
          <p><strong>นามสกุล:</strong> {student.LastName}</p>
          <p><strong>สถานะ:</strong> {student.StudentStatus}</p>
          <p><strong>คณะ:</strong> {student.FacultyName}</p>
          <p><strong>สาขาวิชา:</strong> {student.DepartmentName}</p>
          <p><strong>หมายเลขทะเบียนรถ:</strong> {student.LicensePlate}</p>
        </div>
        <h3 className="text-lg font-semibold mb-2">ข้อมูลการตรวจจับหมวกกันน็อค</h3>
        <div className="mb-4">
          {detections.length > 0 ? (
            <div>
              {detections.slice(0, visibleDetections).map((detection, index) => (
                <div key={index} className="border border-gray-300 rounded p-2 mb-2">
                  <p><strong>เวลา:</strong> {formatDate(detection.timestamp)} {formatTime(detection.timestamp)}</p>
                  <p><strong>หมายเลขทะเบียนรถ:</strong> {detection.licensePlate || 'ไม่ระบุ'}</p>
                  <p><strong>หมวกกันน็อค:</strong> {detection.helmetDetected ? "สวมใส่" : "ไม่สวมใส่"}</p>
                </div>
              ))}
              {detections.length > visibleDetections && (
                <button
                  className="mt-2 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
                  onClick={loadMoreDetections}
                >
                  โหลดเพิ่มเติม
                </button>
              )}
            </div>
          ) : (
            <p>ไม่มีข้อมูลการตรวจจับหมวกกันน็อค</p> // Handle empty detection case
          )}
        </div>
      </div>
    </div>
  );
};

export default StudentDetailsModal;
