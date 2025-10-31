import React, { useState } from 'react';
import Navbar from '../components/Navbar'
import { FilmIcon,EditIcon,CheckIcon,ChevronRightIcon,ChevronLeftIcon } from 'lucide-react';

// Regenerate Icon
const RefreshIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0 0v4.992m0 0h-4.992" />
  </svg>
);



// // Visualization Icon
const GraphIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6a7.5 7.5 0 107.5 7.5h-7.5V6z" />
    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0013.5 3v7.5z" />
  </svg>
);



const SagaAgent = () => {
  const sections = [
    'Concept', 'World Lore', 'Factions', 'Characters', 'Plot Arcs', 'Questlines', 'Dialogue'
  ];

  // State to manage which step is active
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const currentSection = sections[currentStepIndex];

  // Mock content and edit state for each section
  const [content, setContent] = useState({
    'Concept': "A detective in 1920s Chicago discovers a vast conspiracy...",
    'World Lore': "Generated history, geography, and magical systems...",
    'Factions': "Details of major and minor factions...",
    'Characters': "Character profiles, backstories, motivations...",
    'Plot Arcs': "Main story arcs and major plot points...",
    'Questlines': "Detailed quest chains, objectives...",
    'Dialogue': "Generated dialogue trees..."
  });

  const handleContentChange = (section, value) => {
    setContent(prev => ({ ...prev, [section]: value }));
  };

  const goToNextStep = () => {
    setCurrentStepIndex(prev => Math.min(prev + 1, sections.length - 1));
  };

  const goToPrevStep = () => {
    setCurrentStepIndex(prev => Math.max(prev - 1, 0));
  };

  return (
    <>
    <Navbar/>
      {/* Main container with Hero styling */}
      <div className="min-h-screen bg-[#050505] text-white relative overflow-hidden">
        {/* Background glow (Copied from HeroSection) */}
        <div
          className="hero-glow absolute inset-0 z-0 scale-100 opacity-60 transition-all duration-700 
                       bg-[radial-gradient(circle_at_center,rgba(130,75,255,0.4)_0%,rgba(10,10,10,1)_80%)] 
                       blur-[180px]"
        ></div>

        {/* Content Wrapper */}
        <div className="relative z-10 container mx-auto px-4 py-16 sm:py-24">
          {/* Header */}
          <div className="pt-16 pb-8 text-center">
            <div className="flex items-center justify-center gap-2 mb-2">
              <FilmIcon className="w-8 h-8 text-purple-400" />
              <h1 className="text-4xl font-bold text-white">SagaAgent Interface</h1>
            </div>
            <p className="text-gray-300 text-sm">
              Manage and edit the AI-generated narrative
            </p>
          </div>

          {/* Wizard Card */}
          <div className="max-w-4xl mx-auto bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl shadow-2xl overflow-hidden">
            
            {/* 1. Stepper Header */}
            <div className=" p-8  border-b  border-purple-500/30">
              <div className="flex items-center" aria-label="Progress">
                {sections.map((section, index) => (
                  <React.Fragment key={section}>
                    <div className="relative">
                      <div className={`flex items-center justify-center w-8 h-8 rounded-full transition-colors
                        ${index === currentStepIndex
                          ? 'bg-purple-600 ring-2 ring-purple-400'
                          : index < currentStepIndex
                          ? 'bg-green-600' // Completed
                          : 'bg-gray-700' // Upcoming
                        }`}
                      >
                        {index < currentStepIndex ? (
                          <CheckIcon className="w-5 h-5 text-white" />
                        ) : (
                          <span className={`${index === currentStepIndex ? 'text-white' : 'text-gray-400'}`}>
                            {index + 1}
                          </span>
                        )}
                      </div>
                      <p className={`absolute -bottom-7 text-xs font-medium ${index === currentStepIndex ? 'text-purple-300' : 'text-gray-400'}`}>
                        {section.split(' ')[0]} {/* Shorten name for mobile */}
                      </p>
                    </div>
                    {index < sections.length - 1 && (
                      <div className={`flex-auto border-t-2 transition-colors ${index < currentStepIndex ? 'border-green-600' : 'border-gray-700'}`} />
                    )}
                  </React.Fragment>
                ))}
              </div>
            </div>

            {/* 2. Step Content */}
            <div className="p-8 mt-2 sm:p-6">
              <h2 className="text-3xl font-bold text-white text-center mb-6">
                {currentSection}
              </h2>

              {/* Inline text editing */}
              <textarea
                className="w-full px-4 py-8 bg-gray-800/70 border border-gray-600 rounded-lg text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 resize-y"
                rows="8"
                value={content[currentSection]}
                onChange={(e) => handleContentChange(currentSection, e.target.value)}
              />

              {/* Visualization Tools (Conditional) */}
              {(currentSection === 'Characters' || currentSection === 'Plot Arcs' || currentSection === 'Questlines') && (
                <div className="mt-6">
                  <h3 className="text-lg font-semibold text-gray-200 mb-3">Visualization</h3>
                  <div className="p-4 bg-gray-800/70 border border-gray-600 rounded-lg flex items-center gap-3">
                    <GraphIcon className="w-5 h-5 text-purple-400" />
                    <p className="text-gray-300">
                      {currentSection === 'Characters'
                        ? 'Character relationship graph placeholder'
                        : 'Timeline or quest flow diagram placeholder'}
                    </p>
                  </div>
                </div>
              )}

              {/* HITL Controls */}
              <div className="flex flex-wrap items-center gap-3 mt-6">
                <button className="flex items-center gap-2 px-4 py-2 bg-green-600/80 text-white hover:bg-green-700 rounded-lg transition-colors text-sm font-medium">
                  <CheckIcon className="w-4 h-4" /> Approve
                </button>
                <button className="flex items-center gap-2 px-4 py-2 bg-yellow-600/80 text-white hover:bg-yellow-700 rounded-lg transition-colors text-sm font-medium">
                  <RefreshIcon className="w-4 h-4" /> Regenerate
                </button>
                <button className="flex items-center gap-2 px-4 py-2 bg-blue-600/80 text-white hover:bg-blue-700 rounded-lg transition-colors text-sm font-medium">
                  <EditIcon className="w-4 h-4" /> Save Edit
                </button>
              </div>
            </div>

            {/* 3. Navigation Footer */}
            <div className="flex justify-between items-center p-5 sm:p-6 border-t border-purple-500/30">
              <button
                onClick={goToPrevStep}
                disabled={currentStepIndex === 0}
                className="flex items-center gap-2 px-4 py-2 bg-gray-600/80 text-white rounded-lg transition-colors text-sm font-medium hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronLeftIcon className="w-4 h-4" />
                Previous
              </button>
              
              <span className="text-sm text-gray-400">
                Step {currentStepIndex + 1} of {sections.length}
              </span>

              <button
                onClick={goToNextStep}
                disabled={currentStepIndex === sections.length - 1}
                className="flex items-center gap-2 px-4 py-2 bg-purple-600/80 text-white rounded-lg transition-colors text-sm font-medium hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
                <ChevronRightIcon className="w-4 h-4" />
              </button>
            </div>

          </div>
        </div>
      </div>
    </>
  );
};

export default SagaAgent;

