import React from 'react'
import {Route,Routes} from 'react-router-dom'
import Home from './pages/Home'
import Agents from './pages/Agents'
import Dashboard from './pages/Dashboard'

import ContactUs from './pages/ContactUs'
import Signup from './pages/SignUp'
import RenderPrepAgent from './pages/RenderPrepAgent'
import Utility from './pages/Utility'
const App = () => {
  return (
    <div >
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
  )
}

export default App
