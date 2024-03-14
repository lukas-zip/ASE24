import React from 'react';

const Dashboard = ({ onLogout }) => {
  return (
    <div>
      <h1>Welcome to Your Dashboard</h1>
      {/* Display user information, activity feed, data visualizations, etc. */}
      <button onClick={onLogout}>Logout</button>
    </div>
  );
};

export default Dashboard;
