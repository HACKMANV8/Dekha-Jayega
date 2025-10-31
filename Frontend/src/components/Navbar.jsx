// src/components/Navbar.jsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { HiMenu, HiX } from 'react-icons/hi';
import logo from '../assets/assets';

const Navbar = () => {
  const [navOpen, setNavOpen] = useState(false);
  const [showNavbar, setShowNavbar] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);
  const [isScrolled, setIsScrolled] = useState(false);

  // Scroll listener to toggle navbar visibility
  useEffect(() => {
    const handleScroll = () => {
      const currentScroll = window.scrollY;

      // detect scroll direction
      if (currentScroll > lastScrollY && currentScroll > 100) {
        setShowNavbar(false); // scrolling down hides navbar
      } else {
        setShowNavbar(true); // scrolling up shows navbar
      }

      // Add background when scrolled
      if (currentScroll > 50) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }

      setLastScrollY(currentScroll);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [lastScrollY]);

  const NavLinks = () => (
    <>
      <li><Link to="/agents" className="hover:text-gray-300">SAGA AGENTS</Link></li>
      <li><Link to="/renderprepagent" className="hover:text-gray-300">RENDERPREP AGENTS</Link></li>
      <li><Link to="/dashboard" className="hover:text-gray-300">DASHBOARD</Link></li>
      <li><Link to="/utility" className="hover:text-gray-300">UTILITY</Link></li>
    </>
  );

  return (
    <>
      <nav
        className={`
          fixed top-0 left-0 z-50 flex h-20 w-full items-center justify-between px-6 py-4 text-sm font-medium uppercase tracking-wider text-white lg:px-12
          transition-all duration-500 ease-in-out
          ${showNavbar ? 'translate-y-0' : '-translate-y-full'}
          ${isScrolled
            ? 'bg-black/70 backdrop-blur-md shadow-lg'
            : 'bg-transparent'}
        `}
      >
        {/* Logo */}
        <div className='flex items-center'>
          <div className="z-50">
            <Link to="/">
              <img src={logo} alt="Project X Logo" className="h-10 w-auto" />
            </Link>
          </div>
          <Link to="/">
            <div className='p-1 font-Orbitron font-black text-2xl'>
              Project X
            </div>
          </Link>
        </div>

        {/* Desktop Nav Links */}
        <ul className="hidden list-none items-center gap-12 md:flex">
          <NavLinks />
        </ul>

        {/* Desktop Button */}
        <div className="hidden md:block">
          <Link
            to="/contactus"
            className="rounded-full border border-brand-purple px-7 py-3 text-brand-purple transition-all hover:bg-brand-purple hover:text-white"
          >
            GET IN TOUCH
          </Link>
        </div>

        {/* Mobile Menu Button */}
        <div className="z-50 md:hidden">
          <button onClick={() => setNavOpen(!navOpen)}>
            {navOpen ? <HiX size={30} /> : <HiMenu size={30} />}
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div
        className={`fixed top-0 left-0 z-40 flex h-screen w-full flex-col items-center justify-center gap-8 bg-black/90 transition-transform duration-300 ease-in-out md:hidden ${
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
