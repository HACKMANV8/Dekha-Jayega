import mongoose from "mongoose";

const worldSchema = new mongoose.Schema(
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
    lore: {
      history: String,
      mythology: String,
      cosmology: String,
      magicSystem: String,
      technology: String,
      cultures: [String],
    },
    geography: {
      continents: [String],
      climateZones: [String],
      notableFeatures: [String],
    },
    timeline: [
      {
        era: String,
        events: [String],
        significance: String,
      },
    ],
    factions: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Faction",
      },
    ],
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
    plotArcs: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "PlotArc",
      },
    ],
    quests: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Quest",
      },
    ],
    researchSources: [String],
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

export const World = mongoose.model("World", worldSchema);
