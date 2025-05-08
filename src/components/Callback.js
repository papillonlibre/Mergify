import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Callback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
  
    if (code) {
      fetch('http://localhost:5000/exchange_token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.access_token) {
            localStorage.setItem('spotify_access_token', data.access_token);
            localStorage.setItem('spotify_refresh_token', data.refresh_token);
            navigate('/dashboard');
          } else {
            console.error('Error retrieving access token');
          }
        })
        .catch((error) => console.error('Error exchanging token:', error));
    }
  }, [navigate]);
  
  return (
    <div className="h-screen flex items-center justify-center">
      <p className="text-lg text-gray-600">Processing Spotify authentication...</p>
    </div>
  );
};

export default Callback;
