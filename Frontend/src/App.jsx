import React from 'react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { useEffect } from 'react';

import Home from './pages/Home';
import Agents from './pages/Agents';
import Dashboard from './pages/Dashboard';
import ContactUs from './pages/ContactUs';
import Signup from './pages/SignUp';
import RenderPrepAgent from './pages/RenderPrepAgent';
import Utility from './pages/Utility';

// ✅ ScrollToTop Component (included here directly)
const ScrollToTop = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    // Smoothly scroll to top whenever route changes
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [pathname]);

  return null;
};

const App = () => {
  return (
    <div>
      {/* Auto scroll to top when switching routes */}
      <ScrollToTop />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/contactus" element={<ContactUs />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/renderprepagent" element={<RenderPrepAgent />} />
        <Route path="/utility" element={<Utility />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </div>
  );
};

export default App;
