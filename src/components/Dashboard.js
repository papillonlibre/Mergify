import React, { useEffect, useState } from 'react';

const Dashboard = () => {
  const [topArtists, setTopArtists] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('spotify_access_token');
    console.log("Token being used:", token); // Log the token being used
    
    if (!token) {
      setLoading(false);
      return;
    }

    fetch('http://localhost:5000/user/top-artists', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(data => {
        console.log(data)
        if (data && typeof data === 'object' && (data.short_term || data.medium_term || data.long_term)) {
          console.log("The typing seems right")
          setTopArtists(data); // Store entire object for potential future use
        } else {
          console.error('Unexpected data shape:', data);
        }
      })
      .catch(err => console.error('Fetch failed:', err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h2 className="text-2xl font-semibold mb-4 text-center">Your Dashboard</h2>

      {/* Top Artists Banner */}
      <div className="flex items-center bg-cyan-100 p-6 rounded-lg shadow mb-6">
        <div className="mb-4">
          <h3 className="text-lg font-medium">Your Top Artists</h3>
          <span className="text-sm text-gray-600 block">(Last 4 Weeks)</span>
        </div>
        {loading ? (
          <div className="w-full flex justify-center">
            <p className="text-gray-500">Loading...</p>
          </div>
        ) : topArtists.long_term?.length > 0 ? (
          <div className="overflow-x-auto">
            <div className="flex space-x-4">
              {topArtists.long_term.map((artist, idx) => (
                <div key={idx} className="min-w-[120px] flex-shrink-0 text-center">
                  {artist.image && (
                    <img
                      src={artist.image}
                      alt={artist.name}
                      className="w-24 h-24 object-cover rounded-full mx-auto"
                    />
                  )}
                  <p className="mt-2 font-medium">{artist.name}</p>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="w-full flex justify-center">
            <p className="text-gray-500">No top artists found.</p>
          </div>
        )}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-cyan-50 p-4 rounded-lg shadow text-center">Liked Songs Analysis</div>
        <div className="bg-cyan-50 p-4 rounded-lg shadow text-center">Merge Playlists</div>
      </div>
    </div>
  );
};

export default Dashboard;
