import express from "express";
import {
  startSagaWorkflow,
  submitFeedback,
  continueWorkflow,
  getSessionState,
  getProjectSessions,
  getAllActiveSessions,
  deleteSession,
} from "../controller/sagaAgentController.js";

const router = express.Router();

// Start a new saga workflow
router.post("/start", startSagaWorkflow);

// Submit feedback for current stage (human-in-the-loop)
router.post("/feedback", submitFeedback);

// Continue to next stage
router.post("/continue", continueWorkflow);

// Get session state by sessionId
router.get("/session/:sessionId", getSessionState);

// Get all sessions for a project
router.get("/project/:projectId/sessions", getProjectSessions);

// Get all active sessions (for dashboard)
router.get("/active", getAllActiveSessions);

// Delete a session
router.delete("/session/:sessionId", deleteSession);

export default router;
