import React, { useEffect, useState } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { saveAs } from 'file-saver'; // Install file-saver to handle file downloads

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend);

const AdminDashboard = () => {
  const [statistics, setStatistics] = useState({
    today: 0,
    thisMonth: 0,
    allTime: 0,
  });
  const [monthlyChartData, setMonthlyChartData] = useState({
    labels: [],
    datasets: []
  });

  useEffect(() => {
    // Fetch statistics from the server
    const fetchStatistics = async () => {
      try {
        const response = await fetch('http://localhost:3000/api/statistics'); // Adjust the endpoint as needed
        if (response.ok) {
          const data = await response.json();
          setStatistics({
            today: data.today,
            thisMonth: data.thisMonth,
            allTime: data.allTime,
          });
          setMonthlyChartData(data.monthlyData); // Set chart data
        } else {
          console.error('Failed to fetch statistics');
        }
      } catch (error) {
        console.error('Error fetching statistics:', error);
      }
    };

    fetchStatistics();
  }, []);



  return (
    <div className="dashboard-container">
      <div className="p-5 bg-gray-100 min-h-screen flex flex-col items-center">
        <h1 className="mb-5 text-4xl text-gray-800">สถิติทั้งหมด</h1>
        <div className="flex justify-around w-full max-w-4xl mb-10">
          <div className="bg-white p-5 rounded-lg shadow-lg text-center w-1/3">
            <h2 className="mb-2 text-2xl text-blue-600">วันนี้</h2>
            <p className="text-lg text-gray-700">จำนวน: {statistics.today}</p>
          </div>
          <div className="bg-white p-5 rounded-lg shadow-lg text-center w-1/3">
            <h2 className="mb-2 text-2xl text-blue-600">เดือนนี้</h2>
            <p className="text-lg text-gray-700">จำนวน: {statistics.thisMonth}</p>
          </div>
          <div className="bg-white p-5 rounded-lg shadow-lg text-center w-1/3">
            <h2 className="mb-2 text-2xl text-blue-600">ทั้งหมด</h2>
            <p className="text-lg text-gray-700">จำนวน: {statistics.allTime}</p>
          </div>
        </div>
        <div className="w-full max-w-4xl mb-10">
          <h2 className="mb-5 text-2xl text-gray-800">กราฟสถิติการตรวจจับรายเดือน</h2>
          <div className="bg-white p-5 rounded-lg shadow-lg">
            <Line 
              data={monthlyChartData} 
              options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'top',
                  },
                  tooltip: {
                    callbacks: {
                      label: function(tooltipItem) {
                        return `จำนวน: ${tooltipItem.raw}`;
                      }
                    }
                  }
                }
              }} 
            />
          </div>
        </div>
        <div className="w-full max-w-4xl mb-10">
          <h2 className="mb-5 text-2xl text-gray-800">กราฟการตรวจจับรายเดือน</h2>
          <div className="bg-white p-5 rounded-lg shadow-lg">
            <Bar 
              data={monthlyChartData} 
              options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'top',
                  },
                  tooltip: {
                    callbacks: {
                      label: function(tooltipItem) {
                        return `จำนวน: ${tooltipItem.raw}`;
                      }
                    }
                  }
                }
              }} 
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
