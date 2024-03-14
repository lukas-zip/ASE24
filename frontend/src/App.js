import React, { useState } from 'react';
import Login from './Login'; // Import the Login component
import Dashboard from './Dashboard'; // Import the Dashboard component (or any other component for authenticated users)

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // State to track authentication status

  // Function to handle successful login
  const handleLogin = () => {
    setIsLoggedIn(true); // Set isLoggedIn state to true when login is successful
  };

  // Function to handle logout
  const handleLogout = () => {
    setIsLoggedIn(false); // Set isLoggedIn state to false when logout is triggered
  };

  return (
    <div>
      {/* Conditionally render either the Login component or Dashboard component based on isLoggedIn state */}
      {isLoggedIn ? (
        <Dashboard onLogout={handleLogout} /> // Pass handleLogout function to Dashboard component
      ) : (
        <Login onLogin={handleLogin} /> // Pass handleLogin function to Login component
      )}
    </div>
  );
};

export default App;
