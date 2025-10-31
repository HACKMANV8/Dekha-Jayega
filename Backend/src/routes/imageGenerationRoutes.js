import express from "express";
import {
  generateImage,
  remixImages,
} from "../controller/imageGenerationController.js";

const router = express.Router();

// Generate image from text prompt
router.post("/generate", generateImage);

// Remix/combine multiple images with prompt
router.post("/remix", remixImages);

export default router;
