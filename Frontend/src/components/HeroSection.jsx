import React, { useEffect, useRef } from "react";
import { FaArrowRight } from "react-icons/fa";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

const HeroSection = () => {
  const headingRef = useRef(null);
  const subTextRef = useRef(null);
  const buttonRef = useRef(null);
  const illustrationRef = useRef(null);

  useEffect(() => {
    const tl = gsap.timeline();

    // --- Initial entrance animation ---
    gsap.set([headingRef.current, subTextRef.current], { opacity: 0, y: 100 });
    gsap.set(buttonRef.current, { opacity: 0, scale: 0.8 });
    gsap.set(illustrationRef.current, { opacity: 0, y: 50 });

    tl.to(headingRef.current, {
      opacity: 1,
      y: 0,
      duration: 1.2,
      ease: "power3.out",
    })
      .to(
        subTextRef.current,
        { opacity: 1, y: 0, duration: 1, ease: "power3.out" },
        "-=0.8"
      )
      .to(
        illustrationRef.current,
        { opacity: 1, y: 0, duration: 1.5, ease: "power2.out" },
        "-=0.5"
      )
      .to(
        buttonRef.current,
        { opacity: 1, scale: 1, duration: 0.8, ease: "back.out(1.7)" },
        "-=0.8"
      );

    
    gsap.to(illustrationRef.current, {
      y: -20,
      duration: 3,
      ease: "power1.inOut",
      yoyo: true,
      repeat: -1,
    });

   
// Set initial state
gsap.set(".hero-text", {
  scale: 1,
  opacity: 1,
  filter: "blur(0px)",
  transformOrigin: "center center",
});

// --- Scale + blur (phase 1: scroll begins) ---
gsap.to(".hero-text", {
  scale: 0.85,
  filter: "blur(0px)",
  ease: "none",
  scrollTrigger: {
    trigger: "#hero",
    start: "top top",
    end: "center center",
    scrub: 1,
    // markers: true,
  },
});

// --- Fade-out (phase 2: slow dissolve after scaling) ---
gsap.to(".hero-text", {
  opacity: 0,
  filter: "blur(0px)",
  ease: "none",
  scrollTrigger: {
    trigger: "#hero",
    start: "30%",
    end: "bottom top+=200",
    scrub: 1,
    // markers: true,
  },
});



    // --- Keep the glow expansion effect ---
    gsap.to(".hero-glow", {
      scale: 1.8,
      opacity: 1,
      filter: "blur(220px)",
      scrollTrigger: {
        trigger: "#hero",
        start: "top top",
        end: "bottom top",
        scrub: true,
      },
    });

    // --- Scale + blur hero text while scrolling down ---
    gsap.to([headingRef.current, subTextRef.current], {
      scale: 1.4, // enlarge
      filter: "blur(0px)",
      transformOrigin: "center center",
      ease: "power2.out",
      scrollTrigger: {
        trigger: "#hero",
        start: "top top",
        end: "bottom top",
        scrub: true,
        onLeaveBack: () => {
          gsap.set([headingRef.current, subTextRef.current], {
            scale: 1,
            filter: "blur(0px)",
          });
        },
      },
    });
  }, []);

  return (
    <section
      id="hero"
      className="relative min-h-screen w-full overflow-hidden bg-[#050505] text-white"
    >
      {/* 🔮 Background glow */}
      <div
        className="hero-glow absolute inset-0 z-0 scale-100 opacity-60 transition-all duration-700 
                   bg-[radial-gradient(circle_at_center,rgba(130,75,255,0.4)_0%,rgba(10,10,10,1)_80%)] 
                   blur-[180px]"
      ></div>

      {/* 🪐 Text content */}
      <div className="relative z-10 flex min-h-screen flex-col items-center justify-center px-5 py-20 text-center">
        <h1
          ref={headingRef}
          className="hero-text font-Orbitron uppercase text-white 
                     leading-tight tracking-tighter text-[5vw] sm:text-5xl md:text-7xl lg:text-8xl xl:text-8xl mb-4"
        >
          From Imagination to
        </h1>

        <h2
          ref={subTextRef}
          className="hero-text font-Manrope font-medium uppercase leading-tight tracking-tighter 
                  text-transparent bg-clip-text bg-linear-to-r from-white to-purple-500
                    text-[3vw] sm:text-4xl md:text-7xl lg:text-7xl xl:text-8xl"
        >
          Interactive Worlds
        </h2>
      </div>

      {/* 🐼 Illustration */}
      <div
        ref={illustrationRef}
        className="absolute bottom-[-10vh] left-1/2 z-10 w-[80vw] max-w-[1000px] 
                   -translate-x-1/2 pointer-events-none lg:w-[60vw] opacity-90"
      >
        <img src="/project-x-illustration.png" alt="Project X Illustration" />
      </div>

      {/* 🌫️ Soft reflection glow */}
      <div
        className="absolute bottom-[-5vh] left-1/2 z-0 h-[40vh] w-[80vw] -translate-x-1/2 
                   rounded-full bg-[radial-gradient(circle_at_center,rgba(110,64,255,0.35)_0%,transparent_70%)]
                   blur-[120px] opacity-70"
      ></div>

      
      
    </section>
  );
};

export default HeroSection;
