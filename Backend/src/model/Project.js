import mongoose from "mongoose";

const projectSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
    },
    description: {
      type: String,
      required: true,
    },
    concept: {
      type: String,
      required: true,
    },
    genre: {
      type: String,
      enum: [
        "fantasy",
        "sci-fi",
        "horror",
        "mystery",
        "adventure",
        "rpg",
        "action",
        "other",
      ],
      default: "fantasy",
    },
    status: {
      type: String,
      enum: [
        "concept",
        "world-building",
        "narrative-development",
        "asset-generation",
        "completed",
      ],
      default: "concept",
    },
    checkpoint: {
      type: String,
      enum: [
        "concept",
        "world-lore",
        "factions",
        "characters",
        "plot-arcs",
        "quests",
        "dialogue",
        "render-prep",
      ],
      default: "concept",
    },
    worldData: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "World",
    },
    assets: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Asset",
      },
    ],
    metadata: {
      targetAudience: String,
      estimatedPlayTime: String,
      complexity: {
        type: String,
        enum: ["simple", "moderate", "complex"],
        default: "moderate",
      },
    },
  },
  {
    timestamps: true,
  }
);

export const Project = mongoose.model("Project", projectSchema);
