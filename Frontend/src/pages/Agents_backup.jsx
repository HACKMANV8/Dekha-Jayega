import React, { useState } from "react";
import Navbar from "../components/Navbar";
import { FilmIcon } from "lucide-react";

const API_BASE_URL = "http://localhost:4000/api";

const SagaAgent = () => {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [response, setResponse] = useState(null);
  const [showFeedbackModal, setShowFeedbackModal] = useState(false);
  const [feedback, setFeedback] = useState("");

  const handleStartSaga = async () => {
    if (!topic.trim()) {
      setError("Please enter a topic");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const projectRes = await fetch(`${API_BASE_URL}/projects`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: topic,
          description: `Saga: ${topic}`,
          concept: topic,
          genre: "fantasy",
        }),
      });
      if (!projectRes.ok) throw new Error("Failed to create project");
      const projectData = await projectRes.json();
      const sagaRes = await fetch(`${API_BASE_URL}/saga-agent/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          projectId: projectData.data._id,
          topic: topic,
          model: "gemini-2.0-flash",
        }),
      });
      if (!sagaRes.ok) {
        const errData = await sagaRes.json();
        throw new Error(errData.message || "Saga API failed");
      }
      const sagaData = await sagaRes.json();
      setResponse(sagaData.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async () => {
    if (!response?.sessionId) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/saga-agent/continue`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId: response.sessionId }),
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.message || "Failed to continue");
      }
      const data = await res.json();
      setResponse(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitFeedback = async () => {
    if (!response?.sessionId || !feedback.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/saga-agent/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId: response.sessionId,
          feedback: feedback,
          regenerate: true,
        }),
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.message || "Failed to submit feedback");
      }
      const data = await res.json();
      setResponse(data.data);
      setFeedback("");
      setShowFeedbackModal(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Helper to get step info
  const getStepInfo = () => {
    if (!response) return { current: 0, total: 7, name: "" };
    const stages = {
      concept: { step: 1, name: "Concept" },
      world_lore: { step: 2, name: "World Lore" },
      factions: { step: 3, name: "Factions" },
      characters: { step: 4, name: "Characters" },
      plot_arcs: { step: 5, name: "Plot Arcs" },
      questlines: { step: 6, name: "Questlines" },
      complete: { step: 7, name: "Complete" },
    };
    const info = stages[response.currentStage] || { step: 1, name: "Concept" };
    return { current: info.step, total: 7, name: info.name };
  };

  const stepInfo = response ? getStepInfo() : { current: 0, total: 7, name: "" };

  // Get current stage data
  const getCurrentStageData = () => {
    if (!response) return null;
    switch (response.currentStage) {
      case "concept":
        return { title: "Concept", content: response.concept, isText: true };
      case "world_lore":
        return { title: "World Lore", content: response.worldLore, isText: true };
      case "factions":
        return { title: "Factions", content: response.factions, isArray: true };
      case "characters":
        return { title: "Characters", content: response.characters, isArray: true };
      case "plot_arcs":
        return { title: "Plot Arcs", content: response.plotArcs, isArray: true };
      case "questlines":
        return { title: "Questlines", content: response.questlines, isArray: true };
      default:
        return null;
    }
  };

  const stageData = getCurrentStageData();

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-br from-[#0a0e1a] via-[#0f1629] to-[#0a0e1a] text-white">
        {/* Initial Input Screen */}
        {!response && (
          <div className="container mx-auto px-4 py-16">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-12">
                <FilmIcon className="w-16 h-16 text-purple-500 mx-auto mb-6" />
                <h1 className="text-5xl font-bold mb-4 text-white">
                  AI Saga Generator
                </h1>
                <p className="text-gray-400 text-lg">
                  Create an immersive narrative experience powered by AI
                </p>
              </div>

              {error && (
                <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200">
                  {error}
                </div>
              )}

              <div className="bg-[#1a1f35]/60 backdrop-blur-sm rounded-2xl p-8 border border-slate-700/50 shadow-2xl">
                <div className="mb-6">
                  <label className="block text-sm font-semibold mb-3 text-gray-300">
                    Enter Your Saga Concept
                  </label>
                  <textarea
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="e.g., A detective in 1920s Chicago discovers a vast conspiracy..."
                    rows="4"
                    className="w-full px-4 py-3 bg-[#0f1629]/80 border border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-500 resize-none"
                  />
                </div>
                <button
                  onClick={handleStartSaga}
                  disabled={loading || !topic.trim()}
                  className="w-full px-6 py-4 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-purple-500/50"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Generating...
                    </span>
                  ) : (
                    "Start Saga Generation"
                  )}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Workflow View */}
        {response && (
          <div className="min-h-screen flex flex-col">
            {/* Header */}
            <div className="bg-[#0f1629]/80 border-b border-slate-800/50 py-6">
              <div className="container mx-auto px-4">
                <h1 className="text-xl font-medium text-center text-gray-300">
                  Manage and edit the AI-generated narrative
                </h1>
              </div>
            </div>

            {/* Main Content Wrapper */}
            <div className="flex-1 flex flex-col">
              <div className="container mx-auto px-4 py-8 flex-1 flex flex-col">
                <div className="max-w-7xl mx-auto w-full flex-1 flex flex-col">
                  {/* Progress Indicator */}
                  <div className="bg-[#1a1f35]/60 rounded-xl p-6 mb-6 border border-slate-700/50">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm font-semibold text-gray-300">
                        {stepInfo.name}
                      </span>
                      <span className="text-sm font-semibold text-gray-300">
                        Step {stepInfo.current} of {stepInfo.total}
                      </span>
                    </div>
                    <div className="w-full bg-slate-800/80 rounded-full h-1.5 overflow-hidden">
                      <div
                        className="bg-purple-600 h-full transition-all duration-500 ease-out"
                        style={{
                          width: `${(stepInfo.current / stepInfo.total) * 100}%`,
                        }}
                      ></div>
                    </div>
                  </div>

                  {error && (
                    <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-300">
                      <div className="flex items-center gap-2">
                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                        {error}
                      </div>
                    </div>
                  )}

                  {/* Main Content Card */}
                  <div className="bg-[#1a1f35]/60 rounded-xl border border-slate-700/50 flex-1 flex flex-col overflow-hidden">
                    {/* Stage Title */}
                    <div className="p-8 border-b border-slate-700/30">
                      <h2 className="text-4xl font-bold text-center text-white">
                        {stepInfo.name}
                      </h2>
                    </div>

                    {/* Content Area */}
                    <div className="flex-1 p-8 overflow-y-auto">
                      {/* Concept Stage */}
                      {response.currentStage === "concept" && response.concept && (
                        <textarea
                          value={response.concept?.pitch || response.concept || ""}
                          readOnly
                          className="w-full h-full min-h-[300px] px-6 py-4 bg-[#0f1629]/60 border border-slate-700/50 rounded-lg text-gray-200 text-base leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                          placeholder="Your saga concept will appear here..."
                        />
                      )}

                      {/* World Lore Stage */}
                      {response.currentStage === "world_lore" && response.worldLore && (
                        <textarea
                          value={JSON.stringify(response.worldLore, null, 2)}
                          readOnly
                          className="w-full h-full min-h-[300px] px-6 py-4 bg-[#0f1629]/60 border border-slate-700/50 rounded-lg text-gray-200 text-sm leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-purple-500/50 font-mono"
                          placeholder="World lore details will appear here..."
                        />
                      )}

                      {/* Factions Stage */}
                      {response.currentStage === "factions" && response.factions && (
                        <textarea
                          value={JSON.stringify(response.factions, null, 2)}
                          readOnly
                          className="w-full h-full min-h-[300px] px-6 py-4 bg-[#0f1629]/60 border border-slate-700/50 rounded-lg text-gray-200 text-sm leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-purple-500/50 font-mono"
                          placeholder="Faction details will appear here..."
                        />
                      )}

                      {/* Characters Stage */}
                      {response.currentStage === "characters" && response.characters && (
                        <textarea
                          value={JSON.stringify(response.characters, null, 2)}
                          readOnly
                          className="w-full h-full min-h-[300px] px-6 py-4 bg-[#0f1629]/60 border border-slate-700/50 rounded-lg text-gray-200 text-sm leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-purple-500/50 font-mono"
                          placeholder="Character details will appear here..."
                        />
                      )}

                      {/* Plot Arcs Stage */}
                      {response.currentStage === "plot_arcs" && response.plotArcs && (
                        <textarea
                          value={JSON.stringify(response.plotArcs, null, 2)}
                          readOnly
                          className="w-full h-full min-h-[300px] px-6 py-4 bg-[#0f1629]/60 border border-slate-700/50 rounded-lg text-gray-200 text-sm leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-purple-500/50 font-mono"
                          placeholder="Plot arc details will appear here..."
                        />
                      )}

                      {/* Questlines Stage */}
                      {response.currentStage === "questlines" && response.questlines && (
                        <textarea
                          value={JSON.stringify(response.questlines, null, 2)}
                          readOnly
                          className="w-full h-full min-h-[300px] px-6 py-4 bg-[#0f1629]/60 border border-slate-700/50 rounded-lg text-gray-200 text-sm leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-purple-500/50 font-mono"
                          placeholder="Questline details will appear here..."
                        />
                      )}
                    </div>

                    {/* Action Buttons */}
                    <div className="p-8 border-t border-slate-700/30">
                      {response.awaitingFeedback && (
                        <div className="flex gap-4 justify-center mb-6">
                          <button
                            onClick={handleApprove}
                            disabled={loading}
                            className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-green-500/30 flex items-center gap-2"
                          >
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                            Approve
                          </button>
                          <button
                            onClick={() => setShowFeedbackModal(true)}
                            disabled={loading}
                            className="px-8 py-3 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-orange-500/30 flex items-center gap-2"
                          >
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M4 3a2 2 0 100 4h12a2 2 0 100-4H4z" />
                              <path fillRule="evenodd" d="M3 8h14v7a2 2 0 01-2 2H5a2 2 0 01-2-2V8zm5 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" clipRule="evenodd" />
                            </svg>
                            Regenerate
                          </button>
                          <button
                            onClick={() => setShowFeedbackModal(true)}
                            disabled={loading}
                            className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-blue-500/30 flex items-center gap-2"
                          >
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                            </svg>
                            Save Edit
                          </button>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Navigation Buttons */}
                  <div className="flex items-center justify-between mt-6">
                    <button
                      disabled
                      className="px-6 py-3 bg-slate-800/50 text-gray-500 rounded-lg font-semibold cursor-not-allowed flex items-center gap-2"
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      Previous
                    </button>

                    <div className="text-gray-400 text-sm">
                      Step {stepInfo.current} of {stepInfo.total}
                    </div>

                    <button
                      onClick={handleApprove}
                      disabled={loading || !response.awaitingFeedback}
                      className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                    >
                      Next
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Feedback Modal */}
        {showFeedbackModal && (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-[#1a1f35] border border-slate-700/50 rounded-2xl p-8 max-w-2xl w-full shadow-2xl">
              <h3 className="text-2xl font-bold mb-6 text-white">Provide Feedback</h3>
              <textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                placeholder="Enter your feedback or regeneration instructions..."
                rows="6"
                className="w-full px-4 py-3 bg-[#0f1629]/80 border border-slate-700 rounded-lg text-white placeholder-gray-500 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 mb-6"
              />
              <div className="flex gap-3 justify-end">
                <button
                  onClick={() => {
                    setShowFeedbackModal(false);
                    setFeedback("");
                  }}
                  disabled={loading}
                  className="px-6 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold disabled:opacity-50 transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSubmitFeedback}
                  disabled={loading || !feedback.trim()}
                  className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-semibold disabled:opacity-50 transition-all"
                >
                  {loading ? "Submitting..." : "Submit Feedback"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default SagaAgent;
                  <div className="p-6 bg-gray-800/60 border border-blue-500/40 rounded-xl">
                    <h2 className="text-2xl font-bold text-blue-400 mb-4">
                      🌍 World Lore
                    </h2>
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-sm font-semibold text-gray-400 uppercase mb-2">
                          Overview
                        </h4>
                        <p className="text-gray-300 leading-relaxed">
                          {response.worldLore.overview}
                        </p>
                      </div>
                      {response.worldLore.geography && (
                        <div>
                          <h4 className="text-sm font-semibold text-gray-400 uppercase mb-2">
                            Geography
                          </h4>
                          <p className="text-gray-300 whitespace-pre-line leading-relaxed">
                            {response.worldLore.geography}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Factions Stage */}
                {response.factions && response.factions.length > 0 && (
                  <div className="p-6 bg-gray-800/60 border border-red-500/40 rounded-xl">
                    <h2 className="text-2xl font-bold text-red-400 mb-4">
                      ⚔️ Factions ({response.factions.length})
                    </h2>
                    <div className="grid gap-6">
                      {response.factions.map((faction, idx) => {
                        console.log(`Faction ${idx}:`, faction);

                        return (
                          <div
                            key={idx}
                            className="p-6 bg-gradient-to-br from-gray-900/80 to-gray-900/50 border border-red-500/30 rounded-xl hover:border-red-400/50 transition-all"
                          >
                            {/* Header */}
                            <div className="flex items-start justify-between mb-4">
                              <div>
                                <h3 className="text-xl font-bold text-white mb-1">
                                  {faction.faction_name ||
                                    faction.name ||
                                    `${
                                      faction.faction_type || "Unknown Faction"
                                    }`}
                                </h3>
                                {faction.motto_tagline && (
                                  <p className="text-red-400 text-sm italic">
                                    "{faction.motto_tagline}"
                                  </p>
                                )}
                              </div>
                              <span className="px-3 py-1 bg-red-600/20 text-red-300 rounded-full text-xs font-semibold">
                                #{idx + 1}
                              </span>
                            </div>

                            {/* Content Grid */}
                            <div className="grid md:grid-cols-2 gap-4">
                              {/* Type */}
                              {faction.faction_type && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-red-300 mb-2 flex items-center gap-2">
                                    <span>🏛️</span> Type
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {faction.faction_type}
                                  </p>
                                </div>
                              )}

                              {/* Ideology */}
                              {faction.core_ideology && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-purple-300 mb-2 flex items-center gap-2">
                                    <span>💭</span> Core Ideology
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {faction.core_ideology}
                                  </p>
                                </div>
                              )}

                              {/* Aesthetic */}
                              {faction.aesthetic_identity && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-pink-300 mb-2 flex items-center gap-2">
                                    <span>🎨</span> Aesthetic Identity
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {faction.aesthetic_identity}
                                  </p>
                                </div>
                              )}

                              {/* Leader */}
                              {faction.leader_profile && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-yellow-300 mb-2 flex items-center gap-2">
                                    <span>👑</span> Leadership
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {faction.leader_profile}
                                  </p>
                                </div>
                              )}

                              {/* Headquarters */}
                              {faction.headquarters && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-blue-300 mb-2 flex items-center gap-2">
                                    <span>🏰</span> Headquarters
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {faction.headquarters}
                                  </p>
                                </div>
                              )}

                              {/* Controlled Regions */}
                              {faction.controlled_regions && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-green-300 mb-2 flex items-center gap-2">
                                    <span>🗺️</span> Territory
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {faction.controlled_regions}
                                  </p>
                                </div>
                              )}

                              {/* Hierarchy */}
                              {faction.hierarchy && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-cyan-300 mb-2 flex items-center gap-2">
                                    <span>📊</span> Hierarchy
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {faction.hierarchy}
                                  </p>
                                </div>
                              )}

                              {/* Questline */}
                              {faction.faction_questline && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-orange-300 mb-2 flex items-center gap-2">
                                    <span>📜</span> Faction Questline
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {faction.faction_questline}
                                  </p>
                                </div>
                              )}
                            </div>

                            {/* Debug */}
                            <details className="mt-4">
                              <summary className="text-xs text-gray-500 cursor-pointer hover:text-gray-400">
                                🔍 Debug Data
                              </summary>
                              <pre className="text-xs text-gray-400 mt-2 p-3 bg-black/30 rounded overflow-auto max-h-40">
                                {JSON.stringify(faction, null, 2)}
                              </pre>
                            </details>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Characters Stage */}
                {response.characters && response.characters.length > 0 && (
                  <div className="p-6 bg-gray-800/60 border border-green-500/40 rounded-xl">
                    <h2 className="text-2xl font-bold text-green-400 mb-4">
                      👥 Characters ({response.characters.length})
                    </h2>
                    <div className="grid gap-6">
                      {response.characters.map((char, idx) => {
                        console.log(`Character ${idx}:`, char);

                        return (
                          <div
                            key={idx}
                            className="p-6 bg-gradient-to-br from-gray-900/80 to-gray-900/50 border border-green-500/30 rounded-xl hover:border-green-400/50 transition-all"
                          >
                            {/* Header */}
                            <div className="flex items-start justify-between mb-4">
                              <div>
                                <h3 className="text-xl font-bold text-white mb-1">
                                  {char.character_name ||
                                    char.name ||
                                    `Character ${idx + 1}`}
                                </h3>
                                {char.tagline_quote && (
                                  <p className="text-green-400 text-sm italic">
                                    "{char.tagline_quote}"
                                  </p>
                                )}
                              </div>
                              <span className="px-3 py-1 bg-green-600/20 text-green-300 rounded-full text-xs font-semibold">
                                #{idx + 1}
                              </span>
                            </div>

                            {/* Content Grid */}
                            <div className="grid md:grid-cols-2 gap-4">
                              {/* Appearance */}
                              {char.appearance && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-green-300 mb-2 flex items-center gap-2">
                                    <span>👤</span> Appearance
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {char.appearance}
                                  </p>
                                </div>
                              )}

                              {/* Motivations */}
                              {char.motivations && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-blue-300 mb-2 flex items-center gap-2">
                                    <span>🎯</span> Motivations
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {char.motivations}
                                  </p>
                                </div>
                              )}

                              {/* Relationships */}
                              {char.relationships && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-purple-300 mb-2 flex items-center gap-2">
                                    <span>🤝</span> Relationships
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {char.relationships}
                                  </p>
                                </div>
                              )}

                              {/* Abilities */}
                              {char.class_abilities && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-orange-300 mb-2 flex items-center gap-2">
                                    <span>⚡</span> Abilities
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {char.class_abilities}
                                  </p>
                                </div>
                              )}

                              {/* Additional fields */}
                              {char.personality_traits && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-pink-300 mb-2">
                                    Personality
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {char.personality_traits}
                                  </p>
                                </div>
                              )}

                              {char.backstory && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-yellow-300 mb-2">
                                    Background
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {char.backstory}
                                  </p>
                                </div>
                              )}

                              {char.combat_style && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-red-300 mb-2">
                                    Combat Style
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {char.combat_style}
                                  </p>
                                </div>
                              )}

                              {char.character_type && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-cyan-300 mb-2">
                                    Type
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {char.character_type}
                                  </p>
                                </div>
                              )}

                              {char.role_purpose && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-teal-300 mb-2">
                                    Role
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {char.role_purpose}
                                  </p>
                                </div>
                              )}
                            </div>

                            {/* Debug */}
                            <details className="mt-4">
                              <summary className="text-xs text-gray-500 cursor-pointer hover:text-gray-400">
                                🔍 Debug Data
                              </summary>
                              <pre className="text-xs text-gray-400 mt-2 p-3 bg-black/30 rounded overflow-auto max-h-40">
                                {JSON.stringify(char, null, 2)}
                              </pre>
                            </details>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Plot Arcs Stage */}
                {response.plotArcs && response.plotArcs.length > 0 && (
                  <div className="p-6 bg-gray-800/60 border border-purple-500/40 rounded-xl">
                    <h2 className="text-2xl font-bold text-purple-400 mb-4">
                      📖 Plot Arcs ({response.plotArcs.length})
                    </h2>
                    <div className="grid gap-6">
                      {response.plotArcs.map((arc, idx) => {
                        console.log(`Plot Arc ${idx}:`, arc);

                        return (
                          <div
                            key={idx}
                            className="p-6 bg-gradient-to-br from-gray-900/80 to-gray-900/50 border border-purple-500/30 rounded-xl hover:border-purple-400/50 transition-all"
                          >
                            {/* Header */}
                            <div className="flex items-start justify-between mb-4">
                              <div>
                                <h3 className="text-xl font-bold text-white mb-1">
                                  {arc.arc_title ||
                                    arc.arc_name ||
                                    arc.name ||
                                    `Plot Arc ${idx + 1}`}
                                </h3>
                                {arc.arc_type && (
                                  <span className="inline-block px-3 py-1 bg-purple-600/30 text-purple-300 rounded-full text-xs font-semibold">
                                    {arc.arc_type}
                                  </span>
                                )}
                              </div>
                              <span className="px-3 py-1 bg-purple-600/20 text-purple-300 rounded-full text-xs font-semibold">
                                Arc #{idx + 1}
                              </span>
                            </div>

                            {/* Content Grid */}
                            <div className="grid md:grid-cols-2 gap-4">
                              {/* Central Question */}
                              {arc.central_question && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-purple-300 mb-2 flex items-center gap-2">
                                    <span>❓</span> Central Question
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {arc.central_question}
                                  </p>
                                </div>
                              )}

                              {/* Theme */}
                              {arc.theme && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-pink-300 mb-2 flex items-center gap-2">
                                    <span>🎭</span> Theme
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {arc.theme}
                                  </p>
                                </div>
                              )}

                              {/* Estimated Playtime */}
                              {arc.estimated_playtime && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-blue-300 mb-2 flex items-center gap-2">
                                    <span>⏱️</span> Playtime
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {arc.estimated_playtime}
                                  </p>
                                </div>
                              )}

                              {/* Act 1 Hook */}
                              {arc.act1_hook && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-green-300 mb-2 flex items-center gap-2">
                                    <span>🎣</span> Act 1: Hook
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {arc.act1_hook}
                                  </p>
                                </div>
                              )}

                              {/* World Building */}
                              {arc.act1_worldbuilding && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-cyan-300 mb-2 flex items-center gap-2">
                                    <span>🌍</span> World Building
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {arc.act1_worldbuilding}
                                  </p>
                                </div>
                              )}

                              {/* Tutorial */}
                              {arc.act1_tutorial && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-orange-300 mb-2 flex items-center gap-2">
                                    <span>📚</span> Tutorial Mechanics
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {arc.act1_tutorial}
                                  </p>
                                </div>
                              )}

                              {/* Other acts */}
                              {arc.act2_rising_action && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-yellow-300 mb-2 flex items-center gap-2">
                                    <span>📈</span> Act 2: Rising Action
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-line">
                                    {arc.act2_rising_action}
                                  </p>
                                </div>
                              )}

                              {arc.act3_climax && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-red-300 mb-2 flex items-center gap-2">
                                    <span>💥</span> Act 3: Climax & Resolution
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-line">
                                    {arc.act3_climax}
                                  </p>
                                </div>
                              )}

                              {/* Summary fallback */}
                              {arc.summary && !arc.central_question && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-purple-300 mb-2">
                                    📝 Summary
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {arc.summary}
                                  </p>
                                </div>
                              )}

                              {arc.key_events && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-yellow-300 mb-2">
                                    ⭐ Key Events
                                  </h4>
                                  <p className="text-gray-300 text-sm whitespace-pre-line leading-relaxed">
                                    {arc.key_events}
                                  </p>
                                </div>
                              )}

                              {arc.narrative_themes && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-pink-300 mb-2">
                                    🎭 Themes
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {arc.narrative_themes}
                                  </p>
                                </div>
                              )}

                              {arc.character_development && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-green-300 mb-2">
                                    👥 Character Development
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {arc.character_development}
                                  </p>
                                </div>
                              )}
                            </div>

                            <details className="mt-4">
                              <summary className="text-xs text-gray-500 cursor-pointer hover:text-gray-400">
                                🔍 Debug Data
                              </summary>
                              <pre className="text-xs text-gray-400 mt-2 p-3 bg-black/30 rounded overflow-auto max-h-40">
                                {JSON.stringify(arc, null, 2)}
                              </pre>
                            </details>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Questlines Stage */}
                {response.questlines && response.questlines.length > 0 && (
                  <div className="p-6 bg-gray-800/60 border border-amber-500/40 rounded-xl">
                    <h2 className="text-2xl font-bold text-amber-400 mb-4">
                      🗺️ Questlines ({response.questlines.length})
                    </h2>
                    <div className="grid gap-6">
                      {response.questlines.map((quest, idx) => {
                        console.log(`Quest ${idx}:`, quest);

                        return (
                          <div
                            key={idx}
                            className="p-6 bg-gradient-to-br from-gray-900/80 to-gray-900/50 border border-amber-500/30 rounded-xl hover:border-amber-400/50 transition-all"
                          >
                            {/* Header */}
                            <div className="flex items-start justify-between mb-4">
                              <div className="flex-1">
                                <h3 className="text-xl font-bold text-white mb-2">
                                  {quest.quest_name ||
                                    quest.name ||
                                    `Quest ${idx + 1}`}
                                </h3>
                                <div className="flex flex-wrap gap-2">
                                  {quest.quest_type && (
                                    <span className="px-3 py-1 bg-amber-600/30 text-amber-300 rounded-full text-xs font-semibold">
                                      {quest.quest_type}
                                    </span>
                                  )}
                                  {quest.difficulty && (
                                    <span className="px-3 py-1 bg-red-600/30 text-red-300 rounded-full text-xs font-semibold">
                                      💪 {quest.difficulty}
                                    </span>
                                  )}
                                  {quest.estimated_time && (
                                    <span className="px-3 py-1 bg-blue-600/30 text-blue-300 rounded-full text-xs font-semibold">
                                      ⏱️ {quest.estimated_time}
                                    </span>
                                  )}
                                </div>
                              </div>
                              <span className="px-3 py-1 bg-amber-600/20 text-amber-300 rounded-full text-xs font-semibold shrink-0">
                                #{idx + 1}
                              </span>
                            </div>

                            {/* Content Grid */}
                            <div className="grid md:grid-cols-2 gap-4">
                              {/* Discovery Method */}
                              {quest.discovery_method && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-cyan-300 mb-2 flex items-center gap-2">
                                    <span>🔍</span> How to Discover
                                  </h4>
                                  <p className="text-gray-300 text-sm leading-relaxed">
                                    {quest.discovery_method}
                                  </p>
                                </div>
                              )}

                              {/* Quest Giver */}
                              {quest.quest_giver && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-purple-300 mb-2 flex items-center gap-2">
                                    <span>👤</span> Quest Giver
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {quest.quest_giver}
                                  </p>
                                </div>
                              )}

                              {/* Hook/Pitch */}
                              {quest.hook_pitch && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-pink-300 mb-2 flex items-center gap-2">
                                    <span>🎣</span> Hook
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {quest.hook_pitch}
                                  </p>
                                </div>
                              )}

                              {/* Urgency Factor */}
                              {quest.urgency_factor && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-orange-300 mb-2 flex items-center gap-2">
                                    <span>⚡</span> Urgency
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {quest.urgency_factor}
                                  </p>
                                </div>
                              )}

                              {/* Primary Objectives */}
                              {quest.primary_objectives && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-green-300 mb-2 flex items-center gap-2">
                                    <span>✓</span> Primary Objectives
                                  </h4>
                                  <p className="text-gray-300 text-sm whitespace-pre-line leading-relaxed">
                                    {quest.primary_objectives}
                                  </p>
                                </div>
                              )}

                              {/* Optional Objectives */}
                              {quest.optional_objectives && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-blue-300 mb-2 flex items-center gap-2">
                                    <span>⭐</span> Optional Objectives
                                  </h4>
                                  <p className="text-gray-300 text-sm whitespace-pre-line leading-relaxed">
                                    {quest.optional_objectives}
                                  </p>
                                </div>
                              )}

                              {/* Nested Objectives */}
                              {quest.nested_objectives && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-indigo-300 mb-2 flex items-center gap-2">
                                    <span>📋</span> Detailed Steps
                                  </h4>
                                  <p className="text-gray-300 text-sm whitespace-pre-line leading-relaxed">
                                    {quest.nested_objectives}
                                  </p>
                                </div>
                              )}

                              {/* Choice Points */}
                              {quest.choice_points && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-yellow-300 mb-2 flex items-center gap-2">
                                    <span>🔀</span> Key Choices
                                  </h4>
                                  <p className="text-gray-300 text-sm whitespace-pre-line leading-relaxed">
                                    {quest.choice_points}
                                  </p>
                                </div>
                              )}

                              {/* Path Outcomes */}
                              {quest.path_outcomes && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-purple-300 mb-2 flex items-center gap-2">
                                    <span>🎯</span> Branching Outcomes
                                  </h4>
                                  <p className="text-gray-300 text-sm whitespace-pre-line leading-relaxed">
                                    {quest.path_outcomes}
                                  </p>
                                </div>
                              )}

                              {/* Skill Checks */}
                              {quest.skill_checks && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-teal-300 mb-2 flex items-center gap-2">
                                    <span>🎲</span> Skill Checks
                                  </h4>
                                  <p className="text-gray-300 text-sm whitespace-pre-line">
                                    {quest.skill_checks}
                                  </p>
                                </div>
                              )}

                              {/* Rewards */}
                              {quest.reward_structure && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-yellow-300 mb-2 flex items-center gap-2">
                                    <span>🎁</span> Rewards
                                  </h4>
                                  <p className="text-gray-300 text-sm whitespace-pre-line">
                                    {quest.reward_structure}
                                  </p>
                                </div>
                              )}

                              {/* Failure Conditions */}
                              {quest.failure_conditions && (
                                <div className="p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-red-300 mb-2 flex items-center gap-2">
                                    <span>❌</span> Failure
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {quest.failure_conditions}
                                  </p>
                                </div>
                              )}

                              {/* Story Beats */}
                              {quest.story_beats && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-pink-300 mb-2 flex items-center gap-2">
                                    <span>🎬</span> Story Moments
                                  </h4>
                                  <p className="text-gray-300 text-sm whitespace-pre-line">
                                    {quest.story_beats}
                                  </p>
                                </div>
                              )}

                              {/* Exploration */}
                              {quest.exploration_required && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-cyan-300 mb-2 flex items-center gap-2">
                                    <span>🗺️</span> Exploration
                                  </h4>
                                  <p className="text-gray-300 text-sm">
                                    {quest.exploration_required}
                                  </p>
                                </div>
                              )}

                              {/* Unlocks */}
                              {quest.unlocks_consequences && (
                                <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                  <h4 className="text-sm font-bold text-green-300 mb-2 flex items-center gap-2">
                                    <span>🔓</span> Unlocks & Consequences
                                  </h4>
                                  <p className="text-gray-300 text-sm whitespace-pre-line">
                                    {quest.unlocks_consequences}
                                  </p>
                                </div>
                              )}

                              {/* Fallback fields */}
                              {quest.description &&
                                !quest.primary_objectives && (
                                  <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                    <h4 className="text-sm font-bold text-amber-300 mb-2">
                                      📜 Description
                                    </h4>
                                    <p className="text-gray-300 text-sm leading-relaxed">
                                      {quest.description}
                                    </p>
                                  </div>
                                )}

                              {quest.objectives &&
                                !quest.primary_objectives && (
                                  <div className="col-span-2 p-4 bg-black/20 rounded-lg border border-gray-700/50">
                                    <h4 className="text-sm font-bold text-blue-300 mb-2">
                                      ✓ Objectives
                                    </h4>
                                    <p className="text-gray-300 text-sm whitespace-pre-line leading-relaxed">
                                      {quest.objectives}
                                    </p>
                                  </div>
                                )}
                            </div>

                            {/* Debug */}
                            <details className="mt-4">
                              <summary className="text-xs text-gray-500 cursor-pointer hover:text-gray-400">
                                🔍 Debug Data
                              </summary>
                              <pre className="text-xs text-gray-400 mt-2 p-3 bg-black/30 rounded overflow-auto max-h-60">
                                {JSON.stringify(quest, null, 2)}
                              </pre>
                            </details>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Feedback Modal */}
          {showFeedbackModal && (
            <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
              <div className="bg-gray-900 border border-purple-500/50 rounded-2xl p-6 max-w-lg w-full">
                <h3 className="text-xl font-bold mb-4">Provide Feedback</h3>
                <textarea
                  className="w-full px-4 py-3 bg-gray-800/70 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-purple-500 resize-none mb-4"
                  rows="6"
                  placeholder="What would you like to change about this concept?"
                  value={feedback}
                  onChange={(e) => setFeedback(e.target.value)}
                  disabled={loading}
                />
                <div className="flex gap-3">
                  <button
                    onClick={handleSubmitFeedback}
                    disabled={loading || !feedback.trim()}
                    className="flex-1 px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold disabled:opacity-50"
                  >
                    {loading ? "Submitting..." : "Submit Feedback"}
                  </button>
                  <button
                    onClick={() => {
                      setShowFeedbackModal(false);
                      setFeedback("");
                    }}
                    disabled={loading}
                    className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg font-semibold disabled:opacity-50"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default SagaAgent;
