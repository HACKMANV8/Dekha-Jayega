import mongoose from "mongoose";

const plotArcSchema = new mongoose.Schema(
  {
    worldId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "World",
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      enum: ["main", "side", "character", "faction", "world"],
      required: true,
    },
    acts: [
      {
        actNumber: Number,
        title: String,
        description: String,
        keyEvents: [String],
        characters: [
          {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Character",
          },
        ],
        locations: [
          {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Location",
          },
        ],
      },
    ],
    themes: [String],
    conflicts: [
      {
        type: String,
        description: String,
        resolution: String,
      },
    ],
    prerequisites: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "PlotArc",
      },
    ],
    consequences: [String],
    quests: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Quest",
      },
    ],
    visualSequences: [
      {
        sceneDescription: String,
        keyFrames: [String],
        cinematicNotes: String,
      },
    ],
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

export const PlotArc = mongoose.model("PlotArc", plotArcSchema);
