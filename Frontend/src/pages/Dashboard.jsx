import React from 'react';
import { PlusIcon,FolderIcon,ClockIcon   } from 'lucide-react';
import Navbar from '../components/Navbar'

const Dashboard = () => {
  // Mock data for projects and activities
  const projects = [
    { id: 1, name: 'Cyber-Noir Detective', status: 'Narrative in progress' },
    { id: 2, name: 'Project Chimera', status: 'Assets ready' },
    { id: 3, name: 'Voidfarer', status: 'Concept' },
  ];

  const activities = [
    { id: 1, text: 'SagaAgent completed plot arc for "Cyber-Noir".' },
    { id: 2, text: 'RenderPrepAgent generated 5 character portraits.' },
    { id: 3, text: 'New project "Voidfarer" created.' },
  ];

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
          <h1 className="text-4xl font-bold font-Orbitron mb-8">Dashboard</h1>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
            <a href="/agents" className="bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl p-8 shadow-2xl hover:border-purple-400 transition-all group">
              <PlusIcon className="w-10 h-10 text-purple-400 mb-4" />
              <h2 className="text-2xl font-bold mb-2">Create New Project</h2>
              <p className="text-gray-300">Start with a fresh concept and let the agents build your world.</p>
            </a>
            
            <div className="bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl p-8 shadow-2xl">
              <FolderIcon className="w-10 h-10 text-purple-400 mb-4" />
              <h2 className="text-2xl font-bold mb-2">Continue Project</h2>
              <p className="text-gray-300 mb-4">Pick up where you left off.</p>
              <select className="w-full px-4 py-3 bg-gray-800/70 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500">
                {projects.map(p => (
                  <option key={p.id} className="text-black">{p.name}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Project Status & Recent Activity */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Project Status */}
            <div className="bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl shadow-2xl p-8">
              <h2 className="text-2xl font-bold mb-6">Project Status</h2>
              <ul className="space-y-4">
                {projects.map(project => (
                  <li key={project.id} className="flex justify-between items-center bg-gray-800/50 p-4 rounded-lg">
                    <div>
                      <h3 className="font-semibold">{project.name}</h3>
                      <p className="text-sm text-purple-300">{project.status}</p>
                    </div>
                    <a href="#/workspace" className="text-sm text-purple-400 hover:text-purple-300">Open</a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Recent Activity */}
            <div className="bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl shadow-2xl p-8">
              <h2 className="text-2xl font-bold mb-6">Recent Activity</h2>
              <ul className="space-y-4">
                {activities.map(activity => (
                  <li key={activity.id} className="flex items-start gap-3">
                    <ClockIcon className="w-5 h-5 text-gray-400 mt-1 flex-shrink-0" />
                    <p className="text-gray-300">{activity.text}</p>
                  </li>
                ))}
              </ul>
            </div>

          </div>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
