
import React, { useState } from 'react';
import Navbar from '../components/Navbar'
import { PlayIcon,PauseIcon   } from 'lucide-react';
const StopIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 7.5A2.25 2.25 0 017.5 5.25h9a2.25 2.25 0 012.25 2.25v9a2.25 2.25 0 01-2.25 2.25h-9a2.25 2.25 0 01-2.25-2.25v-9z" />
  </svg>
);
const TABS = ['Concept', 'Narrative', 'Assets', 'Settings', 'Chat / Logs'];

const ProjectWorkspace = () => {
  const [activeTab, setActiveTab] = useState(TABS[0]);

  // Placeholder content for tabs
  const renderTabContent = () => {
    switch (activeTab) {
      case 'Concept':
        return <div className="p-8"><h2 className="text-2xl font-bold">Define High-Level Concept</h2><p className="text-gray-300 mt-4">Here you would define the genre, setting, tone, etc. This could reuse or expand upon the 'Agents' page form.</p></div>;
      case 'Narrative':
        return <div className="p-8"><h2 className="text-2xl font-bold">SagaAgent Output</h2><p className="text-gray-300 mt-4">Display generated story structure, lore, factions, characters, and quests with "Approve/Regenerate" buttons.</p></div>;
      case 'Assets':
        return <div className="p-8"><h2 className="text-2xl font-bold">RenderPrepAgent Output</h2><p className="text-gray-300 mt-4">Show generated image prompts and the resulting images/videos from models like Veo or SDXL.</p></div>;
      case 'Settings':
        return <div className="p-8"><h2 className="text-2xl font-bold">Project Settings</h2><p className="text-gray-300 mt-4">Manage model parameters, checkpoints, and Human-in-the-Loop (HITL) controls.</p></div>;
      case 'Chat / Logs':
        return <div className="p-8"><h2 className="text-2xl font-bold">Agent Logs</h2><p className="text-gray-300 mt-4">A console-like view of the conversation and logs between the user and the agents (Supervisor, SagaAgent, etc.).</p></div>;
      default:
        return null;
    }
  };

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-[#050505] text-white relative overflow-hidden">
        {/* Background glow */}
        <div
          className="hero-glow absolute inset-0 z-0 scale-100 opacity-60 transition-all duration-700 
                     bg-[radial-gradient(circle_at_center,rgba(130,75,255,0.4)_0%,rgba(10,10,10,1)_80%)] 
                     blur-[180px]"
        ></div>

        {/* Content Wrapper */}
        <div className="relative z-10 container mx-auto px-6 pt-32 pb-16">
          
          {/* Project Header & Controls */}
          <div className="flex flex-col md:flex-row justify-between md:items-center gap-4 mb-8">
            <h1 className="text-4xl font-bold font-Orbitron">Project: <span className="text-purple-400">Cyber-Noir Detective</span></h1>
            <div className="flex items-center gap-3">
              <button className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors">
                <PlayIcon className="w-5 h-5" /> Run
              </button>
              <button className="flex items-center gap-2 px-4 py-2 bg-yellow-600 hover:bg-yellow-700 rounded-lg transition-colors">
                <PauseIcon className="w-5 h-5" /> Pause
              </button>
              <button className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-colors">
                <StopIcon className="w-5 h-5" /> Stop
              </button>
            </div>
          </div>

          {/* Tabbed Interface */}
          <div className="bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl shadow-2xl overflow-hidden">
            {/* Tab Headers */}
            <div className="flex border-b border-purple-500/30">
              {TABS.map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-3 sm:px-6 font-medium text-sm sm:text-base ${
                    activeTab === tab
                      ? 'bg-purple-600/50 text-white'
                      : 'text-gray-300 hover:bg-gray-800/50'
                  } transition-colors`}
                >
                  {tab}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="min-h-[500px]">
              {renderTabContent()}
            </div>
          </div>

        </div>
      </div>
    </>
  );
};

export default ProjectWorkspace;

