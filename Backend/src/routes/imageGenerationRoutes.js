import express from "express";
import {
  generateImage,
  remixImages,
} from "../controller/imageGenerationController.js";
import {
  generateSagaImages,
  generateSingleImage,
  autoGenerateStageImages,
} from "../controller/sagaImageController.js";

const router = express.Router();

// Generate image from text prompt (original)
router.post("/generate", generateImage);

// Generate single image (new, uses same Python script)
router.post("/single", generateSingleImage);

// Remix/combine multiple images with prompt
router.post("/remix", remixImages);

// Generate images for an entire saga session
router.post("/saga", generateSagaImages);

// Auto-generate images for a specific saga stage
router.post("/saga/auto", autoGenerateStageImages);

export default router;
