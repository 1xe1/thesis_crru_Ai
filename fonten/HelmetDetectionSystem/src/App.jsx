import React, { useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./Components/Navbar";
import UserDashboard from "./Components/UserDashboard";
import Students from "./Components/Students";
import Login from "./Components/Login";
import Register from "./Components/Register";
import "./App.css";
import "react-toastify/dist/ReactToastify.css";
import PrivateRoute from "./Components/PrivateRoute";
import AdminDashboard from "./Components/AdminDashboard";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsAuthenticated(!!token);
  }, []);

  return (
    <>
      {!isAuthenticated ? (
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      ) : (
        <div className="flex min-h-screen bg-gray-100">
          <Navbar />
          <div className="flex-1 p-5">
            <Routes>
              <Route
                path="/UserDashboard"
                element={<PrivateRoute element={<UserDashboard />} />}
              />
              <Route
                path="/Students"
                element={<PrivateRoute element={<Students />} />}
              />
              {/* <Route
                path="/UserProfile"
                element={<PrivateRoute element={<UserProfile />} />}
              /> */}
              <Route
                path="/AdminDashboard"
                element={<PrivateRoute element={<AdminDashboard />} />}
              />
              <Route path="/Register" element={<Register />} />
            </Routes>
          </div>
        </div>
      )}
    </>
  );
}

export default App;
