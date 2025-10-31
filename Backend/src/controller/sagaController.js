import {
  Project,
  World,
  Faction,
  Character,
  Location,
  PlotArc,
  Quest,
} from "../model/index.js";

// Initialize world for a project (first step of SagaAgent)
export const initializeWorld = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { name, lore, geography, timeline, researchSources } = req.body;

    // Check if world already exists
    let world = await World.findOne({ projectId });

    if (world) {
      // Update existing world
      Object.assign(world, {
        name,
        lore,
        geography,
        timeline,
        researchSources,
      });
      await world.save();
    } else {
      // Create new world
      world = new World({
        projectId,
        name,
        lore,
        geography,
        timeline,
        researchSources,
        approvalStatus: "pending",
      });
      await world.save();

      // Update project with world reference
      await Project.findByIdAndUpdate(projectId, {
        worldData: world._id,
        checkpoint: "world-lore",
        status: "world-building",
      });
    }

    res.status(200).json({
      success: true,
      message: "World initialized successfully",
      data: world,
      nextCheckpoint: "factions",
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to initialize world",
      error: error.message,
    });
  }
};

// Create factions for the world
export const createFactions = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { factions } = req.body;

    const world = await World.findOne({ projectId });
    if (!world) {
      return res.status(404).json({
        success: false,
        message: "World not found for this project",
      });
    }

    const createdFactions = [];
    for (const factionData of factions) {
      const faction = new Faction({
        ...factionData,
        worldId: world._id,
      });
      await faction.save();
      createdFactions.push(faction);
    }

    // Update world with faction references
    world.factions = createdFactions.map((f) => f._id);
    await world.save();

    // Update project checkpoint
    await Project.findByIdAndUpdate(projectId, {
      checkpoint: "factions",
      status: "narrative-development",
    });

    res.status(201).json({
      success: true,
      message: "Factions created successfully",
      data: createdFactions,
      nextCheckpoint: "characters",
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to create factions",
      error: error.message,
    });
  }
};

// Create characters for the world
export const createCharacters = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { characters } = req.body;

    const world = await World.findOne({ projectId });
    if (!world) {
      return res.status(404).json({
        success: false,
        message: "World not found for this project",
      });
    }

    const createdCharacters = [];
    for (const characterData of characters) {
      const character = new Character({
        ...characterData,
        worldId: world._id,
      });
      await character.save();
      createdCharacters.push(character);
    }

    // Update world with character references
    world.characters = createdCharacters.map((c) => c._id);
    await world.save();

    // Update project checkpoint
    await Project.findByIdAndUpdate(projectId, {
      checkpoint: "characters",
    });

    res.status(201).json({
      success: true,
      message: "Characters created successfully",
      data: createdCharacters,
      nextCheckpoint: "plot-arcs",
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to create characters",
      error: error.message,
    });
  }
};

// Create locations for the world
export const createLocations = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { locations } = req.body;

    const world = await World.findOne({ projectId });
    if (!world) {
      return res.status(404).json({
        success: false,
        message: "World not found for this project",
      });
    }

    const createdLocations = [];
    for (const locationData of locations) {
      const location = new Location({
        ...locationData,
        worldId: world._id,
      });
      await location.save();
      createdLocations.push(location);
    }

    // Update world with location references
    world.locations = createdLocations.map((l) => l._id);
    await world.save();

    res.status(201).json({
      success: true,
      message: "Locations created successfully",
      data: createdLocations,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to create locations",
      error: error.message,
    });
  }
};

// Create plot arcs for the world
export const createPlotArcs = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { plotArcs } = req.body;

    const world = await World.findOne({ projectId });
    if (!world) {
      return res.status(404).json({
        success: false,
        message: "World not found for this project",
      });
    }

    const createdPlotArcs = [];
    for (const plotArcData of plotArcs) {
      const plotArc = new PlotArc({
        ...plotArcData,
        worldId: world._id,
      });
      await plotArc.save();
      createdPlotArcs.push(plotArc);
    }

    // Update world with plot arc references
    world.plotArcs = createdPlotArcs.map((p) => p._id);
    await world.save();

    // Update project checkpoint
    await Project.findByIdAndUpdate(projectId, {
      checkpoint: "plot-arcs",
    });

    res.status(201).json({
      success: true,
      message: "Plot arcs created successfully",
      data: createdPlotArcs,
      nextCheckpoint: "quests",
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to create plot arcs",
      error: error.message,
    });
  }
};

// Create quests for the world
export const createQuests = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { quests } = req.body;

    const world = await World.findOne({ projectId });
    if (!world) {
      return res.status(404).json({
        success: false,
        message: "World not found for this project",
      });
    }

    const createdQuests = [];
    for (const questData of quests) {
      const quest = new Quest({
        ...questData,
        worldId: world._id,
      });
      await quest.save();
      createdQuests.push(quest);
    }

    // Update world with quest references
    world.quests = createdQuests.map((q) => q._id);
    await world.save();

    // Update project checkpoint
    await Project.findByIdAndUpdate(projectId, {
      checkpoint: "quests",
    });

    res.status(201).json({
      success: true,
      message: "Quests created successfully",
      data: createdQuests,
      nextCheckpoint: "dialogue",
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to create quests",
      error: error.message,
    });
  }
};

// Get current world state
export const getWorldState = async (req, res) => {
  try {
    const { projectId } = req.params;

    const world = await World.findOne({ projectId })
      .populate("factions")
      .populate("characters")
      .populate("locations")
      .populate("plotArcs")
      .populate("quests");

    if (!world) {
      return res.status(404).json({
        success: false,
        message: "World not found for this project",
      });
    }

    const project = await Project.findById(projectId);

    res.status(200).json({
      success: true,
      data: {
        world,
        currentCheckpoint: project.checkpoint,
        status: project.status,
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to fetch world state",
      error: error.message,
    });
  }
};

// Approve a narrative element
export const approveElement = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { elementType, elementId, approvalStatus, feedback } = req.body;

    let Model;
    switch (elementType) {
      case "world":
        Model = World;
        break;
      case "faction":
        Model = Faction;
        break;
      case "character":
        Model = Character;
        break;
      case "location":
        Model = Location;
        break;
      case "plotArc":
        Model = PlotArc;
        break;
      case "quest":
        Model = Quest;
        break;
      default:
        return res.status(400).json({
          success: false,
          message: "Invalid element type",
        });
    }

    const element = await Model.findByIdAndUpdate(
      elementId,
      { approvalStatus, feedback },
      { new: true }
    );

    if (!element) {
      return res.status(404).json({
        success: false,
        message: "Element not found",
      });
    }

    res.status(200).json({
      success: true,
      message: "Element approval status updated",
      data: element,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to update approval status",
      error: error.message,
    });
  }
};
