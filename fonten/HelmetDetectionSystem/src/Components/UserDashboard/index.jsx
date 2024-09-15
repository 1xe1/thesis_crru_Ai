import React, { useEffect, useState } from 'react';

const UserDashboard = () => {
  const [stats, setStats] = useState({ today: 0, month: 0, allTime: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      const token = localStorage.getItem('token');
  
      try {
        const response = await fetch('http://localhost:3000/api/user/statistics', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
  
        if (response.ok) {
          const data = await response.json();
          setStats(data);
        } else if (response.status === 401) {
          console.error('Unauthorized: Token may be invalid');
        } else if (response.status === 403) {
          console.error('Forbidden: Invalid token');
        } else {
          console.error('Failed to fetch statistics', await response.text());
        }
      } catch (error) {
        console.error('Error fetching statistics:', error);
      } finally {
        setLoading(false);
      }
    };
  
    fetchStats();
  }, []);
  

  if (loading) {
    return <div className="p-5">Loading...</div>;
  }

  return (
    <div className="p-5 bg-gray-100 min-h-screen flex flex-col items-center">
      <h1 className="mb-5 text-4xl text-gray-800">สถิติการตรวจจับ</h1>
      <div className="flex justify-around w-full max-w-4xl">
        <div className="bg-white p-5 rounded-lg shadow-lg text-center w-1/3">
          <h2 className="mb-2 text-2xl text-blue-600">วันนี้</h2>
          <p className="text-lg text-gray-700">จำนวน: {stats.today}</p>
        </div>
        <div className="bg-white p-5 rounded-lg shadow-lg text-center w-1/3">
          <h2 className="mb-2 text-2xl text-blue-600">เดือนนี้</h2>
          <p className="text-lg text-gray-700">จำนวน: {stats.month}</p>
        </div>
        <div className="bg-white p-5 rounded-lg shadow-lg text-center w-1/3">
          <h2 className="mb-2 text-2xl text-blue-600">ทั้งหมด</h2>
          <p className="text-lg text-gray-700">จำนวน: {stats.allTime}</p>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
