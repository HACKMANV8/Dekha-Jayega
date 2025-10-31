import express from "express";
import {
  getAssets,
  getAssetById,
  updateAsset,
  uploadAssetFiles,
  deleteAsset,
  approveAsset,
  getAssetsByWorkflow,
  createCustomAsset,
} from "../controller/assetController.js";

const router = express.Router({ mergeParams: true });

// Asset management endpoints
router.get("/", getAssets);
router.post("/", createCustomAsset);
router.get("/workflow", getAssetsByWorkflow);
router.get("/:assetId", getAssetById);
router.put("/:assetId", updateAsset);
router.patch("/:assetId/upload", uploadAssetFiles);
router.patch("/:assetId/approve", approveAsset);
router.delete("/:assetId", deleteAsset);

export default router;
