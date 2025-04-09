import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import spotifyApi from '../utils/spotify';

const Callback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const searchParams = new URLSearchParams(window.location.search);
    const code = searchParams.get('code');

    if (!code) {
      navigate('/');
      return;
    }

    const fetchToken = async () => {
      try {
        const res = await fetch('http://localhost:5000/exchange_token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ code })
        });

        const data = await res.json();

        if (data.access_token) {
          localStorage.setItem('spotify_access_token', data.access_token);
          localStorage.setItem('spotify_refresh_token', data.refresh_token);
          spotifyApi.setAccessToken(data.access_token);
          navigate('/dashboard');
        } else {
          console.error('No access token returned', data);
          navigate('/');
        }
      } catch (err) {
        console.error('Error exchanging token:', err);
        navigate('/');
      }
    };

    fetchToken();
  }, [navigate]);

  return <p>Processing authentication...</p>;
};

export default Callback;
