import mongoose from "mongoose";

const factionSchema = new mongoose.Schema(
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
        "kingdom",
        "guild",
        "cult",
        "tribe",
        "organization",
        "alliance",
        "empire",
        "other",
      ],
      required: true,
    },
    ideology: String,
    goals: [String],
    leadership: {
      structure: String,
      leaders: [String],
    },
    territory: {
      regions: [String],
      strongholds: [String],
    },
    relationships: [
      {
        factionId: {
          type: mongoose.Schema.Types.ObjectId,
          ref: "Faction",
        },
        relationship: {
          type: String,
          enum: ["allied", "neutral", "rival", "enemy", "unknown"],
        },
        description: String,
      },
    ],
    resources: {
      military: String,
      economic: String,
      magical: String,
      political: String,
    },
    members: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Character",
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

export const Faction = mongoose.model("Faction", factionSchema);
