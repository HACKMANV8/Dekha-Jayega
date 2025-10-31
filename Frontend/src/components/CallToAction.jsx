import React from "react";
import { FaFire } from "react-icons/fa";

const MakeSomethingSection = () => {
  return (
    <section
      id="make-something"
      className="relative min-h-screen bg-[#050505] text-white py-16 sm:py-24 overflow-hidden flex flex-col items-center justify-center"
    >
      {/* Background Glow (same as ProjectSection) */}
      <div
        className="absolute inset-0 z-0 scale-100 opacity-60 transition-all duration-700 
                   bg-[radial-gradient(circle_at_center,rgba(130,75,255,0.4)_0%,rgba(10,10,10,1)_80%)] 
                   blur-[180px]"
      ></div>

      {/* Text Content */}
      <div className="relative z-10 text-center">
        <h1
          className="font-Orbitron uppercase leading-tight tracking-tighter 
                     text-white text-[10vw] sm:text-[8vw] md:text-[6vw] lg:text-[5vw]"
        >
          LET’S MAKE
          <br />
          SOMETHING{" "}
          <FaFire className="inline text-orange-500 mb-2 ml-2 animate-pulse" />
        </h1>
      </div>
    </section>
  );
};

export default MakeSomethingSection;
