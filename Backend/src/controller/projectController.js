import { Project, World } from "../model/index.js";

// Create a new project
export const createProject = async (req, res) => {
  try {
    const { name, description, concept, genre, metadata } = req.body;

    const project = new Project({
      name,
      description,
      concept,
      genre,
      metadata,
      status: "concept",
      checkpoint: "concept",
    });

    await project.save();

    res.status(201).json({
      success: true,
      message: "Project created successfully",
      data: project,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to create project",
      error: error.message,
    });
  }
};

// Get all projects
export const getAllProjects = async (req, res) => {
  try {
    const projects = await Project.find()
      .populate("worldData")
      .populate("assets")
      .sort({ createdAt: -1 });

    res.status(200).json({
      success: true,
      data: projects,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to fetch projects",
      error: error.message,
    });
  }
};

// Get project by ID
export const getProjectById = async (req, res) => {
  try {
    const { projectId } = req.params;

    const project = await Project.findById(projectId)
      .populate("worldData")
      .populate("assets");

    if (!project) {
      return res.status(404).json({
        success: false,
        message: "Project not found",
      });
    }

    res.status(200).json({
      success: true,
      data: project,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to fetch project",
      error: error.message,
    });
  }
};

// Update project
export const updateProject = async (req, res) => {
  try {
    const { projectId } = req.params;
    const updates = req.body;

    const project = await Project.findByIdAndUpdate(projectId, updates, {
      new: true,
      runValidators: true,
    });

    if (!project) {
      return res.status(404).json({
        success: false,
        message: "Project not found",
      });
    }

    res.status(200).json({
      success: true,
      message: "Project updated successfully",
      data: project,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to update project",
      error: error.message,
    });
  }
};

// Update project checkpoint (for LangGraph workflow)
export const updateCheckpoint = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { checkpoint, status } = req.body;

    const project = await Project.findByIdAndUpdate(
      projectId,
      { checkpoint, status },
      { new: true }
    );

    if (!project) {
      return res.status(404).json({
        success: false,
        message: "Project not found",
      });
    }

    res.status(200).json({
      success: true,
      message: "Checkpoint updated successfully",
      data: {
        projectId: project._id,
        checkpoint: project.checkpoint,
        status: project.status,
      },
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to update checkpoint",
      error: error.message,
    });
  }
};

// Delete project
export const deleteProject = async (req, res) => {
  try {
    const { projectId } = req.params;

    // Also delete associated world data
    await World.findOneAndDelete({ projectId });

    const project = await Project.findByIdAndDelete(projectId);

    if (!project) {
      return res.status(404).json({
        success: false,
        message: "Project not found",
      });
    }

    res.status(200).json({
      success: true,
      message: "Project deleted successfully",
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to delete project",
      error: error.message,
    });
  }
};
