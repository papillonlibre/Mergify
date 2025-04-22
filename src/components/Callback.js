import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import spotifyApi from '../utils/spotify';

const Callback = () => {
  const navigate = useNavigate();
  const hasFetched = useRef(false); // <-- import useRef

  useEffect(() => {
    if (hasFetched.current) return;
    hasFetched.current = true;

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

  return (
    <div className="h-screen flex items-center justify-center">
  <p className="text-lg text-gray-600">Processing Spotify authentication...</p>
</div>
  )
};


export default Callback;