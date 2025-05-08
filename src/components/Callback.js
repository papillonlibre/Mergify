import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Callback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // When the user is redirected back from Spotify,
    // the Flask backend has already handled token exchange
    navigate('/dashboard');
  }, [navigate]);

  return (
    <div className="h-screen flex items-center justify-center">
      <p className="text-lg text-gray-600">Processing Spotify authentication...</p>
    </div>
  );
};

export default Callback;
