import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import { connectDB } from "./lib/db.js";

// Import routes
import projectRoutes from "./routes/projectRoutes.js";
import sagaRoutes from "./routes/sagaRoutes.js";
import renderPrepRoutes from "./routes/renderPrepRoutes.js";
import assetRoutes from "./routes/assetRoutes.js";

// Import middleware
import {
  errorHandler,
  notFound,
  logger,
  responseTimeLogger,
} from "./middleware/index.js";

const app = express();

// Load environment variables
dotenv.config();

// Middleware
app.use(cors());
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true, limit: "10mb" }));
app.use(logger);
app.use(responseTimeLogger);

// Health check endpoint
app.get("/api/health", (req, res) => {
  res.status(200).json({
    success: true,
    message: "Project X API is running",
    timestamp: new Date().toISOString(),
  });
});

// API Routes
app.use("/api/projects", projectRoutes);
app.use("/api/projects/:projectId/saga", sagaRoutes);
app.use("/api/projects/:projectId/renderprep", renderPrepRoutes);
app.use("/api/projects/:projectId/assets", assetRoutes);

// Error handling middleware
app.use(notFound);
app.use(errorHandler);

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`🚀 Project X API Server is running on port ${PORT}`);
  console.log(`📋 Health check: http://localhost:${PORT}/api/health`);
  connectDB();
});
