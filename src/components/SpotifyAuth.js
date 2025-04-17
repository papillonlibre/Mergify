// SpotifyAuth.js
import React, { useEffect, useState } from 'react';
import spotifyApi from '../utils/spotify';
import Header from './Header'

const SpotifyAuth = () => {
  const [token, setToken] = useState(localStorage.getItem('spotify_access_token'));

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (code && !token) {
      // Exchange code with Flask backend for access token
      fetch(`http://localhost:5000/callback?code=${code}`)
        .then(res => res.json())
        .then(data => {
          if (data.access_token) {
            localStorage.setItem('spotify_access_token', data.access_token);
            setToken(data.access_token);
            spotifyApi.setAccessToken(data.access_token);

            // Clean up the URL after auth
            window.history.replaceState({}, document.title, "/");
          } else {
            console.error("Failed to get token:", data);
          }
        })
        .catch(err => console.error("Error during token fetch:", err));
    }
  }, [token]);

  const handleLogin = () => {
    window.location.assign("http://localhost:5000/login");
  };

  const handleLogout = () => {
    localStorage.removeItem('spotify_access_token');
    setToken(null);
    spotifyApi.setAccessToken(null);
  };


return (
  <div className="flex items-center justify-center min-h-screen">
    <div className="text-center">
      <Header />
      {token ? (
        <button onClick={handleLogout}>Logout</button>
      ) : (
        // <button onClick={handleLogin}>Login to Spotify</button>
        <button onClick={handleLogin} type="button" class="text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700">Login to Spotify</button>
      )}
      <h1 className="text-4xl font-bold text-blue-500 mt-10">
        Tailwind is Working! 🎉
      </h1>
    </div>
  </div>
);
};


export default SpotifyAuth;
