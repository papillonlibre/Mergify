import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SpotifyAuth from './components/SpotifyAuth';
import Callback from './components/Callback';
import Dashboard from './components/Dashboard'; // main app after auth

function App() {
  console.log(process.env.PUBLIC_URL);
  return (
    <Router basename={process.env.PUBLIC_URL || "/"}> {/* this will work locally */}
      <Routes>
        <Route path="/" element={<SpotifyAuth />} />
        <Route path="/callback" element={<Callback />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
