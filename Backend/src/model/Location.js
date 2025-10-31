import mongoose from "mongoose";

const locationSchema = new mongoose.Schema(
  {
    worldId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "World",
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      enum: [
        "city",
        "village",
        "dungeon",
        "wilderness",
        "landmark",
        "temple",
        "castle",
        "cave",
        "forest",
        "other",
      ],
      required: true,
    },
    geography: {
      terrain: String,
      climate: String,
      size: String,
      coordinates: {
        x: Number,
        y: Number,
      },
    },
    inhabitants: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Character",
      },
    ],
    factionControl: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Faction",
    },
    features: {
      architecture: String,
      notableBuildings: [String],
      naturalFeatures: [String],
      secrets: [String],
    },
    atmosphere: {
      mood: String,
      soundscape: [String],
      lighting: String,
      weather: String,
    },
    connections: [
      {
        locationId: {
          type: mongoose.Schema.Types.ObjectId,
          ref: "Location",
        },
        connectionType: {
          type: String,
          enum: ["road", "path", "portal", "water", "underground", "secret"],
        },
        travelTime: String,
      },
    ],
    visualPrompts: {
      overview: String,
      keyAreas: [String],
      ambientDetails: [String],
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

export const Location = mongoose.model("Location", locationSchema);
