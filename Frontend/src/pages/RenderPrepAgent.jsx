import React, { useState } from "react";
import Navbar from "../components/Navbar";
import {
  TextIcon,
  ImageIcon,
  VideoIcon,
  MapIcon,
  CheckIcon,
  SendIcon,
} from "lucide-react";
// --- INLINE SVG ICONS ---

// Regenerate Icon
const RefreshIcon = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={1.5}
    stroke="currentColor"
    {...props}
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0 0v4.992m0 0h-4.992"
    />
  </svg>
);

const RenderPrepAgent = () => {
  const [activeTab, setActiveTab] = useState("Prompt Preview");

  const tabs = [
    { name: "Prompt Preview", icon: TextIcon },
    { name: "Image Generation", icon: ImageIcon },
    { name: "Video Storyboarding", icon: VideoIcon },
    { name: "World Layout", icon: MapIcon },
  ];

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
            <h1 className="text-4xl font-bold text-white">
              RenderPrepAgent Interface
            </h1>
            <p className="text-gray-300 text-sm">
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

// --- TAB COMPONENTS ---

const HITLControls = () => (
  <div className="flex flex-wrap items-center gap-3 mt-6 p-4 bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-xl">
    <span className="text-sm font-medium text-gray-300 mr-2">Actions:</span>
    <button className="flex items-center gap-2 px-4 py-2 bg-green-600/80 text-white hover:bg-green-700 rounded-lg transition-colors text-sm font-medium">
      <CheckIcon className="w-4 h-4" /> Approve
    </button>
    <button className="flex items-center gap-2 px-4 py-2 bg-yellow-600/80 text-white hover:bg-yellow-700 rounded-lg transition-colors text-sm font-medium">
      <RefreshIcon className="w-4 h-4" /> Regenerate
    </button>
    <button className="flex items-center gap-2 px-4 py-2 bg-blue-600/80 text-white hover:bg-blue-700 rounded-lg transition-colors text-sm font-medium">
      <SendIcon className="w-4 h-4" /> Send to Engine
    </button>
  </div>
);

const PromptPreviewTab = () => (
  <div className="space-y-6">
    <h2 className="text-2xl font-bold text-white mb-4">Prompt Preview</h2>
    <div className="bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl shadow-2xl p-6">
      <h3 className="text-lg font-semibold text-purple-300 mb-3">
        Character: 'Detective Harding'
      </h3>
      <pre className="text-gray-300 text-sm bg-gray-800/70 p-4 rounded-lg overflow-x-auto">
        {`{
  "entity": "Detective Harding",
  "type": "character",
  "description": "A weary, cynical detective in his late 40s, 1920s Chicago.",
  "visual_style": "Film noir, high contrast lighting, gritty realism",
  "prompt": "A close-up portrait of a 1920s detective, weary eyes, fedora casting a shadow, trench coat collar up, rain-slicked city street at night in the background, film noir style."
}`}
      </pre>
    </div>
    <div className="bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl shadow-2xl p-6">
      <h3 className="text-lg font-semibold text-purple-300 mb-3">
        Environment: 'The Onyx Club'
      </h3>
      <pre className="text-gray-300 text-sm bg-gray-800/70 p-4 rounded-lg overflow-x-auto">
        {`{
  "entity": "The Onyx Club",
  "type": "environment",
  "description": "A smoky, opulent 1920s speakeasy, dimly lit, velvet curtains.",
  "visual_style": "Art deco, opulent, dark, smoky atmosphere",
  "prompt": "Wide interior shot of a 1920s speakeasy, 'The Onyx Club', art deco design, velvet booths, smoky atmosphere, dimly lit, jazz band on a small stage."
}`}
      </pre>
    </div>
    <HITLControls />
  </div>
);

const ImageGenerationTab = () => {
  const [prompt, setPrompt] = useState("");
  const [aspectRatio, setAspectRatio] = useState("16:9");
  const [stylePreset, setStylePreset] = useState("Film Noir");
  const [negativePrompt, setNegativePrompt] = useState("");
  const [generatedImage, setGeneratedImage] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);
  const [generationHistory, setGenerationHistory] = useState([]);

  const handleGenerateImage = async () => {
    if (!prompt.trim()) {
      setError("Please enter a prompt");
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      const response = await fetch(
        "http://localhost:4000/api/image-generation/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            prompt,
            aspectRatio,
            stylePreset,
            negativePrompt,
          }),
        }
      );

      const data = await response.json();

      if (data.success) {
        setGeneratedImage(data.data);
        // Add to history
        setGenerationHistory((prev) => [data.data, ...prev].slice(0, 6));
      } else {
        setError(data.message || "Failed to generate image");
      }
    } catch (err) {
      setError(
        "Failed to connect to server. Make sure the backend is running."
      );
      console.error("Error generating image:", err);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white mb-4">Image Generation</h2>

      {/* Error Display */}
      {error && (
        <div className="bg-red-900/30 border border-red-500/50 rounded-lg p-4 text-red-200">
          {error}
        </div>
      )}

      {/* Current Generation Display */}
      <div className="bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl shadow-2xl p-6 flex flex-col md:flex-row gap-6">
        <div className="md:w-1/2">
          <h3 className="text-xl font-semibold text-purple-300 mb-3">
            Generated Image
          </h3>
          <div className="aspect-video bg-gray-800/70 rounded-lg flex items-center justify-center mb-3 overflow-hidden">
            {isGenerating ? (
              <div className="flex flex-col items-center gap-3">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
                <span className="text-gray-400">Generating image...</span>
              </div>
            ) : generatedImage ? (
              <img
                src={generatedImage.imageUrl}
                alt="Generated"
                className="w-full h-full object-contain"
              />
            ) : (
              <span className="text-gray-500">
                Generated Image Will Appear Here
              </span>
            )}
          </div>
          {generatedImage && (
            <>
              <p className="text-sm text-gray-400">
                Model: {generatedImage.model || "gemini-2.0-flash-exp"} | Aspect
                Ratio: {aspectRatio} | Style: {stylePreset}
              </p>
              <p className="text-sm text-gray-400 mt-1">
                Prompt: "{generatedImage.prompt}"
              </p>
              {generatedImage.text && (
                <p className="text-xs text-gray-500 mt-1">
                  AI Response: {generatedImage.text}
                </p>
              )}
            </>
          )}
        </div>
        <div className="md:w-1/2 flex flex-col justify-between">
          <div>
            <h3 className="text-xl font-semibold text-purple-300 mb-3">
              Generate Parameters
            </h3>
            <div className="space-y-4">
              {/* Prompt Input */}
              <div>
                <label
                  htmlFor="promptInput"
                  className="block text-sm font-medium text-gray-300 mb-1"
                >
                  Prompt *
                </label>
                <textarea
                  id="promptInput"
                  rows="3"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="w-full p-2 bg-gray-800/70 border border-gray-700 rounded-lg text-white text-sm focus:ring-purple-500 focus:border-purple-500"
                  placeholder="e.g., A close-up portrait of a 1920s detective, weary eyes, fedora casting a shadow..."
                ></textarea>
              </div>
              {/* Aspect Ratio */}
              <div>
                <label
                  htmlFor="aspectRatio"
                  className="block text-sm font-medium text-gray-300 mb-1"
                >
                  Aspect Ratio
                </label>
                <select
                  id="aspectRatio"
                  value={aspectRatio}
                  onChange={(e) => setAspectRatio(e.target.value)}
                  className="w-full p-2 bg-gray-800/70 border border-gray-700 rounded-lg text-white text-sm"
                >
                  <option>16:9 (Landscape)</option>
                  <option>9:16 (Portrait)</option>
                  <option>1:1 (Square)</option>
                  <option>4:3 (Traditional)</option>
                </select>
              </div>
              {/* Style Preset */}
              <div>
                <label
                  htmlFor="stylePreset"
                  className="block text-sm font-medium text-gray-300 mb-1"
                >
                  Style Preset
                </label>
                <select
                  id="stylePreset"
                  value={stylePreset}
                  onChange={(e) => setStylePreset(e.target.value)}
                  className="w-full p-2 bg-gray-800/70 border border-gray-700 rounded-lg text-white text-sm"
                >
                  <option>Film Noir</option>
                  <option>Art Deco</option>
                  <option>Gritty Realism</option>
                  <option>Anime</option>
                  <option>Fantasy Art</option>
                  <option>Photorealistic</option>
                </select>
              </div>
              {/* Negative Prompt */}
              <div>
                <label
                  htmlFor="negativePrompt"
                  className="block text-sm font-medium text-gray-300 mb-1"
                >
                  Negative Prompt (Optional)
                </label>
                <textarea
                  id="negativePrompt"
                  rows="2"
                  value={negativePrompt}
                  onChange={(e) => setNegativePrompt(e.target.value)}
                  className="w-full p-2 bg-gray-800/70 border border-gray-700 rounded-lg text-white text-sm focus:ring-purple-500 focus:border-purple-500"
                  placeholder="e.g., blurry, distorted, low quality, bad anatomy"
                ></textarea>
              </div>
            </div>
          </div>
          {/* Generate Button */}
          <button
            onClick={handleGenerateImage}
            disabled={isGenerating}
            className={`mt-6 flex items-center justify-center gap-2 px-6 py-3 rounded-lg transition-colors font-semibold text-lg ${
              isGenerating
                ? "bg-gray-600 cursor-not-allowed"
                : "bg-purple-600/80 hover:bg-purple-700 text-white"
            }`}
          >
            {isGenerating ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Generating...
              </>
            ) : (
              <>
                <ImageIcon className="w-6 h-6" /> Generate Image
              </>
            )}
          </button>
        </div>
      </div>

      {/* Gallery of Previous Generations */}
      {generationHistory.length > 0 && (
        <>
          <h3 className="text-2xl font-bold text-white mt-8 mb-4">
            Previous Generations
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {generationHistory.map((item, index) => (
              <div
                key={index}
                className="bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl shadow-2xl p-4"
              >
                <div className="aspect-video bg-gray-800/70 rounded-lg flex items-center justify-center mb-3 overflow-hidden">
                  <img
                    src={item.imageUrl}
                    alt={`Generation ${index + 1}`}
                    className="w-full h-full object-contain"
                  />
                </div>
                <h3
                  className="text-lg font-semibold text-white truncate"
                  title={item.prompt}
                >
                  {item.prompt.substring(0, 40)}...
                </h3>
                <p className="text-sm text-gray-400">
                  Style: {item.stylePreset}
                </p>
                <div className="flex justify-end gap-2 mt-3">
                  <button
                    onClick={() => {
                      setPrompt(item.prompt);
                      setStylePreset(item.stylePreset);
                      setAspectRatio(item.aspectRatio);
                    }}
                    className="p-2 bg-yellow-600/80 hover:bg-yellow-700 rounded-full text-white transition-colors"
                    title="Use this prompt"
                  >
                    <RefreshIcon className="w-4 h-4" />
                  </button>
                  <button className="p-2 bg-green-600/80 hover:bg-green-700 rounded-full text-white transition-colors">
                    <CheckIcon className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {/* HITL Controls for the entire tab */}
      <HITLControls />
    </div>
  );
};

const VideoStoryboardingTab = () => (
  <div>
    <h2 className="text-2xl font-bold text-white mb-4">
      Video Storyboarding: 'Opening Scene'
    </h2>
    <div className="flex overflow-x-auto space-x-4 p-4 bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl">
      {[
        { num: 1, desc: "EXT. CITY STREET - NIGHT" },
        { num: 2, desc: "Rain hits pavement" },
        { num: 3, desc: "Detective Harding arrives" },
        { num: 4, desc: "CU - Harding lights cigarette" },
        { num: 5, desc: "POV - Enters The Onyx Club" },
      ].map((frame) => (
        <div key={frame.num} className="flex-shrink-0 w-64">
          <div className="aspect-video bg-gray-800/70 rounded-lg flex items-center justify-center mb-2">
            <span className="text-gray-500">Frame {frame.num}</span>
          </div>
          <p className="text-sm text-white text-center">{frame.desc}</p>
        </div>
      ))}
    </div>
    <HITLControls />
  </div>
);

const WorldLayoutTab = () => (
  <div>
    <h2 className="text-2xl font-bold text-white mb-4">
      World Layout Viewer (Genie Integration)
    </h2>
    <div className="bg-gray-900/60 backdrop-blur-md border border-purple-500/30 rounded-2xl shadow-2xl p-6">
      <div className="aspect-video bg-gray-800/70 rounded-lg flex items-center justify-center">
        <p className="text-gray-500">Map / Grid-based display placeholder</p>
      </div>
    </div>
    <HITLControls />
  </div>
);

export default RenderPrepAgent;
