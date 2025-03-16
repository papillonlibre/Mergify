// SpotifyAuth.js
import React, { useEffect } from 'react';
import spotifyApi from './spotify';

const CLIENT_ID = '141d8896106f454abbf04bb2c5789ab4';
const REDIRECT_URI = 'https://papillonlibre.github.io/Mergify/';
const AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize';
const RESPONSE_TYPE = 'token';

const SpotifyAuth = () => {
  useEffect(() => {
    const hash = window.location.hash;
    let token = localStorage.getItem('spotify_access_token');

    if (!token && hash) {
      token = hash.substring(1).split('&').find(elem => elem.startsWith('access_token')).split('=')[1];
      window.location.hash = '';
      localStorage.setItem('spotify_access_token', token);
    }

    if (token) {
      spotifyApi.setAccessToken(token);
    }
  }, []);

  const handleLogin = () => {
    window.location.href = `${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=${RESPONSE_TYPE}`;
  };

  return (
    <div>
      <h1>Spotify Lyrics App</h1>
      <button onClick={handleLogin}>Login to Spotify</button>
    </div>
  );
};

export default SpotifyAuth;
