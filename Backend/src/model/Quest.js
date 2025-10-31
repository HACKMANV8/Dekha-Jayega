import mongoose from "mongoose";

const questSchema = new mongoose.Schema(
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
      enum: [
        "main",
        "side",
        "fetch",
        "kill",
        "escort",
        "discovery",
        "puzzle",
        "social",
        "crafting",
      ],
      required: true,
    },
    questGiver: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Character",
    },
    objectives: [
      {
        description: String,
        completed: {
          type: Boolean,
          default: false,
        },
        optional: {
          type: Boolean,
          default: false,
        },
      },
    ],
    rewards: {
      experience: Number,
      items: [String],
      reputation: [
        {
          faction: {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Faction",
          },
          change: Number,
        },
      ],
      story: String,
    },
    requirements: {
      level: Number,
      prerequisites: [String],
      items: [String],
    },
    locations: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Location",
      },
    ],
    characters: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Character",
      },
    ],
    plotArc: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "PlotArc",
    },
    dialogue: [
      {
        speaker: {
          type: mongoose.Schema.Types.ObjectId,
          ref: "Character",
        },
        text: String,
        conditions: [String],
        responses: [String],
      },
    ],
    visualElements: {
      cutscenes: [String],
      keyMoments: [String],
      environmentalCues: [String],
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

export const Quest = mongoose.model("Quest", questSchema);
