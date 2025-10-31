// src/components/Navbar.jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { HiMenu, HiX } from 'react-icons/hi'; // Icons for hamburger menu
import logo from '../assets/assets'
const Navbar = () => {
  const [navOpen, setNavOpen] = useState(false);

 
  const NavLinks = () => (
    <>
      <li><Link to="/agents" className="hover:text-gray-300">SAGA AGENTS</Link></li>
      <li><Link to="/renderprepagent" className="hover:text-gray-300">RENDERPREP AGENTS</Link></li>
      <li><Link to="/workflow" className="hover:text-gray-300">WORKFLOW</Link></li>
      <li><Link to="/dashboard" className="hover:text-gray-300">DASHBOARD</Link></li>
      <li><Link to="/utility" className="hover:text-gray-300">UTILITY</Link></li>
      <li><Link to="/contactus" className="hover:text-gray-300">CONTACT US</Link></li>
      
    </>
  );

  return (
    <>
      <nav className="absolute top-0 left-0 z-50 flex h-24 w-full items-center justify-between px-6 py-4 text-sm font-medium uppercase tracking-wider text-white lg:px-12">
        {/* Logo */}
        <div className='flex'>
        <div className="z-50">
          <Link to="/">
            {/* --- UPDATE THIS --- */}
            <img src={logo} alt="Project X Logo" className="h-13 w-auto" />
          </Link>
          
        </div>
        <div className='p-1 font-Orbitron font-black text-2xl'>
           Project  X 
        </div></div>
        {/* Desktop Nav Links */}
        <ul className="hidden list-none items-center gap-12 md:flex">
          <NavLinks />
        </ul>

        {/* Desktop Get in Touch Button */}
        <div className="hidden md:block">
          <Link
            to="/contactus"
            className="rounded-full border border-brand-purple px-7 py-3 text-brand-purple transition-all hover:bg-brand-purple hover:text-white"
          >
            GET IN TOUCH
          </Link>
        </div>

        {/* Hamburger Menu Button (Mobile) */}
        <div className="z-50 md:hidden">
          <button onClick={() => setNavOpen(!navOpen)}>
            {navOpen ? <HiX size={30} /> : <HiMenu size={30} />}
          </button>
        </div>
      </nav>

      {/* Mobile Menu (Fullscreen Overlay) */}
      <div
        className={`fixed top-0 left-0 z-40 flex h-screen w-full flex-col items-center justify-center gap-8 bg-brand-dark transition-transform duration-300 ease-in-out md:hidden ${
          navOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <ul className="flex list-none flex-col items-center gap-8 text-xl uppercase text-white">
          <NavLinks />
        </ul>
        <Link
          to="/contactus"
          className="rounded-full border border-brand-purple px-8 py-4 text-xl uppercase text-brand-purple transition-all hover:bg-brand-purple hover:text-white"
          onClick={() => setNavOpen(false)}
        >
          GET IN TOUCH
        </Link>
      </div>
    </>
  );
};

export default Navbar;