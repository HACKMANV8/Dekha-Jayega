import mongoose from "mongoose";

const assetSchema = new mongoose.Schema(
  {
    projectId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Project",
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      enum: [
        "character-concept",
        "environment",
        "item",
        "creature",
        "keyframe",
        "storyboard",
        "ui-element",
      ],
      required: true,
    },
    category: {
      type: String,
      enum: ["image", "video", "audio", "3d-model", "texture", "animation"],
      required: true,
    },
    sourceEntity: {
      entityType: {
        type: String,
        enum: ["Character", "Location", "Quest", "PlotArc", "Faction", "World"],
      },
      entityId: mongoose.Schema.Types.ObjectId,
    },
    prompts: {
      detailed: String,
      style: String,
      technical: String,
      composition: String,
      lighting: String,
      mood: String,
    },
    metadata: {
      resolution: String,
      aspectRatio: String,
      style: String,
      colorPalette: [String],
      tags: [String],
    },
    generation: {
      model: String,
      parameters: mongoose.Schema.Types.Mixed,
      seed: Number,
      iterations: Number,
    },
    files: [
      {
        url: String,
        filename: String,
        size: Number,
        format: String,
        cloudinaryId: String,
      },
    ],
    videoSequence: {
      isSequence: {
        type: Boolean,
        default: false,
      },
      sequenceOrder: Number,
      duration: Number,
      transitions: String,
    },
    worldGeneration: {
      procedural: Boolean,
      layout: mongoose.Schema.Types.Mixed,
      assetList: [String],
      interactivity: mongoose.Schema.Types.Mixed,
    },
    status: {
      type: String,
      enum: ["pending", "generating", "completed", "failed", "approved"],
      default: "pending",
    },
    approvalStatus: {
      type: String,
      enum: ["pending", "approved", "needs-revision"],
      default: "pending",
    },
  },
  {
    timestamps: true,
  }
);

export const Asset = mongoose.model("Asset", assetSchema);
