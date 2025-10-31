import React, { useState } from 'react';
import { SearchIcon,LibraryIcon,ImageIcon,PauseIcon,PlayIcon } from 'lucide-react';
import Navbar from '../components/Navbar'

// Pipeline Icon
const PipelineIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 6.75c0 3.03-2.47 5.5-5.5 5.5S6.25 9.78 6.25 6.75S8.72 1.25 11.75 1.25s5.5 2.47 5.5 5.5zM11.75 12.25c-3.03 0-5.5 2.47-5.5 5.5s2.47 5.5 5.5 5.5 5.5-2.47 5.5-5.5-2.47-5.5-5.5-5.5zM12 8.25v3.5M12 15.75v3.5" />
    <path strokeLinecap="round" strokeLinejoin="round" d="M3.5 12h3M17.5 12h3" />
  </svg>
);

const ResetIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0 0v4.992m0 0h-4.992" />
  </svg>
);
// --- TABS ---
const TABS = {
RESEARCH: 'Research',
LIBRARY: 'Asset Library',
PIPELINE: 'Pipeline Manager',
};

const Utility = () => {
const [activeTab, setActiveTab] = useState(TABS.RESEARCH);

// --- Research Panel Component ---
const ResearchPanel = () => (
<div className="space-y-6">
    <h2 className="text-3xl font-bold text-white text-center">Research & Data Panel</h2>
    <p className="text-gray-300 text-center mb-8">
    Trigger or review web-based lore research (e.g., “research Norse mythology”).
    </p>
    
    {/* Search Bar */}
    <div className="relative">
    <input 
        type="text" 
        placeholder="Enter research query (e.g., 'Norse mythology factions')" 
        className="w-full px-4 py-3 pl-10 bg-gray-800/70 border border-gray-600 rounded-lg text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
    />
    <SearchIcon className="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
    </div>

    {/* Fetched Summaries */}
    <div>
    <h3 className="text-xl font-semibold text-gray-200 mb-3">Knowledge Panels</h3>
    <div className="p-4 bg-gray-800/70 border border-gray-600 rounded-lg min-h-[150px]">
        <p className="text-gray-400">Research results will appear here...</p>
    </div>
    </div>

    {/* Integration Preview */}
    <div>
    <h3 className="text-xl font-semibold text-gray-200 mb-3">Integration Preview</h3>
    <div className="p-4 bg-gray-800/70 border border-gray-600 rounded-lg min-h-[100px]">
        <p className="text-gray-400">Context-aware integration suggestions...</p>
    </div>
    </div>
</div>
);

// --- Asset Library Component ---
const AssetLibrary = () => (
<div className="space-y-6">
    <h2 className="text-3xl font-bold text-white text-center">Asset Library & Gallery</h2>
    <p className="text-gray-300 text-center mb-8">
    Repository for all generated and approved visual assets.
    </p>

    {/* Filters */}
    <div className="flex flex-wrap items-center justify-center gap-2">
    {['All', 'Character', 'Environment', 'Item', 'Scene'].map(filter => (
        <button 
        key={filter} 
        className="px-4 py-2 bg-gray-800/70 border border-gray-600 rounded-lg text-sm text-gray-300 hover:bg-purple-600/50 hover:text-white focus:bg-purple-600 focus:text-white transition-colors"
        >
        {filter}
        </button>
    ))}
    </div>

    {/* Grid-based Gallery */}
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
    {[...Array(8)].map((_, i) => (
        <div key={i} className="aspect-square bg-gray-800/70 border border-gray-600 rounded-lg flex flex-col items-center justify-center text-gray-500 hover:border-purple-500 transition-colors cursor-pointer group">
        <ImageIcon className="w-12 h-12 text-gray-600 group-hover:text-purple-400" />
        <span className="text-xs mt-1">Asset {i+1}</span>
        </div>
    ))}
    </div>

    {/* Metadata View (Mock) */}
    <div>
    <h3 className="text-xl font-semibold text-gray-200 mb-3">Metadata</h3>
    <div className="p-4 bg-gray-800/70 border border-gray-600 rounded-lg">
        <p className="text-gray-400">Click an asset to view its prompt, model, and timestamp...</p>
    </div>
    </div>
</div>
);

// --- Pipeline Manager Component ---
const PipelineManager = () => (
<div className="space-y-6">
    <h2 className="text-3xl font-bold text-white text-center">Pipeline Manager</h2>
    <p className="text-gray-300 text-center mb-8">
    Oversee all agents and processes.
    </p>

    {/* Manual Controls */}
    <div className="flex items-center justify-center gap-3">
    <button className="flex items-center gap-2 px-4 py-2 bg-blue-600/80 text-white hover:bg-blue-700 rounded-lg transition-colors text-sm font-medium">
        <PlayIcon className="w-4 h-4" /> Resume
    </button>
    <button className="flex items-center gap-2 px-4 py-2 bg-yellow-600/80 text-white hover:bg-yellow-700 rounded-lg transition-colors text-sm font-medium">
        <PauseIcon className="w-4 h-4" /> Pause
    </button>
    <button className="flex items-center gap-2 px-4 py-2 bg-red-600/80 text-white hover:bg-red-700 rounded-lg transition-colors text-sm font-medium">
        <ResetIcon className="w-4 h-4" /> Reset
    </button>
    </div>

    {/* Visual Pipeline Flow */}
    <div>
    <h3 className="text-xl font-semibold text-gray-200 mb-3">Visual Pipeline (LangGraph)</h3>
    <div className="p-4 bg-gray-800/70 border border-gray-600 rounded-lg min-h-[150px] flex items-center justify-center">
        <p className="text-gray-400">[Visual pipeline flow diagram placeholder]</p>
    </div>
    </div>

    {/* Agent Status */}
    <div>
    <h3 className="text-xl font-semibold text-gray-200 mb-3">Agent Status</h3>
    <div className="space-y-2">
        <div className="p-3 bg-gray-800/70 border border-gray-600 rounded-lg flex justify-between items-center">
        <span className="text-gray-300">Supervisor</span>
        <span className="text-green-400 text-sm font-medium px-2 py-0.5 bg-green-900/50 rounded-full">Active</span>
        </div>
        <div className="p-3 bg-gray-800/70 border border-gray-600 rounded-lg flex justify-between items-center">
        <span className="text-gray-300">SagaAgent</span>
        <span className="text-yellow-400 text-sm font-medium px-2 py-0.5 bg-yellow-900/50 rounded-full">Waiting</span>
        </div>
        <div className="p-3 bg-gray-800/70 border border-gray-600 rounded-lg flex justify-between items-center">
        <span className="text-gray-300">RenderPrepAgent</span>
        <span className="text-gray-400 text-sm font-medium px-2 py-0.5 bg-gray-700/50 rounded-full">Idle</span>
        </div>
    </div>
    </div>

    {/* Logs */}
    <div>
    <h3 className="text-xl font-semibold text-gray-200 mb-3">Logs & Error Tracing</h3>
    <div className="p-3 bg-gray-900/80 border border-gray-600 rounded-lg h-48 overflow-y-auto font-mono text-xs text-gray-400 space-y-1">
        <p><span className="text-cyan-400">[Supervisor]</span> Initializing pipeline...</p>
        <p><span className="text-cyan-400">[Supervisor]</span> Handing off to SagaAgent.</p>
        <p><span className="text-purple-400">[SagaAgent]</span> Generating 'World Lore'...</p>
        <p><span className="text-purple-400">[SagaAgent]</span> Checkpoint reached. Awaiting approval.</p>
    </div>
    </div>

</div>
);

return (
<>
    <Navbar/>
    {/* Main container with Hero styling */}
    <div className="min-h-screen bg-[#050505] text-white relative overflow-hidden">
    {/* Background glow */}
    <div
        className="hero-glow absolute inset-0 z-0 scale-100 opacity-60 transition-all duration-700 
                    bg-[radial-gradient(circle_at_center,rgba(130,75,255,0.4)_0%,rgba(10,10,10,1)_80%)] 
                    blur-[180px]"
    ></div>

    {/* Content Wrapper */}
    <div className="relative z-10 container mx-auto px-4 py-10 sm:py-24">
        
        {/* Header */}
        <div className="pt-16 pb-8 text-center">
        <h1 className="text-5xl font-bold text-white font-Orbitron">UTILITY CONSOLE</h1>
        <p className="text-gray-300 text-sm mt-2">
            Manage Research, Assets, and Agent Pipelines
        </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center justify-center border-b border-purple-500/30 mb-8">
        {Object.values(TABS).map(tabName => {
            const isActive = activeTab === tabName;
            let Icon;
            if (tabName === TABS.RESEARCH) Icon = SearchIcon;
            else if (tabName === TABS.LIBRARY) Icon = LibraryIcon;
            else Icon = PipelineIcon;
            
            return (
            <button
                key={tabName}
                onClick={() => setActiveTab(tabName)}
                className={`flex items-center gap-2 px-4 sm:px-6 py-3 text-sm font-medium transition-colors
                ${isActive
                    ? 'text-purple-300 border-b-2 border-purple-300'
                    : 'text-gray-400 hover:text-white'
                }`}
            >
                <Icon className={`w-4 h-4 ${isActive ? 'text-purple-300' : 'text-gray-500'}`} />
                {tabName}
            </button>
            );
        })}
        </div>

        {/* "Glassmorphism" card for tab content */}
        <div className="max-w-4xl mx-auto bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl shadow-2xl overflow-hidden p-6 sm:p-8">
        {activeTab === TABS.RESEARCH && <ResearchPanel />}
        {activeTab === TABS.LIBRARY && <AssetLibrary />}
        {activeTab === TABS.PIPELINE && <PipelineManager />}
        </div>

    </div>
    </div>
</>
);
};

export default Utility;
