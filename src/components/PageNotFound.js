import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import Header from './Header';
import Button from './Button';

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
          No match for route <code className="font-mono text-blue-500">{location.pathname}</code>
        </p>
        <Link to={redirectPath} className="mt-4">
          <Button label="Go to Homepage" color="gray" />
        </Link>
      </div>
    </div>
  );
};

export default PageNotFound;
