import { SagaSession } from "../model/index.js";
import { Project } from "../model/index.js";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";

// Configuration for Python Saga API Server
const SAGA_API_BASE_URL = process.env.SAGA_API_URL || "http://localhost:8001";

/**
 * Convert Python API stage format (underscore) to Project checkpoint format (hyphen)
 */
const convertStageToCheckpoint = (stage) => {
  const mapping = {
    initial: "concept",
    research: "concept",
    concept: "concept",
    world_lore: "world-lore",
    factions: "factions",
    characters: "characters",
    plot_arcs: "plot-arcs",
    questlines: "quests",
    complete: "quests",
  };
  return mapping[stage] || "concept";
};

/**
 * Start a new Saga workflow session
 * Communicates with Python FastAPI server to initialize SagaAgent
 */
export const startSagaWorkflow = async (req, res) => {
  try {
    const {
      projectId,
      topic,
      researchRequired = false,
      researchQuestion = null,
      model = null,
      modelTemperature = null,
      parallelExecution = false,
    } = req.body;

    // Validate required fields
    if (!projectId || !topic) {
      return res.status(400).json({
        success: false,
        message: "projectId and topic are required",
      });
    }

    // Check if project exists
    const project = await Project.findById(projectId);
    if (!project) {
      return res.status(404).json({
        success: false,
        message: "Project not found",
      });
    }

    // Generate session ID
    const sessionId = uuidv4();

    console.log(
      `[SAGA] Starting workflow for project ${projectId}, session ${sessionId}`
    );

    // Call Python Saga API to start workflow
    const pythonPayload = {
      topic,
      research_required: researchRequired ? "required" : "not_required",
      research_question: researchQuestion,
      model,
      model_temperature: modelTemperature,
      parallel_execution: parallelExecution,
    };

    console.log(
      `[SAGA] Calling Python API at ${SAGA_API_BASE_URL}/workflow/start`
    );

    const pythonResponse = await axios.post(
      `${SAGA_API_BASE_URL}/workflow/start`,
      pythonPayload,
      {
        timeout: 120000, // 2 minutes timeout for initial generation
      }
    );

    const pythonData = pythonResponse.data;

    // Create SagaSession in MongoDB
    const sagaSession = new SagaSession({
      sessionId: pythonData.session_id || sessionId,
      projectId,
      topic,
      currentStage: pythonData.current_stage || "concept",
      awaitingFeedback: pythonData.awaiting_feedback || false,
      status: "active",
      researchRequired,
      researchQuestion,
      compressedResearch: pythonData.data?.compressed_research || "",
      rawNotes: pythonData.data?.raw_notes || [],
      concept: pythonData.data?.concept || null,
      worldLore: pythonData.data?.world_lore || null,
      factions: pythonData.data?.factions || [],
      characters: pythonData.data?.characters || [],
      plotArcs: pythonData.data?.plot_arcs || [],
      questlines: pythonData.data?.questlines || [],
      config: {
        model: model,
        model_temperature: modelTemperature,
        parallel_execution: parallelExecution,
      },
    });

    await sagaSession.save();

    // Update project status
    project.status = "world-building";
    project.checkpoint = convertStageToCheckpoint(
      pythonData.current_stage || "concept"
    );
    await project.save();

    console.log(
      `[SAGA] Session ${sagaSession.sessionId} created, stage: ${sagaSession.currentStage}`
    );

    res.status(200).json({
      success: true,
      message: pythonData.message || "Saga workflow started successfully",
      data: {
        sessionId: sagaSession.sessionId,
        currentStage: sagaSession.currentStage,
        awaitingFeedback: sagaSession.awaitingFeedback,
        concept: sagaSession.concept,
        worldLore: sagaSession.worldLore,
        factions: sagaSession.factions,
        characters: sagaSession.characters,
        plotArcs: sagaSession.plotArcs,
        questlines: sagaSession.questlines,
      },
    });
  } catch (error) {
    console.error("[SAGA ERROR] Start workflow failed:", error.message);

    // Handle Python API errors
    if (error.response) {
      return res.status(error.response.status || 500).json({
        success: false,
        message:
          error.response.data?.detail ||
          "Failed to start saga workflow in Python API",
        error: error.response.data,
      });
    }

    res.status(500).json({
      success: false,
      message: "Failed to start saga workflow",
      error: error.message,
    });
  }
};

/**
 * Submit feedback for the current stage
 * Allows human-in-the-loop editing
 */
export const submitFeedback = async (req, res) => {
  try {
    const { sessionId, feedback } = req.body;

    if (!sessionId || !feedback) {
      return res.status(400).json({
        success: false,
        message: "sessionId and feedback are required",
      });
    }

    // Find session in MongoDB
    const sagaSession = await SagaSession.findOne({ sessionId });
    if (!sagaSession) {
      return res.status(404).json({
        success: false,
        message: "Saga session not found",
      });
    }

    console.log(
      `[SAGA] Submitting feedback for session ${sessionId}, stage: ${sagaSession.currentStage}`
    );

    // Call Python API to submit feedback
    const pythonResponse = await axios.post(
      `${SAGA_API_BASE_URL}/workflow/feedback`,
      {
        session_id: sessionId,
        feedback,
      },
      {
        timeout: 120000, // 2 minutes timeout for regeneration
      }
    );

    const pythonData = pythonResponse.data;

    // Update session with regenerated data
    sagaSession.currentStage = pythonData.current_stage;
    sagaSession.awaitingFeedback = pythonData.awaiting_feedback;

    // Update stage-specific data
    if (pythonData.data?.concept) sagaSession.concept = pythonData.data.concept;
    if (pythonData.data?.world_lore)
      sagaSession.worldLore = pythonData.data.world_lore;
    if (pythonData.data?.factions)
      sagaSession.factions = pythonData.data.factions;
    if (pythonData.data?.characters)
      sagaSession.characters = pythonData.data.characters;
    if (pythonData.data?.plot_arcs)
      sagaSession.plotArcs = pythonData.data.plot_arcs;
    if (pythonData.data?.questlines)
      sagaSession.questlines = pythonData.data.questlines;

    // Track feedback history
    sagaSession.feedbackHistory.push({
      stage: sagaSession.currentStage,
      feedback,
      timestamp: new Date(),
    });

    await sagaSession.save();

    console.log(
      `[SAGA] Feedback processed for session ${sessionId}, regenerated ${sagaSession.currentStage}`
    );

    res.status(200).json({
      success: true,
      message: pythonData.message || "Feedback submitted and stage regenerated",
      data: {
        sessionId: sagaSession.sessionId,
        currentStage: sagaSession.currentStage,
        awaitingFeedback: sagaSession.awaitingFeedback,
        concept: sagaSession.concept,
        worldLore: sagaSession.worldLore,
        factions: sagaSession.factions,
        characters: sagaSession.characters,
        plotArcs: sagaSession.plotArcs,
        questlines: sagaSession.questlines,
      },
    });
  } catch (error) {
    console.error("[SAGA ERROR] Submit feedback failed:", error.message);

    if (error.response) {
      return res.status(error.response.status || 500).json({
        success: false,
        message:
          error.response.data?.detail ||
          "Failed to submit feedback to Python API",
        error: error.response.data,
      });
    }

    res.status(500).json({
      success: false,
      message: "Failed to submit feedback",
      error: error.message,
    });
  }
};

/**
 * Continue to the next stage in the workflow
 */
export const continueWorkflow = async (req, res) => {
  try {
    const { sessionId } = req.body;

    if (!sessionId) {
      return res.status(400).json({
        success: false,
        message: "sessionId is required",
      });
    }

    // Find session in MongoDB
    const sagaSession = await SagaSession.findOne({ sessionId });
    if (!sagaSession) {
      return res.status(404).json({
        success: false,
        message: "Saga session not found",
      });
    }

    console.log(
      `[SAGA] Continuing workflow for session ${sessionId}, current stage: ${sagaSession.currentStage}`
    );

    // Call Python API to continue workflow
    const pythonResponse = await axios.post(
      `${SAGA_API_BASE_URL}/workflow/continue`,
      {
        session_id: sessionId,
      },
      {
        timeout: 180000, // 3 minutes timeout for next stage generation
      }
    );

    const pythonData = pythonResponse.data;

    console.log(
      "[SAGA DEBUG] Python response:",
      JSON.stringify(pythonData, null, 2)
    );
    console.log("[SAGA DEBUG] Response data type:", typeof pythonData.data);
    console.log(
      "[SAGA DEBUG] Response data keys:",
      pythonData.data ? Object.keys(pythonData.data) : "null"
    );

    // Log faction data specifically
    if (pythonData.data?.factions) {
      console.log(
        "[SAGA DEBUG] Factions array length:",
        pythonData.data.factions.length
      );
      if (pythonData.data.factions.length > 0) {
        console.log(
          "[SAGA DEBUG] First faction keys:",
          Object.keys(pythonData.data.factions[0])
        );
        console.log(
          "[SAGA DEBUG] First faction sample:",
          JSON.stringify(pythonData.data.factions[0], null, 2)
        );
      }
    }

    // Update session with new stage data
    sagaSession.currentStage = pythonData.current_stage;
    sagaSession.awaitingFeedback = pythonData.awaiting_feedback;

    if (pythonData.current_stage === "complete") {
      sagaSession.status = "completed";
    }

    // Update stage-specific data from full_state (which has all accumulated data)
    const fullState = pythonData.data || {};
    console.log("[SAGA DEBUG] Full state keys:", Object.keys(fullState));

    if (fullState.concept) {
      sagaSession.concept = fullState.concept;
      console.log("[SAGA DEBUG] Updated concept");
    }
    if (fullState.world_lore) {
      sagaSession.worldLore = fullState.world_lore;
      console.log(
        "[SAGA DEBUG] Updated world_lore:",
        Object.keys(fullState.world_lore)
      );
    }
    if (fullState.factions) {
      sagaSession.factions = fullState.factions;
      console.log(
        "[SAGA DEBUG] Updated factions, count:",
        fullState.factions?.length
      );
    }
    if (fullState.characters) {
      sagaSession.characters = fullState.characters;
      console.log(
        "[SAGA DEBUG] Updated characters, count:",
        fullState.characters?.length
      );
    }
    if (fullState.plot_arcs) {
      sagaSession.plotArcs = fullState.plot_arcs;
      console.log(
        "[SAGA DEBUG] Updated plot_arcs, count:",
        fullState.plot_arcs?.length
      );
    }
    if (fullState.questlines) {
      sagaSession.questlines = fullState.questlines;
      console.log(
        "[SAGA DEBUG] Updated questlines, count:",
        fullState.questlines?.length
      );
    }

    await sagaSession.save();

    // Update project checkpoint
    const project = await Project.findById(sagaSession.projectId);
    if (project) {
      project.checkpoint = convertStageToCheckpoint(sagaSession.currentStage);
      if (sagaSession.status === "completed") {
        project.status = "completed";
      }
      await project.save();
    }

    console.log(
      `[SAGA] Workflow continued for session ${sessionId}, new stage: ${sagaSession.currentStage}`
    );

    res.status(200).json({
      success: true,
      message: pythonData.message || "Moved to next stage",
      data: {
        sessionId: sagaSession.sessionId,
        currentStage: sagaSession.currentStage,
        awaitingFeedback: sagaSession.awaitingFeedback,
        status: sagaSession.status,
        concept: sagaSession.concept,
        worldLore: sagaSession.worldLore,
        factions: sagaSession.factions,
        characters: sagaSession.characters,
        plotArcs: sagaSession.plotArcs,
        questlines: sagaSession.questlines,
      },
    });
  } catch (error) {
    console.error("[SAGA ERROR] Continue workflow failed:", error.message);

    if (error.response) {
      return res.status(error.response.status || 500).json({
        success: false,
        message:
          error.response.data?.detail ||
          "Failed to continue workflow in Python API",
        error: error.response.data,
      });
    }

    res.status(500).json({
      success: false,
      message: "Failed to continue workflow",
      error: error.message,
    });
  }
};

/**
 * Get current state of a saga session
 */
export const getSessionState = async (req, res) => {
  try {
    const { sessionId } = req.params;

    const sagaSession = await SagaSession.findOne({ sessionId }).populate(
      "projectId"
    );

    if (!sagaSession) {
      return res.status(404).json({
        success: false,
        message: "Saga session not found",
      });
    }

    res.status(200).json({
      success: true,
      data: {
        sessionId: sagaSession.sessionId,
        projectId: sagaSession.projectId,
        topic: sagaSession.topic,
        currentStage: sagaSession.currentStage,
        awaitingFeedback: sagaSession.awaitingFeedback,
        status: sagaSession.status,
        concept: sagaSession.concept,
        worldLore: sagaSession.worldLore,
        factions: sagaSession.factions,
        characters: sagaSession.characters,
        plotArcs: sagaSession.plotArcs,
        questlines: sagaSession.questlines,
        generatedAssets: sagaSession.generatedAssets,
        feedbackHistory: sagaSession.feedbackHistory,
        config: sagaSession.config,
        createdAt: sagaSession.createdAt,
        updatedAt: sagaSession.updatedAt,
      },
    });
  } catch (error) {
    console.error("[SAGA ERROR] Get session state failed:", error.message);
    res.status(500).json({
      success: false,
      message: "Failed to get session state",
      error: error.message,
    });
  }
};

/**
 * Get all saga sessions for a project
 */
export const getProjectSessions = async (req, res) => {
  try {
    const { projectId } = req.params;

    const sessions = await SagaSession.find({ projectId }).sort({
      createdAt: -1,
    });

    res.status(200).json({
      success: true,
      count: sessions.length,
      data: sessions,
    });
  } catch (error) {
    console.error("[SAGA ERROR] Get project sessions failed:", error.message);
    res.status(500).json({
      success: false,
      message: "Failed to get project sessions",
      error: error.message,
    });
  }
};

/**
 * Get all active saga sessions (for dashboard)
 */
export const getAllActiveSessions = async (req, res) => {
  try {
    const sessions = await SagaSession.find({
      status: { $in: ["active", "paused"] },
    })
      .populate("projectId")
      .sort({ updatedAt: -1 })
      .limit(20);

    res.status(200).json({
      success: true,
      count: sessions.length,
      data: sessions,
    });
  } catch (error) {
    console.error("[SAGA ERROR] Get active sessions failed:", error.message);
    res.status(500).json({
      success: false,
      message: "Failed to get active sessions",
      error: error.message,
    });
  }
};

/**
 * Delete a saga session
 */
export const deleteSession = async (req, res) => {
  try {
    const { sessionId } = req.params;

    const sagaSession = await SagaSession.findOneAndDelete({ sessionId });

    if (!sagaSession) {
      return res.status(404).json({
        success: false,
        message: "Saga session not found",
      });
    }

    console.log(`[SAGA] Session ${sessionId} deleted`);

    res.status(200).json({
      success: true,
      message: "Saga session deleted successfully",
    });
  } catch (error) {
    console.error("[SAGA ERROR] Delete session failed:", error.message);
    res.status(500).json({
      success: false,
      message: "Failed to delete session",
      error: error.message,
    });
  }
};
