// SpotifyAuth.js
import React, { useEffect, useState } from 'react';
import spotifyApi from '../utils/spotify';
import { getSpotifyAuthUrl, getTokenFromUrl } from '../utils/spotifyAuthLogic';

const SpotifyAuth = () => {
  const [token, setToken] = useState(localStorage.getItem('spotify_access_token')); // retrieves token if the user has logged in before
  useEffect(() => {
    const tokenFromUrl = getTokenFromUrl();
    if (tokenFromUrl) {
      localStorage.setItem('spotify_access_token', tokenFromUrl);
      setToken(tokenFromUrl);
      spotifyApi.setAccessToken(tokenFromUrl);
    }
  }, []);

  const handleLogin = () => { // redirects user to Spotify login if they are not already logged in
    window.location.assign(getSpotifyAuthUrl());
  };

  const handleLogout = () => {
    localStorage.removeItem('spotify_access_token');
    setToken(null);
    spotifyApi.setAccessToken(null);
  };

  return (
    <div>
      <h1>Mergify</h1>
      {token ? (
        <button onClick={handleLogout}>Logout</button>
      ) : (
        <button onClick={handleLogin}>Login to Spotify</button>
      )}
    </div>
  );
};

export default SpotifyAuth;
