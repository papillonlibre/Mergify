// SpotifyAuth.js
import React, { useEffect, useState } from 'react';
import spotifyApi from '../utils/spotify';
import Header from './Header'
import Button from './Button';

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
    <div className="min-h-screen flex flex-col items-center justify-center px-4 bg-white">
      <Header />
      <div className="mt-8">
        {token ? (
          <Button onClick={handleLogout} label="Logout" />
        ) : (
          <Button onClick={handleLogin} label="Login with Spotify" />
        )}
      </div>
    </div>
  );
};


export default SpotifyAuth;
