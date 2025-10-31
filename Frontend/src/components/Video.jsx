import React, { useState } from 'react';

function EnhancedVideoSection({ thumbnailVideoSrc, mainVideoSrc, posterImage }) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <>
      {/* Container */}
      <div className="relative z-10 w-full flex-1 flex items-center justify-center px-10 py-10">
        {/* Glassmorphism Wrapper */}
        <div className="relative w-full md:w-[80%] lg:w-[70%] rounded-[2rem] overflow-hidden 
                       bg-black/30 backdrop-blur-md shadow-2xl">
          
          {/* Silent Preview Video */}
          <video
            src={thumbnailVideoSrc}
            poster={posterImage} // Shows this image before the video loads
            autoPlay
            loop
            muted
            playsInline // Essential for autoplay on mobile browsers
            className="w-full h-auto opacity-70"
          >
            Your browser does not support the video tag.
          </video>

          {/* Play Button */}
          <button
            onClick={openModal}
            aria-label="Play video"
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 
                       flex flex-col items-center justify-center rounded-full 
                       border-2 border-white/50 text-white 
                       w-20 h-20 md:w-28 md:h-28
                       bg-white/10 backdrop-blur-sm
                       hover:bg-white hover:text-black hover:scale-110
                       active:scale-95
                       transition-all duration-300 ease-in-out"
          >
            {/* SVG Play Icon */}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-6 h-6 md:w-8 md:h-8 ml-1" // ml-1 for optical centering
            >
              <path d="M7 6v12l10-6z"></path>
            </svg>
          </button>
        </div>
      </div>

      {/* Video Modal (Lightbox) */}
      {isModalOpen && (
        <div 
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          onClick={closeModal}
        >
          {/* Backdrop */}
          <div className="absolute inset-0 bg-black/80 backdrop-blur-sm" />

          {/* Close Button */}
          <button
            onClick={closeModal}
            aria-label="Close video player"
            className="absolute top-4 right-4 z-[60] text-white/70 hover:text-white transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-8 h-8"
            >
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>

          {/* Video Player */}
          <div 
            className="relative z-[55] w-full max-w-4xl rounded-lg overflow-hidden"
            onClick={(e) => e.stopPropagation()} // Prevents click from bubbling to backdrop
          >
            <video
              src={mainVideoSrc}
              autoPlay
              controls // Show default video controls (play, pause, volume)
              playsInline
              className="w-full h-auto"
            >
              Your browser does not support the video tag.
            </video>
          </div>
        </div>
      )}
    </>
  );
}

export default EnhancedVideoSection;