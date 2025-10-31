import React, { useState } from 'react';
import { FilmIcon } from 'lucide-react';
import Navbar from '../components/Navbar';

const Agents = () => {
  const [storyTopic, setStoryTopic] = useState('');
  const [research, setResearch] = useState('No Research');
  const [filmLength, setFilmLength] = useState('90');
  const [numScenes, setNumScenes] = useState('12');

  return (
    <>
      <Navbar />
      {/* Main container with Hero styling */}
      <div className="min-h-screen bg-[#050505] text-white relative overflow-hidden">
        {/* Background glow (Copied from HeroSection) */}
        <div
          className="hero-glow absolute inset-0 z-0 scale-100 opacity-60 transition-all duration-700 
                     bg-[radial-gradient(circle_at_center,rgba(130,75,255,0.4)_0%,rgba(10,10,10,1)_80%)] 
                     blur-[180px]"
        ></div>

        {/* Content Wrapper */}
        <div className="relative z-10">
          {/* Header */}
          <div className="pt-32 pb-8 text-center"> {/* Increased top padding to pt-32 */}
            <div className="flex items-center justify-center gap-2 mb-2">
              <FilmIcon className="w-8 h-8 text-purple-400" />
              <h1 className="text-4xl font-bold text-white">ScriptEngine</h1>
            </div>
            <p className="text-gray-300 text-sm">
              AI-Powered Creative Writing Platform
            </p>
          </div>

          {/* Main Form Container */}
          <div className="flex items-center justify-center px-4 py-8">
            {/* "Glassmorphism" card */}
            <div className="bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl shadow-2xl p-8 sm:p-12 w-full max-w-3xl">
              <h2 className="text-3xl font-bold text-white text-center mb-4">
                Create Your Story
              </h2>
              <p className="text-gray-300 text-center mb-8">
                Start by describing your story idea. Our AI will help you
                develop it into a complete screenplay.
              </p>

              {/* Story Topic */}
              <div className="mb-6">
                <label className="block text-gray-200 font-medium mb-2">
                  Story Topic
                </label>
                <textarea
                  className="w-full px-4 py-3 bg-gray-800/70 border border-gray-600 rounded-lg text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 resize-none"
                  rows="4"
                  placeholder="Describe your story idea... (e.g., 'A detective in 1920s Chicago discovers a conspiracy')"
                  value={storyTopic}
                  onChange={(e) => setStoryTopic(e.target.value)}
                />
              </div>

              {/* Research Required */}
              <div className="mb-6">
                <label className="block text-gray-200 font-medium mb-2">
                  Research Required
                </label>
                <select
                  className="w-full px-4 py-3 bg-gray-800/70 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                  value={research}
                  onChange={(e) => setResearch(e.target.value)}
                >
                  <option className="text-black">No Research</option>
                  <option className="text-black">Light Research</option>
                  <option className="text-black">Moderate Research</option>
                  <option className="text-black">Extensive Research</option>
                </select>
              </div>

              {/* Film Length and Number of Scenes */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
                <div>
                  <label className="block text-gray-200 font-medium mb-2">
                    Film Length (seconds)
                  </label>
                  <input
                    type="number"
                    className="w-full px-4 py-3 bg-gray-800/70 border border-gray-600 rounded-lg text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                    value={filmLength}
                    onChange={(e) => setFilmLength(e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-gray-200 font-medium mb-2">
                    Number of Scenes
                  </label>
                  <input
                    type="number"
                    className="w-full px-4 py-3 bg-gray-800/70 border border-gray-600 rounded-lg text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                    value={numScenes}
                    onChange={(e) => setNumScenes(e.target.value)}
                  />
                </div>
              </div>

              {/* Submit Button */}
              <button className="w-full px-6 py-3 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center gap-2">
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                </svg>
                Start Creating
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Agents;