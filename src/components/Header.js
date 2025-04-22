import React from 'react';

const Header = () => {
  return (
      <header className="bg-gradient-to-r from-green-400 to-blue-500 text-white py-8 px-6 text-center rounded-xl shadow-lg max-w-3xl mx-auto mt-16">
        <h1 className="text-4xl font-bold mb-3">Mergify</h1>
        <p className="text-lg">
          Merge multiple playlists into one effortlessly, and discover which of your liked songs match playlists in your library.
        </p>
    </header>
  );
};

export default Header;
