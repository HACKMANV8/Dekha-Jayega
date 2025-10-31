import express from "express";
import {
  initializeWorld,
  createFactions,
  createCharacters,
  createLocations,
  createPlotArcs,
  createQuests,
  getWorldState,
  approveElement,
} from "../controller/sagaController.js";

const router = express.Router({ mergeParams: true });

// SagaAgent narrative workflow endpoints
router.post("/initialize", initializeWorld);
router.post("/factions", createFactions);
router.post("/characters", createCharacters);
router.post("/locations", createLocations);
router.post("/plot-arcs", createPlotArcs);
router.post("/quests", createQuests);

// Get current world state
router.get("/state", getWorldState);

// Human-in-the-loop approval
router.patch("/approve", approveElement);

export default router;
