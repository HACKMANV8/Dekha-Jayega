import React, { useRef, useState } from "react";
import { Link } from "react-router-dom";
import SagaAgent from "../assets/SagaAgent.mp4";
import renderPrep from "../assets/renderPrep.mp4";
import utilities from "../assets/Utilities.mp4";
import { FaFire } from "react-icons/fa";

const ProjectsSection = () => {
  const videoRefs = [useRef(null), useRef(null), useRef(null)];
  const [activeVideo, setActiveVideo] = useState(null);

  const handleHover = (index) => {
    setActiveVideo(index);
    videoRefs.forEach((ref, i) => {
      const video = ref.current;
      if (!video) return;
      if (i === index) {
        video.play();
      } else {
        video.pause();
        video.currentTime = 0;
      }
    });
  };

  const handleMouseLeave = (index) => {
    const video = videoRefs[index].current;
    if (video) {
      video.pause();
      video.currentTime = 0;
    }
    setActiveVideo(null);
  };

  const projects = [
    {
      title: "SagaAgent",
      src: SagaAgent,
      link: "/agents",
    },
    {
      title: "Render PrepAgent",
      src: renderPrep,
      link: "/renderprepagent",
    },
    {
      title: "Utility",
      src: utilities,
      link: "/utility",
    },
  ];

  return (
    <section
      id="projects"
      className="relative min-h-screen bg-[#050505] text-white py-16 sm:py-24 overflow-hidden flex flex-col items-center"
    >
      {/* Background Glow */}
      <div
        className="hero-glow absolute inset-0 z-0 scale-100 opacity-60 transition-all duration-700 
                   bg-[radial-gradient(circle_at_center,rgba(130,75,255,0.4)_0%,rgba(10,10,10,1)_80%)] 
                   blur-[180px]"
      ></div>

      {/* Content Wrapper */}
      <div className="relative z-10 container mx-auto px-4 flex flex-col items-center">
        {/* Header */}
        <div className="max-w-3xl mx-auto text-center mb-16">
          <p className="text-purple-400 text-lg font-medium mb-3 flex items-center justify-center">
            Take a deep dive into some of our favorite Agents.
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-5 h-5 ml-2"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3"
              />
            </svg>
          </p>
          <p className="text-gray-300 text-lg">
            From established corporations to startups gearing to launch, we've
            seen a lot of our partners win – and we're excited to see you thrive
            too.
          </p>
        </div>

        {/* Projects Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mb-12 w-full max-w-6xl">
          {projects.map((project, index) => (
            <Link
              key={index}
              to={project.link}
              className={`group flex flex-col items-center transition-all duration-700 ${
                activeVideo !== null && activeVideo !== index
                  ? "opacity-40 scale-[0.97]"
                  : "opacity-100 scale-100"
              }`}
              onMouseEnter={() => handleHover(index)}
              onMouseLeave={() => handleMouseLeave(index)}
            >
              <div className="bg-gray-800/60 backdrop-blur-md rounded-3xl overflow-hidden shadow-xl hover:shadow-purple-500/30 transition-shadow duration-300 w-full">
                <div className="relative w-full aspect-[3/4] overflow-hidden bg-[#121212] flex items-center justify-center">
                  <video
                    ref={videoRefs[index]}
                    src={project.src}
                    className="object-cover w-full h-full transition-transform duration-500 group-hover:scale-105"
                    muted
                    playsInline
                  />
                </div>
              </div>
              <h3 className="mt-6 text-2xl font-extrabold text-white group-hover:text-purple-300 transition-colors duration-300 text-center tracking-wide">
                {project.title}
              </h3>
            </Link>
          ))}
        </div>
      </div>
      <div className="relative z-10 text-left pt-20 w-full max-w-6xl px-4">
              <h1
                className="font-Manrope font-medium uppercase leading-tight tracking-tighter 
                           text-white text-[15vw] sm:text-[12vw] md:text-[10vw] lg:text-[8vw]"
              >
                LET'S MAKE
                <br />
                SOMETHING{" "}
                <FaFire className="inline text-orange-500 mb-2 ml-2 animate-pulse" />
              </h1>
            </div>
    </section>
  );
};

export default ProjectsSection;
