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

  const stepInfo = response
    ? getStepInfo()
    : { current: 0, total: 7, name: "" };

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
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                          fill="none"
                        />
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        />
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
                          width: `${
                            (stepInfo.current / stepInfo.total) * 100
                          }%`,
                        }}
                      ></div>
                    </div>
                  </div>

                  {error && (
                    <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-300">
                      <div className="flex items-center gap-2">
                        <svg
                          className="w-5 h-5"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path
                            fillRule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                            clipRule="evenodd"
                          />
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
                      {response.currentStage === "concept" &&
                        response.concept && (
                          <div className="prose prose-invert max-w-none">
                            <div className="bg-[#0f1629]/60 rounded-lg p-6 border border-slate-700/50">
                              <p className="text-gray-200 text-lg leading-relaxed whitespace-pre-wrap">
                                {typeof response.concept === "string"
                                  ? response.concept
                                  : response.concept?.pitch ||
                                    JSON.stringify(response.concept, null, 2)}
                              </p>
                            </div>
                          </div>
                        )}

                      {/* World Lore Stage */}
                      {response.currentStage === "world_lore" &&
                        response.worldLore && (
                          <div className="space-y-6">
                            {response.worldLore.overview && (
                              <div className="bg-[#0f1629]/60 rounded-lg p-6 border border-slate-700/50">
                                <h3 className="text-xl font-bold text-blue-400 mb-3 flex items-center gap-2">
                                  <span>🌍</span> World Overview
                                </h3>
                                <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">
                                  {response.worldLore.overview}
                                </p>
                              </div>
                            )}

                            {Object.entries(response.worldLore).map(
                              ([key, value]) => {
                                if (key === "overview" || !value) return null;
                                return (
                                  <div
                                    key={key}
                                    className="bg-[#0f1629]/60 rounded-lg p-6 border border-slate-700/50"
                                  >
                                    <h3 className="text-lg font-bold text-blue-300 mb-3 capitalize">
                                      {key.replace(/_/g, " ")}
                                    </h3>
                                    <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">
                                      {typeof value === "string"
                                        ? value
                                        : JSON.stringify(value, null, 2)}
                                    </p>
                                  </div>
                                );
                              }
                            )}
                          </div>
                        )}

                      {/* Factions Stage */}
                      {response.currentStage === "factions" &&
                        response.factions && (
                          <div className="space-y-6">
                            {response.factions.map((faction, idx) => (
                              <div
                                key={idx}
                                className="bg-[#0f1629]/60 rounded-lg p-6 border border-amber-500/30 hover:border-amber-400/50 transition-all"
                              >
                                <div className="flex items-center justify-between mb-4">
                                  <h3 className="text-2xl font-bold text-amber-400">
                                    {faction.faction_name ||
                                      faction.name ||
                                      `Faction ${idx + 1}`}
                                  </h3>
                                  {faction.faction_type && (
                                    <span className="px-3 py-1 bg-amber-600/30 text-amber-300 rounded-full text-sm font-semibold">
                                      {faction.faction_type}
                                    </span>
                                  )}
                                </div>

                                <div className="grid md:grid-cols-2 gap-4">
                                  {faction.core_ideology && (
                                    <div className="col-span-2">
                                      <h4 className="text-sm font-bold text-amber-300 mb-2">
                                        💭 Core Ideology
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {faction.core_ideology}
                                      </p>
                                    </div>
                                  )}

                                  {faction.aesthetic_identity && (
                                    <div>
                                      <h4 className="text-sm font-bold text-purple-300 mb-2">
                                        🎨 Aesthetic
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {faction.aesthetic_identity}
                                      </p>
                                    </div>
                                  )}

                                  {faction.leader_profile && (
                                    <div>
                                      <h4 className="text-sm font-bold text-pink-300 mb-2">
                                        👑 Leadership
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {faction.leader_profile}
                                      </p>
                                    </div>
                                  )}

                                  {faction.headquarters && (
                                    <div>
                                      <h4 className="text-sm font-bold text-cyan-300 mb-2">
                                        🏰 Headquarters
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {faction.headquarters}
                                      </p>
                                    </div>
                                  )}

                                  {faction.hierarchy && (
                                    <div>
                                      <h4 className="text-sm font-bold text-green-300 mb-2">
                                        📊 Hierarchy
                                      </h4>
                                      <p className="text-gray-300 text-sm whitespace-pre-wrap">
                                        {faction.hierarchy}
                                      </p>
                                    </div>
                                  )}
                                </div>
                              </div>
                            ))}
                          </div>
                        )}

                      {/* Characters Stage */}
                      {response.currentStage === "characters" &&
                        response.characters && (
                          <div className="space-y-6">
                            {response.characters.map((char, idx) => (
                              <div
                                key={idx}
                                className="bg-[#0f1629]/60 rounded-lg p-6 border border-green-500/30 hover:border-green-400/50 transition-all"
                              >
                                <div className="flex items-center justify-between mb-4">
                                  <h3 className="text-2xl font-bold text-green-400">
                                    {char.character_name ||
                                      char.name ||
                                      `Character ${idx + 1}`}
                                  </h3>
                                  <span className="px-3 py-1 bg-green-600/20 text-green-300 rounded-full text-xs font-semibold">
                                    #{idx + 1}
                                  </span>
                                </div>

                                <div className="grid md:grid-cols-2 gap-4">
                                  {char.appearance && (
                                    <div className="col-span-2">
                                      <h4 className="text-sm font-bold text-cyan-300 mb-2">
                                        👤 Appearance
                                      </h4>
                                      <p className="text-gray-300 text-sm leading-relaxed">
                                        {char.appearance}
                                      </p>
                                    </div>
                                  )}

                                  {char.motivations && (
                                    <div>
                                      <h4 className="text-sm font-bold text-yellow-300 mb-2">
                                        🎯 Motivations
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {char.motivations}
                                      </p>
                                    </div>
                                  )}

                                  {char.relationships && (
                                    <div>
                                      <h4 className="text-sm font-bold text-pink-300 mb-2">
                                        🤝 Relationships
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {char.relationships}
                                      </p>
                                    </div>
                                  )}

                                  {char.class_abilities && (
                                    <div className="col-span-2">
                                      <h4 className="text-sm font-bold text-purple-300 mb-2">
                                        ⚡ Abilities
                                      </h4>
                                      <p className="text-gray-300 text-sm whitespace-pre-wrap">
                                        {char.class_abilities}
                                      </p>
                                    </div>
                                  )}

                                  {char.personality_traits && (
                                    <div>
                                      <h4 className="text-sm font-bold text-orange-300 mb-2">
                                        ✨ Personality
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {char.personality_traits}
                                      </p>
                                    </div>
                                  )}

                                  {char.backstory && (
                                    <div>
                                      <h4 className="text-sm font-bold text-blue-300 mb-2">
                                        📖 Background
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {char.backstory}
                                      </p>
                                    </div>
                                  )}
                                </div>
                              </div>
                            ))}
                          </div>
                        )}

                      {/* Plot Arcs Stage */}
                      {response.currentStage === "plot_arcs" &&
                        response.plotArcs && (
                          <div className="space-y-6">
                            {response.plotArcs.map((arc, idx) => (
                              <div
                                key={idx}
                                className="bg-[#0f1629]/60 rounded-lg p-6 border border-purple-500/30 hover:border-purple-400/50 transition-all"
                              >
                                <div className="flex items-center justify-between mb-4">
                                  <h3 className="text-2xl font-bold text-purple-400">
                                    {arc.arc_title ||
                                      arc.arc_name ||
                                      `Plot Arc ${idx + 1}`}
                                  </h3>
                                  {arc.arc_type && (
                                    <span className="px-3 py-1 bg-purple-600/30 text-purple-300 rounded-full text-sm font-semibold">
                                      {arc.arc_type}
                                    </span>
                                  )}
                                </div>

                                <div className="space-y-4">
                                  {arc.central_question && (
                                    <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                      <h4 className="text-sm font-bold text-purple-300 mb-2">
                                        ❓ Central Question
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {arc.central_question}
                                      </p>
                                    </div>
                                  )}

                                  {arc.theme && (
                                    <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                      <h4 className="text-sm font-bold text-pink-300 mb-2">
                                        🎭 Theme
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {arc.theme}
                                      </p>
                                    </div>
                                  )}

                                  {arc.estimated_playtime && (
                                    <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                      <h4 className="text-sm font-bold text-cyan-300 mb-2">
                                        ⏱️ Estimated Playtime
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {arc.estimated_playtime}
                                      </p>
                                    </div>
                                  )}

                                  <div className="grid md:grid-cols-2 gap-4">
                                    {arc.act1_hook && (
                                      <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                        <h4 className="text-sm font-bold text-green-300 mb-2">
                                          🎣 Act 1: Hook
                                        </h4>
                                        <p className="text-gray-300 text-sm">
                                          {arc.act1_hook}
                                        </p>
                                      </div>
                                    )}

                                    {arc.act1_worldbuilding && (
                                      <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                        <h4 className="text-sm font-bold text-blue-300 mb-2">
                                          🌍 Act 1: Worldbuilding
                                        </h4>
                                        <p className="text-gray-300 text-sm">
                                          {arc.act1_worldbuilding}
                                        </p>
                                      </div>
                                    )}

                                    {arc.act2_rising_action && (
                                      <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                        <h4 className="text-sm font-bold text-yellow-300 mb-2">
                                          📈 Act 2: Rising Action
                                        </h4>
                                        <p className="text-gray-300 text-sm">
                                          {arc.act2_rising_action}
                                        </p>
                                      </div>
                                    )}

                                    {arc.act3_climax && (
                                      <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                        <h4 className="text-sm font-bold text-red-300 mb-2">
                                          💥 Act 3: Climax
                                        </h4>
                                        <p className="text-gray-300 text-sm">
                                          {arc.act3_climax}
                                        </p>
                                      </div>
                                    )}
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}

                      {/* Questlines Stage */}
                      {response.currentStage === "questlines" &&
                        response.questlines && (
                          <div className="space-y-6">
                            {response.questlines.map((quest, idx) => (
                              <div
                                key={idx}
                                className="bg-[#0f1629]/60 rounded-lg p-6 border border-amber-500/30 hover:border-amber-400/50 transition-all"
                              >
                                <div className="flex items-start justify-between mb-4">
                                  <div className="flex-1">
                                    <h3 className="text-2xl font-bold text-amber-400 mb-2">
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
                                    </div>
                                  </div>
                                </div>

                                <div className="space-y-4">
                                  {quest.discovery_method && (
                                    <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                      <h4 className="text-sm font-bold text-cyan-300 mb-2">
                                        🔍 How to Discover
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {quest.discovery_method}
                                      </p>
                                    </div>
                                  )}

                                  {quest.hook_pitch && (
                                    <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                      <h4 className="text-sm font-bold text-pink-300 mb-2">
                                        🎣 Hook
                                      </h4>
                                      <p className="text-gray-300 text-sm">
                                        {quest.hook_pitch}
                                      </p>
                                    </div>
                                  )}

                                  <div className="grid md:grid-cols-2 gap-4">
                                    {quest.primary_objectives && (
                                      <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                        <h4 className="text-sm font-bold text-green-300 mb-2">
                                          ✓ Primary Objectives
                                        </h4>
                                        <p className="text-gray-300 text-sm whitespace-pre-wrap">
                                          {quest.primary_objectives}
                                        </p>
                                      </div>
                                    )}

                                    {quest.optional_objectives && (
                                      <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                        <h4 className="text-sm font-bold text-blue-300 mb-2">
                                          ⭐ Optional Objectives
                                        </h4>
                                        <p className="text-gray-300 text-sm whitespace-pre-wrap">
                                          {quest.optional_objectives}
                                        </p>
                                      </div>
                                    )}

                                    {quest.reward_structure && (
                                      <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                        <h4 className="text-sm font-bold text-yellow-300 mb-2">
                                          🎁 Rewards
                                        </h4>
                                        <p className="text-gray-300 text-sm whitespace-pre-wrap">
                                          {quest.reward_structure}
                                        </p>
                                      </div>
                                    )}

                                    {quest.skill_checks && (
                                      <div className="bg-black/20 rounded-lg p-4 border border-slate-700/50">
                                        <h4 className="text-sm font-bold text-teal-300 mb-2">
                                          🎲 Skill Checks
                                        </h4>
                                        <p className="text-gray-300 text-sm whitespace-pre-wrap">
                                          {quest.skill_checks}
                                        </p>
                                      </div>
                                    )}
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
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
                            <svg
                              className="w-5 h-5"
                              fill="currentColor"
                              viewBox="0 0 20 20"
                            >
                              <path
                                fillRule="evenodd"
                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                clipRule="evenodd"
                              />
                            </svg>
                            Approve
                          </button>
                          <button
                            onClick={() => setShowFeedbackModal(true)}
                            disabled={loading}
                            className="px-8 py-3 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-orange-500/30 flex items-center gap-2"
                          >
                            <svg
                              className="w-5 h-5"
                              fill="currentColor"
                              viewBox="0 0 20 20"
                            >
                              <path d="M4 3a2 2 0 100 4h12a2 2 0 100-4H4z" />
                              <path
                                fillRule="evenodd"
                                d="M3 8h14v7a2 2 0 01-2 2H5a2 2 0 01-2-2V8zm5 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z"
                                clipRule="evenodd"
                              />
                            </svg>
                            Regenerate
                          </button>
                          <button
                            onClick={() => setShowFeedbackModal(true)}
                            disabled={loading}
                            className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-blue-500/30 flex items-center gap-2"
                          >
                            <svg
                              className="w-5 h-5"
                              fill="currentColor"
                              viewBox="0 0 20 20"
                            >
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
                      <svg
                        className="w-5 h-5"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                          clipRule="evenodd"
                        />
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
                      <svg
                        className="w-5 h-5"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                          clipRule="evenodd"
                        />
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
              <h3 className="text-2xl font-bold mb-6 text-white">
                Provide Feedback
              </h3>
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
