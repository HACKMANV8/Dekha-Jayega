import React from 'react'
import {Route,Routes} from 'react-router-dom'
import Home from './pages/Home'
import Agents from './pages/Agents'
import Dashboard from './pages/Dashboard'
import Workflow from './pages/Workflow'
import ContactUs from './pages/ContactUs'
import Login from './pages/Login'
import Signup from './pages/SignUp'
const App = () => {
  return (
    <div >
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/contactus" element={<ContactUs />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/workflow" element={<Workflow />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </div>
  )
}

export default App
