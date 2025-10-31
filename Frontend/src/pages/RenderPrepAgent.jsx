import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import {
  TextIcon,
  ImageIcon,
  VideoIcon,
  MapIcon,
  Loader2,
  AlertCircle,
  Download,
  Eye,
  Sparkles,
  CheckCircle,
} from "lucide-react";

const API_BASE_URL = "http://localhost:4000/api";

const RenderPrepAgent = () => {
  const [activeTab, setActiveTab] = useState("Prompt Preview");
  const [sagaSessions, setSagaSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [assets, setAssets] = useState([]);
  const [generatingImages, setGeneratingImages] = useState(false);
  const [qualityPreset, setQualityPreset] = useState("standard");

  const tabs = [
    { name: "Prompt Preview", icon: TextIcon },
    { name: "Image Generation", icon: ImageIcon },
    { name: "Video Storyboarding", icon: VideoIcon },
    { name: "World Layout", icon: MapIcon },
  ];

  // Fetch saga sessions on component mount and restore previous session
  useEffect(() => {
    fetchSagaSessions();

    // Restore previously selected session from localStorage
    const savedSessionId = localStorage.getItem("renderPrepSelectedSession");
    console.log("[RenderPrep] Checking for saved session ID:", savedSessionId);
    if (savedSessionId) {
      console.log(
        "[RenderPrep] Found saved session, will restore after sessions load"
      );
      // Fetch assets for the saved session
      fetchAssetsForSession(savedSessionId);
    } else {
      console.log("[RenderPrep] No saved session found in localStorage");
    }
  }, []);

  // Fetch assets when session changes
  useEffect(() => {
    if (selectedSession) {
      // Save selected session to localStorage
      localStorage.setItem("renderPrepSelectedSession", selectedSession._id);
      // Fetch existing assets for this session
      fetchAssetsForSession(selectedSession._id);
    }
  }, [selectedSession]);

  const fetchSagaSessions = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${API_BASE_URL}/saga-agent/sessions`);
      const data = await response.json();

      if (data.success) {
        console.log("Fetched sessions:", data.data);
        // Show all sessions (not just completed ones)
        // Filter for sessions that have reached at least the concept stage
        const validSessions = data.data.filter(
          (session) =>
            session.concept && Object.keys(session.concept).length > 0
        );
        setSagaSessions(validSessions);

        // Restore selected session if it exists
        const savedSessionId = localStorage.getItem(
          "renderPrepSelectedSession"
        );
        if (savedSessionId) {
          const savedSession = validSessions.find(
            (s) => s._id === savedSessionId
          );
          if (savedSession) {
            setSelectedSession(savedSession);
          }
        }

        if (validSessions.length === 0) {
          setError(
            "No saga sessions found. Please create a saga workflow first in the Agents page."
          );
        }
      } else {
        setError(data.message || "Failed to fetch saga sessions");
      }
    } catch (err) {
      setError("Failed to fetch saga sessions: " + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAssetsForSession = async (sessionId) => {
    try {
      console.log(
        "[fetchAssetsForSession] Fetching assets for session:",
        sessionId
      );
      const response = await fetch(
        `${API_BASE_URL}/render-prep/assets/${sessionId}`
      );
      const data = await response.json();

      if (data.success && data.data.length > 0) {
        console.log("[fetchAssetsForSession] Loaded assets:", data.data);
        // Transform assets to match frontend format
        const transformedAssets = data.data.map((asset) => ({
          id: asset._id,
          name: asset.name,
          type: asset.type,
          prompt: asset.prompts?.detailed || asset.prompt || "",
          imageUrl: asset.url,
          status: asset.status,
          metadata: asset.metadata,
        }));
        setAssets(transformedAssets);
        console.log(
          "[fetchAssetsForSession] Transformed assets:",
          transformedAssets
        );
      } else {
        console.log("[fetchAssetsForSession] No assets found for session");
        setAssets([]);
      }
    } catch (err) {
      console.error("[fetchAssetsForSession] Failed to fetch assets:", err);
      // Don't show error to user, just log it
      setAssets([]);
    }
  };

  const generatePrompts = async () => {
    if (!selectedSession) {
      setError("Please select a saga session first");
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await fetch(
        `${API_BASE_URL}/render-prep/generate-prompts`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            sessionId: selectedSession._id,
            qualityPreset,
            generateImages: false,
          }),
        }
      );

      const data = await response.json();

      if (data.success) {
        // Backend now returns assets with all fields including _id/id
        const transformedAssets = data.data.assets.map((asset) => ({
          id: asset._id || asset.id,
          name: asset.name,
          type: asset.type,
          prompt: asset.prompt,
          imageUrl: asset.url,
          status: asset.status,
          metadata: asset.metadata,
        }));
        setAssets(transformedAssets);
        // Switch to Image Generation tab
        setActiveTab("Image Generation");
        setActiveTab("Image Generation");
      } else {
        setError(data.message || "Failed to generate prompts");
      }
    } catch (err) {
      setError("Failed to generate prompts: " + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const generateSingleImage = async (assetId) => {
    try {
      console.log("[generateSingleImage] Starting for assetId:", assetId);
      console.log(
        "[generateSingleImage] URL:",
        `${API_BASE_URL}/render-prep/generate-image/${assetId}`
      );

      const response = await fetch(
        `${API_BASE_URL}/render-prep/generate-image/${assetId}`,
        {
          method: "POST",
        }
      );

      console.log("[generateSingleImage] Response status:", response.status);
      const data = await response.json();
      console.log("[generateSingleImage] Response data:", data);
      console.log("[generateSingleImage] data.data:", data.data);

      if (data.success) {
        const imageUrl = data.data.imageUrl || data.data.url;
        console.log("[generateSingleImage] Success! Image URL:", imageUrl);

        if (!imageUrl) {
          console.error("[generateSingleImage] No imageUrl found in response!");
          throw new Error("No image URL returned from server");
        }

        // Update the asset in the list
        setAssets((prev) => {
          const updated = prev.map((asset) =>
            asset.id === assetId
              ? { ...asset, imageUrl: imageUrl, status: "completed" }
              : asset
          );
          console.log("[generateSingleImage] Updated assets:", updated);
          return updated;
        });
      } else {
        console.error(
          "[generateSingleImage] API returned success=false:",
          data.message
        );
        throw new Error(data.message);
      }
    } catch (err) {
      console.error("[generateSingleImage] Failed to generate image:", err);
      throw err;
    }
  };

  const generateAllImages = async () => {
    try {
      setGeneratingImages(true);
      setError(null);

      const assetIds = assets.map((asset) => asset.id);

      const response = await fetch(
        `${API_BASE_URL}/render-prep/batch-generate-images`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ assetIds }),
        }
      );

      const data = await response.json();

      if (data.success) {
        // Refresh assets to show generated images
        if (selectedSession) {
          const assetsResponse = await fetch(
            `${API_BASE_URL}/render-prep/assets/${selectedSession.projectId}`
          );
          const assetsData = await assetsResponse.json();
          if (assetsData.success) {
            const sessionAssets = assetsData.data.filter(
              (asset) => asset.projectId === selectedSession.projectId
            );
            setAssets(
              sessionAssets.map((a) => ({
                id: a._id,
                name: a.name,
                type: a.type,
                prompt: a.prompts.detailed,
                imageUrl: a.url,
                status: a.status,
              }))
            );
          }
        }
      } else {
        setError(data.message || "Failed to generate images");
      }
    } catch (err) {
      setError("Failed to generate images: " + err.message);
      console.error(err);
    } finally {
      setGeneratingImages(false);
    }
  };

  const PromptPreviewTab = () => (
    <div className="space-y-6">
      {/* Saga Selection */}
      <div className="bg-gray-900/50 border border-purple-500/30 rounded-lg p-6">
        <h3 className="text-xl font-semibold mb-4 text-purple-400">
          Select Saga Session
        </h3>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Available Saga Sessions ({sagaSessions.length})
            </label>
            <select
              value={selectedSession?._id || ""}
              onChange={(e) => {
                const session = sagaSessions.find(
                  (s) => s._id === e.target.value
                );
                setSelectedSession(session);
              }}
              className="w-full px-4 py-2 bg-gray-800 border border-purple-500/30 rounded-lg text-white focus:outline-none focus:border-purple-400"
            >
              <option value="">Choose a saga session...</option>
              {sagaSessions.map((session) => (
                <option key={session._id} value={session._id}>
                  {session.topic} ({session.currentStage} - {session.status}) -{" "}
                  {new Date(session.createdAt).toLocaleDateString()}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Quality Preset
            </label>
            <select
              value={qualityPreset}
              onChange={(e) => setQualityPreset(e.target.value)}
              className="w-full px-4 py-2 bg-gray-800 border border-purple-500/30 rounded-lg text-white focus:outline-none focus:border-purple-400"
            >
              <option value="draft">Draft</option>
              <option value="standard">Standard</option>
              <option value="high">High Quality</option>
              <option value="cinematic">Cinematic</option>
            </select>
          </div>

          <button
            onClick={generatePrompts}
            disabled={loading || !selectedSession}
            className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-medium py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Generating Prompts...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                Generate Prompts
              </>
            )}
          </button>
        </div>
      </div>

      {/* Session Preview */}
      {selectedSession && (
        <div className="bg-gray-900/50 border border-purple-500/30 rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4 text-purple-400">
            Session Details
          </h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-400">Topic:</span>
              <p className="text-white font-medium">{selectedSession.topic}</p>
            </div>
            <div>
              <span className="text-gray-400">Stage:</span>
              <p className="text-white font-medium">
                {selectedSession.currentStage}
              </p>
            </div>
            <div>
              <span className="text-gray-400">Characters:</span>
              <p className="text-white font-medium">
                {selectedSession.characters?.length || 0}
              </p>
            </div>
            <div>
              <span className="text-gray-400">Factions:</span>
              <p className="text-white font-medium">
                {selectedSession.factions?.length || 0}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-red-300">{error}</p>
        </div>
      )}
    </div>
  );

  const ImageGenerationTab = () => (
    <div className="space-y-6">
      {/* Generate All Button */}
      {assets.length > 0 && (
        <div className="bg-gray-900/50 border border-purple-500/30 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-semibold text-purple-400">
                Batch Image Generation
              </h3>
              <p className="text-gray-400 text-sm mt-1">
                Generate images for all {assets.length} prompts using Nano
                Banana
              </p>
            </div>
            <button
              onClick={generateAllImages}
              disabled={generatingImages}
              className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-medium py-3 px-6 rounded-lg transition-colors flex items-center gap-2"
            >
              {generatingImages ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <ImageIcon className="w-5 h-5" />
                  Generate All Images
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Assets Grid */}
      {assets.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {assets.map((asset) => (
            <AssetCard
              key={asset.id}
              asset={asset}
              onGenerate={generateSingleImage}
            />
          ))}
        </div>
      ) : (
        <div className="bg-gray-900/50 border border-purple-500/30 rounded-lg p-12 text-center">
          <ImageIcon className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">
            No prompts generated yet. Go to Prompt Preview tab to generate
            prompts first.
          </p>
        </div>
      )}
    </div>
  );

  const VideoStoryboardingTab = () => (
    <div className="bg-gray-900/50 border border-purple-500/30 rounded-lg p-12 text-center">
      <VideoIcon className="w-16 h-16 text-gray-600 mx-auto mb-4" />
      <h3 className="text-xl font-semibold text-gray-300 mb-2">
        Video Storyboarding
      </h3>
      <p className="text-gray-400">Coming soon...</p>
    </div>
  );

  const WorldLayoutTab = () => (
    <div className="bg-gray-900/50 border border-purple-500/30 rounded-lg p-12 text-center">
      <MapIcon className="w-16 h-16 text-gray-600 mx-auto mb-4" />
      <h3 className="text-xl font-semibold text-gray-300 mb-2">World Layout</h3>
      <p className="text-gray-400">Coming soon...</p>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case "Prompt Preview":
        return <PromptPreviewTab />;
      case "Image Generation":
        return <ImageGenerationTab />;
      case "Video Storyboarding":
        return <VideoStoryboardingTab />;
      case "World Layout":
        return <WorldLayoutTab />;
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
        <div className="relative z-10 container mx-auto px-4 py-16 sm:py-24">
          {/* Header */}
          <div className="pt-16 pb-8 text-center">
            <h1 className="text-4xl font-bold text-white">
              RenderPrepAgent Interface
            </h1>
            <p className="text-gray-300 text-sm mt-2">
              Transform narrative elements into visual assets
            </p>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center border-b border-purple-500/30 mb-8">
            {tabs.map((tab) => (
              <button
                key={tab.name}
                onClick={() => setActiveTab(tab.name)}
                className={`flex items-center gap-2 px-4 py-3 text-sm sm:text-base sm:px-6 font-medium transition-colors
                  ${
                    activeTab === tab.name
                      ? "border-b-2 border-purple-400 text-purple-400"
                      : "text-gray-400 hover:text-white"
                  }`}
              >
                <tab.icon className="w-5 h-5" />
                {tab.name}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="max-w-6xl mx-auto">{renderTabContent()}</div>
        </div>
      </div>
    </>
  );
};

// Asset Card Component
const AssetCard = ({ asset, onGenerate }) => {
  const [generating, setGenerating] = useState(false);
  const [showFullPrompt, setShowFullPrompt] = useState(false);

  const handleGenerate = async () => {
    console.log("[AssetCard] Generate clicked for asset:", asset.id);
    setGenerating(true);
    try {
      console.log("[AssetCard] Calling onGenerate...");
      await onGenerate(asset.id);
      console.log("[AssetCard] onGenerate completed successfully");
    } catch (err) {
      console.error("[AssetCard] Generation failed:", err);
      console.error("[AssetCard] Error details:", {
        message: err.message,
        stack: err.stack,
        name: err.name,
      });
      alert(`Failed to generate image: ${err.message}`);
    } finally {
      setGenerating(false);
      console.log("[AssetCard] Generation process finished");
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case "character-concept":
        return "text-green-400 border-green-500/30";
      case "environment":
        return "text-blue-400 border-blue-500/30";
      case "prop":
        return "text-amber-400 border-amber-500/30";
      case "storyboard":
        return "text-purple-400 border-purple-500/30";
      default:
        return "text-gray-400 border-gray-500/30";
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case "character-concept":
        return "👤";
      case "environment":
        return "🌍";
      case "prop":
        return "⚔️";
      case "storyboard":
        return "🎬";
      default:
        return "📦";
    }
  };

  return (
    <div className="bg-gray-900/50 border border-purple-500/30 rounded-lg overflow-hidden">
      {/* Image Preview */}
      {asset.imageUrl ? (
        <div className="relative h-48 bg-gray-800">
          <img
            src={asset.imageUrl}
            alt={asset.name}
            className="w-full h-full object-cover"
          />
          <div className="absolute top-2 right-2 bg-green-500 text-white px-2 py-1 rounded-full text-xs flex items-center gap-1">
            <CheckCircle className="w-3 h-3" />
            Generated
          </div>
        </div>
      ) : (
        <div className="h-48 bg-gray-800 flex items-center justify-center">
          <ImageIcon className="w-16 h-16 text-gray-600" />
        </div>
      )}

      {/* Card Content */}
      <div className="p-4">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-white font-semibold truncate">{asset.name}</h4>
          <span
            className={`text-xs px-2 py-1 rounded border ${getTypeColor(
              asset.type
            )}`}
          >
            {getTypeIcon(asset.type)} {asset.type}
          </span>
        </div>

        {/* Prompt Preview */}
        <div className="mb-4">
          <p className="text-gray-400 text-sm line-clamp-3">
            {showFullPrompt
              ? asset.prompt
              : asset.prompt.substring(0, 150) + "..."}
          </p>
          <button
            onClick={() => setShowFullPrompt(!showFullPrompt)}
            className="text-purple-400 text-xs mt-1 hover:underline"
          >
            {showFullPrompt ? "Show less" : "Show more"}
          </button>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          {!asset.imageUrl && (
            <button
              onClick={handleGenerate}
              disabled={generating || asset.status === "completed"}
              className="flex-1 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2 text-sm"
            >
              {generating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  Generate
                </>
              )}
            </button>
          )}
          {asset.imageUrl && (
            <a
              href={asset.imageUrl}
              download
              className="flex-1 bg-gray-700 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2 text-sm"
            >
              <Download className="w-4 h-4" />
              Download
            </a>
          )}
        </div>
      </div>
    </div>
  );
};

export default RenderPrepAgent;
