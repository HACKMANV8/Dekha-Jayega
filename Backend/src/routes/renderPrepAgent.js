import express from "express";
import {
  generatePromptsFromSaga,
  generateImageFromAsset,
  getProjectAssets,
  batchGenerateImages,
} from "../controller/renderPrepAgentController.js";

const router = express.Router();

// Generate prompts from saga session using RenderPrepAgent
router.post("/generate-prompts", generatePromptsFromSaga);

// Generate image from a single asset prompt
router.post("/generate-image/:assetId", generateImageFromAsset);

// Batch generate images for multiple assets
router.post("/batch-generate-images", batchGenerateImages);

// Get all assets for a project
router.get("/assets/:projectId", getProjectAssets);

export default router;
