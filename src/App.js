import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SpotifyAuth from './components/SpotifyAuth';
import Callback from './components/Callback';
import Dashboard from './components/Dashboard'; // main app after auth
import PageNotFound from './components/PageNotFound';

function App() {
  const isProduction = window.location.hostname === "papillonlibre.github.io";
  const basename = isProduction ? "/Mergify" : "/";  // "/" for local, "/Mergify" for production
  return (
    <Router basename={basename}>
      <Routes>
        <Route path="/" element={<SpotifyAuth />} />
        <Route path="/callback" element={<Callback />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </Router>
  );
}

export default App;