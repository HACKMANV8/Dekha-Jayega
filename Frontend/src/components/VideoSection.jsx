import React from "react";

const VideoSection = () => {
  return (
    <section
      id="showreel"
      className="relative flex flex-col justify-start min-h-screen bg-[#050505] text-white overflow-hidden pt-20"
    >
     
      <div
        className="hero-glow absolute inset-0 z-0 scale-100 opacity-60 transition-all duration-700 
                   bg-[radial-gradient(circle_at_center,rgba(130,75,255,0.4)_0%,rgba(10,10,10,1)_80%)] 
                   blur-[180px]"
      ></div>

     
      <h2 className="p-5  font-Manrope font-medium uppercase leading-tight tracking-tighter 
                  text-transparent bg-clip-text bg-linear-to-r from-white to-purple-500
                    text-[3vw] sm:text-4xl md:text-7xl lg:text-7xl ">
        Watch Our Showreel
      </h2>

      {/* Video Container (centered in remaining space) */}
      <div className="relative z-10 w-full flex-1 flex items-center justify-center px-10 pb-10 pt-10">
        <div className="relative w-full md:w-[80%] lg:w-[70%] rounded-[2rem] overflow-hidden bg-[#5a5563]/50 flex items-center justify-center">
          {/* Changed back to img tag since the src is a .png */}
          <video
            src="/showreel-preview.png"
            alt="Showreel Thumbnail"
            className="w-full h-auto opacity-80"
          />

          {/* Play Button */}
          <button
            className="absolute flex flex-col items-center justify-center rounded-full border border-white/50 text-white 
                       hover:bg-white hover:text-black transition-all duration-300 w-20 h-20 md:w-28 md:h-28"
          >
            {/* Replaced FaPlay with an inline SVG icon */}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-6 h-6 md:w-8 md:h-8 ml-1" // Added ml-1 for better visual centering
            >
              <path d="M7 6v12l10-6z"></path>
            </svg>
          </button>
        </div>
      </div>

      
      
    </section>
  );
};

export default VideoSection;

