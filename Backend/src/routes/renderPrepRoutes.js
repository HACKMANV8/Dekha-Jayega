import express from "express";
import {
  generateCharacterConcepts,
  generateEnvironmentPrompts,
  generateKeyframeSequences,
  generateStoryboard,
  generateWorldData,
  getRenderPrepStatus,
} from "../controller/renderPrepController.js";

const router = express.Router({ mergeParams: true });

// RenderPrepAgent visual asset generation endpoints
router.post("/character-concepts", generateCharacterConcepts);
router.post("/environment-prompts", generateEnvironmentPrompts);
router.post("/keyframe-sequences", generateKeyframeSequences);
router.post("/storyboard", generateStoryboard);
router.post("/world-data", generateWorldData);

// Get render preparation status
router.get("/status", getRenderPrepStatus);

export default router;
