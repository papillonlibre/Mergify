// Dashboard.js
import React from 'react';

const Dashboard = () => {
  // return <h2>You're logged in. Now we can do cool Spotify stuff here!</h2>;
  return (
    <div className="p-6 max-w-6xl mx-auto">
  <h2 className="text-2xl font-semibold mb-4">Your Dashboard</h2>
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div className="bg-white p-4 rounded-lg shadow">Liked Songs Analysis</div>
    <div className="bg-white p-4 rounded-lg shadow">Merge Playlists</div>
  </div>
</div>

  )
};

export default Dashboard;
