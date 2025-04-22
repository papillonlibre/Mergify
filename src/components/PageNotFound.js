import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import Header from './Header';

const PageNotFound = () => {
  const location = useLocation();
  const [redirectPath, setRedirectPath] = useState('/');

  useEffect(() => {
    const token = localStorage.getItem('spotify_access_token');
    if (token) {
      setRedirectPath('/dashboard');
    }
  }, []);

  return (
    <div className="flex flex-col items-center justify-start min-h-screen pt-10 bg-white">
      <Header />
      <div className="text-center mt-10">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">404 - Not Found</h1>
        <p className="text-gray-500 mb-4">
          No match for <code className="font-mono text-blue-500">{location.pathname}</code>
        </p>
        <Link
          to={redirectPath}
          className="inline-block mt-4 px-6 py-2 text-white bg-green-500 hover:bg-green-600 rounded-lg shadow-md transition duration-300"
        >
          Go to Homepage
        </Link>
      </div>
    </div>
  );
};

export default PageNotFound;
