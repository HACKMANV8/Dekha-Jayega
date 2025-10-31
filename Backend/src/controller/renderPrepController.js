import {
  Asset,
  Project,
  World,
  Character,
  Location,
  PlotArc,
  Quest,
} from "../model/index.js";

// Generate character concept art prompts
export const generateCharacterConcepts = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { characterIds, stylePreferences } = req.body;

    const world = await World.findOne({ projectId }).populate("characters");
    if (!world) {
      return res.status(404).json({
        success: false,
        message: "World not found for this project",
      });
    }

    const generatedAssets = [];

    for (const characterId of characterIds) {
      const character = await Character.findById(characterId);
      if (!character) continue;

      // Generate detailed prompt for character concept art
      const detailedPrompt = `Character concept art: ${character.name}, ${
        character.description
      }. 
        Race: ${character.background.race}, Class: ${
        character.background.class
      }. 
        Appearance: ${character.appearance.physicalDescription}. 
        Clothing: ${character.appearance.clothing}. 
        Personality traits: ${character.personality.traits.join(", ")}. 
        Notable features: ${character.appearance.notableFeatures.join(", ")}.`;

      const stylePrompt = stylePreferences
        ? `Art style: ${stylePreferences.style}, ${stylePreferences.mood}, ${stylePreferences.technique}`
        : "High-quality concept art, detailed character design";

      const asset = new Asset({
        projectId,
        name: `${character.name} - Character Concept`,
        type: "character-concept",
        category: "image",
        sourceEntity: {
          entityType: "Character",
          entityId: characterId,
        },
        prompts: {
          detailed: detailedPrompt,
          style: stylePrompt,
          technical:
            "High resolution, concept art style, detailed character sheet",
          composition: "Full body character pose, multiple angle views",
          lighting: "Professional studio lighting",
          mood: character.personality.traits.includes("dark")
            ? "dramatic"
            : "heroic",
        },
        metadata: {
          resolution: "1024x1024",
          aspectRatio: "1:1",
          style: stylePreferences?.style || "fantasy-realistic",
          tags: [
            character.role,
            character.background.race,
            character.background.class,
          ],
        },
        status: "pending",
      });

      await asset.save();
      generatedAssets.push(asset);
    }

    // Update project checkpoint
    await Project.findByIdAndUpdate(projectId, {
      checkpoint: "render-prep",
      status: "asset-generation",
    });

    res.status(201).json({
      success: true,
      message: "Character concept prompts generated successfully",
      data: generatedAssets,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to generate character concepts",
      error: error.message,
    });
  }
};

// Generate environment art prompts
export const generateEnvironmentPrompts = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { locationIds, environmentPreferences } = req.body;

    const world = await World.findOne({ projectId }).populate("locations");
    if (!world) {
      return res.status(404).json({
        success: false,
        message: "World not found for this project",
      });
    }

    const generatedAssets = [];

    for (const locationId of locationIds) {
      const location = await Location.findById(locationId);
      if (!location) continue;

      // Generate detailed prompt for environment art
      const detailedPrompt = `Environment concept: ${location.name}, ${
        location.description
      }. 
        Type: ${location.type}. Terrain: ${location.geography.terrain}. 
        Climate: ${location.geography.climate}. Architecture: ${
        location.features.architecture
      }. 
        Notable buildings: ${location.features.notableBuildings.join(", ")}. 
        Natural features: ${location.features.naturalFeatures.join(", ")}. 
        Atmosphere: ${location.atmosphere.mood}, ${
        location.atmosphere.lighting
      }. 
        Weather: ${location.atmosphere.weather}.`;

      const asset = new Asset({
        projectId,
        name: `${location.name} - Environment`,
        type: "environment",
        category: "image",
        sourceEntity: {
          entityType: "Location",
          entityId: locationId,
        },
        prompts: {
          detailed: detailedPrompt,
          style: environmentPreferences?.style || "fantasy landscape art",
          technical: "Wide shot, establishing shot, high detail environment",
          composition: "Cinematic composition, rule of thirds",
          lighting: location.atmosphere.lighting,
          mood: location.atmosphere.mood,
        },
        metadata: {
          resolution: "1920x1080",
          aspectRatio: "16:9",
          style: environmentPreferences?.style || "fantasy-realistic",
          colorPalette: environmentPreferences?.colorPalette || [
            "natural",
            "atmospheric",
          ],
          tags: [
            location.type,
            location.geography.terrain,
            location.geography.climate,
          ],
        },
        status: "pending",
      });

      await asset.save();
      generatedAssets.push(asset);
    }

    res.status(201).json({
      success: true,
      message: "Environment prompts generated successfully",
      data: generatedAssets,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to generate environment prompts",
      error: error.message,
    });
  }
};

// Generate keyframe sequences for cinematics
export const generateKeyframeSequences = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { plotArcIds, questIds, sequencePreferences } = req.body;

    const world = await World.findOne({ projectId });
    if (!world) {
      return res.status(404).json({
        success: false,
        message: "World not found for this project",
      });
    }

    const generatedAssets = [];

    // Generate keyframes for plot arcs
    if (plotArcIds) {
      for (const plotArcId of plotArcIds) {
        const plotArc = await PlotArc.findById(plotArcId);
        if (!plotArc) continue;

        for (const [
          index,
          visualSequence,
        ] of plotArc.visualSequences.entries()) {
          const asset = new Asset({
            projectId,
            name: `${plotArc.title} - Keyframe ${index + 1}`,
            type: "keyframe",
            category: "image",
            sourceEntity: {
              entityType: "PlotArc",
              entityId: plotArcId,
            },
            prompts: {
              detailed: visualSequence.sceneDescription,
              style: sequencePreferences?.style || "cinematic storyboard",
              technical: "Storyboard keyframe, cinematic composition",
              composition: "Cinematic framing, dynamic angles",
              lighting: "Dramatic cinematic lighting",
              mood: "Epic, story-driven",
            },
            metadata: {
              resolution: "1920x1080",
              aspectRatio: "16:9",
              style: "cinematic",
              tags: ["keyframe", "storyboard", plotArc.type],
            },
            videoSequence: {
              isSequence: true,
              sequenceOrder: index + 1,
              duration: sequencePreferences?.frameDuration || 3,
              transitions: visualSequence.cinematicNotes,
            },
            status: "pending",
          });

          await asset.save();
          generatedAssets.push(asset);
        }
      }
    }

    // Generate keyframes for quest cinematics
    if (questIds) {
      for (const questId of questIds) {
        const quest = await Quest.findById(questId);
        if (!quest || !quest.visualElements.cutscenes.length) continue;

        for (const [
          index,
          cutscene,
        ] of quest.visualElements.cutscenes.entries()) {
          const asset = new Asset({
            projectId,
            name: `${quest.title} - Cutscene ${index + 1}`,
            type: "keyframe",
            category: "image",
            sourceEntity: {
              entityType: "Quest",
              entityId: questId,
            },
            prompts: {
              detailed: cutscene,
              style: "game cutscene, cinematic",
              technical: "Game cutscene keyframe, high detail",
              composition: "Game camera angles",
              lighting: "Game lighting",
              mood: "Interactive narrative",
            },
            metadata: {
              resolution: "1920x1080",
              aspectRatio: "16:9",
              style: "game-cinematic",
              tags: ["cutscene", "quest", quest.type],
            },
            videoSequence: {
              isSequence: true,
              sequenceOrder: index + 1,
              duration: 5,
            },
            status: "pending",
          });

          await asset.save();
          generatedAssets.push(asset);
        }
      }
    }

    res.status(201).json({
      success: true,
      message: "Keyframe sequences generated successfully",
      data: generatedAssets,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to generate keyframe sequences",
      error: error.message,
    });
  }
};

// Generate storyboard for video generation (Veo preparation)
export const generateStoryboard = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { assetIds, storyboardPreferences } = req.body;

    // Find all keyframe assets for sequencing
    const keyframeAssets = await Asset.find({
      _id: { $in: assetIds },
      type: "keyframe",
      projectId,
    }).sort({ "videoSequence.sequenceOrder": 1 });

    if (keyframeAssets.length === 0) {
      return res.status(400).json({
        success: false,
        message: "No keyframe assets found for storyboard generation",
      });
    }

    // Create storyboard asset
    const storyboard = new Asset({
      projectId,
      name: `Storyboard - ${storyboardPreferences?.title || "Game Sequence"}`,
      type: "storyboard",
      category: "video",
      prompts: {
        detailed: `Video sequence storyboard with ${keyframeAssets.length} keyframes`,
        style: "cinematic video sequence",
        technical: "Video storyboard for Veo generation",
        composition: "Sequential cinematic shots",
        lighting: "Consistent lighting across sequence",
        mood: "Narrative-driven",
      },
      metadata: {
        resolution: "1920x1080",
        aspectRatio: "16:9",
        style: "video-storyboard",
        tags: ["storyboard", "video-sequence", "veo-ready"],
      },
      videoSequence: {
        isSequence: true,
        sequenceOrder: 1,
        duration: keyframeAssets.reduce(
          (total, asset) => total + (asset.videoSequence.duration || 3),
          0
        ),
        transitions: storyboardPreferences?.transitions || "smooth cuts",
      },
      worldGeneration: {
        procedural: false,
        layout: {
          keyframes: keyframeAssets.map((asset) => ({
            id: asset._id,
            order: asset.videoSequence.sequenceOrder,
            duration: asset.videoSequence.duration,
            prompt: asset.prompts.detailed,
          })),
        },
        assetList: keyframeAssets.map((asset) => asset._id),
        interactivity: {
          videoReady: true,
          veoCompatible: true,
        },
      },
      status: "pending",
    });

    await storyboard.save();

    res.status(201).json({
      success: true,
      message: "Storyboard generated successfully",
      data: storyboard,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to generate storyboard",
      error: error.message,
    });
  }
};

// Generate world generation data (Genie preparation)
export const generateWorldData = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { worldPreferences } = req.body;

    const world = await World.findOne({ projectId })
      .populate("locations")
      .populate("characters")
      .populate("factions");

    if (!world) {
      return res.status(404).json({
        success: false,
        message: "World not found for this project",
      });
    }

    // Create comprehensive world generation asset
    const worldAsset = new Asset({
      projectId,
      name: `${world.name} - Interactive World Data`,
      type: "environment",
      category: "interactive",
      sourceEntity: {
        entityType: "World",
        entityId: world._id,
      },
      prompts: {
        detailed: `Interactive world generation data for ${world.name}`,
        style: "procedural world generation",
        technical: "Genie-compatible world data",
        composition: "Complete world layout",
        lighting: "Dynamic world lighting",
        mood: "Interactive exploration",
      },
      metadata: {
        style: "interactive-world",
        tags: ["world-generation", "genie-ready", "interactive"],
      },
      worldGeneration: {
        procedural: true,
        layout: {
          world: {
            name: world.name,
            lore: world.lore,
            geography: world.geography,
          },
          locations: world.locations.map((location) => ({
            id: location._id,
            name: location.name,
            type: location.type,
            coordinates: location.geography.coordinates,
            connections: location.connections,
            features: location.features,
          })),
          npcs: world.characters.map((character) => ({
            id: character._id,
            name: character.name,
            role: character.role,
            location: character.location,
            dialogue: character.dialogue,
          })),
          factions: world.factions.map((faction) => ({
            id: faction._id,
            name: faction.name,
            territory: faction.territory,
            relationships: faction.relationships,
          })),
        },
        assetList: [
          "terrain_generation",
          "building_placement",
          "npc_spawning",
          "quest_triggers",
          "faction_territories",
        ],
        interactivity: {
          navigable: true,
          npcInteraction: true,
          questSystem: true,
          factionSystem: true,
          genieCompatible: true,
        },
      },
      status: "pending",
    });

    await worldAsset.save();

    res.status(201).json({
      success: true,
      message: "World generation data created successfully",
      data: worldAsset,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to generate world data",
      error: error.message,
    });
  }
};

// Get render preparation status
export const getRenderPrepStatus = async (req, res) => {
  try {
    const { projectId } = req.params;

    const assets = await Asset.find({ projectId })
      .populate("sourceEntity.entityId")
      .sort({ createdAt: -1 });

    const assetsByType = assets.reduce((acc, asset) => {
      if (!acc[asset.type]) acc[asset.type] = [];
      acc[asset.type].push(asset);
      return acc;
    }, {});

    res.status(200).json({
      success: true,
      data: {
        totalAssets: assets.length,
        assetsByType,
        readyForGeneration: assets.filter((a) => a.status === "pending").length,
        completed: assets.filter((a) => a.status === "completed").length,
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to fetch render prep status",
      error: error.message,
    });
  }
};
