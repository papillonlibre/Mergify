// Callback.js
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTokenFromUrl } from '../utils/spotifyAuthLogic';
import spotifyApi from '../utils/spotify';

const Callback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = getTokenFromUrl();
    if (token) {
      localStorage.setItem('spotify_access_token', token);
      spotifyApi.setAccessToken(token);
      navigate('/dashboard'); // go to main app logic
    } else {
      navigate('/'); // fallback to login
    }
  }, [navigate]);

  return <p>Processing authentication...</p>;
};

export default Callback;
