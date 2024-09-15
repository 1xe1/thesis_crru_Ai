import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Icon } from "@iconify/react";
import "./Navbar.css"; // If you still have custom styles in this file

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const studentName = localStorage.getItem("studentName") || "Guest";

  const handleMenuToggle = () => {
    setMenuOpen((prev) => !prev);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("studentName");
    window.location.href = "/login"; // Redirect to login
  };

  return (
    <nav className="w-64 bg-[#111926] text-white p-5 relative">
      <div className="mb-5">
        <p className="text-2xl mt-5">
          ระบบตรวจจับ
          <br />
          การสวมหมวกกันน็อค
        </p>
        <hr className="my-5" />
      </div>
      <ul className="list-none p-0 m-0">
        <li className="mb-5">
          <div className="text-sm">หน้าหลัก</div>
          <div className="pl-5">
            <Link to="/UserDashboard" className="flex items-center p-2 rounded hover:bg-[#1e2a38] transition-colors">
              <Icon icon="mdi:home" className="text-2xl mr-2" />
              หน้าหลัก
            </Link>
          </div>
          <div className="pl-5">
            <Link to="/Students" className="flex items-center p-2 rounded hover:bg-[#1e2a38] transition-colors">
              <Icon icon="ph:user-list" className="text-2xl mr-2" />
              ข้อมูลนักศึกษา
            </Link>
          </div>
          <div className="pl-5">
            <Link to="/AdminDashboard" className="flex items-center p-2 rounded hover:bg-[#1e2a38] transition-colors">
              <Icon icon="uil:chart" className="text-2xl mr-2" />
              รายงานสรุปสถิติ
            </Link>
          </div>
        </li>
      </ul>
      <div className="absolute bottom-5 w-[calc(100%-2rem)]">
        <div className="relative">
          <button
            onClick={handleMenuToggle}
            className="flex items-center p-2 rounded hover:bg-[#1e2a38] transition-colors w-full"
          >
            <Icon icon="mdi:account-circle" className="text-2xl mr-2" />
            {studentName}
          </button>
          {menuOpen && (
            <div className="absolute right-0 bottom-full mb-2 w-full bg-[#1e2a38] text-white border border-[#2c3e50] rounded shadow-lg">
              <Link
                to="/UserProfile"
                className="block px-4 py-2 hover:bg-[#2c3e50] transition-colors"
              >
                ข้อมูลส่วนตัว
              </Link>
              <button
                onClick={handleLogout}
                className="block px-4 py-2 w-full text-left hover:bg-[#2c3e50] transition-colors"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
