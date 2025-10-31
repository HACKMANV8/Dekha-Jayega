import express from "express";
import {
  createProject,
  getAllProjects,
  getProjectById,
  updateProject,
  updateCheckpoint,
  deleteProject,
} from "../controller/projectController.js";

const router = express.Router();

// Project CRUD operations
router.post("/", createProject);
router.get("/", getAllProjects);
router.get("/:projectId", getProjectById);
router.put("/:projectId", updateProject);
router.patch("/:projectId/checkpoint", updateCheckpoint);
router.delete("/:projectId", deleteProject);

export default router;
