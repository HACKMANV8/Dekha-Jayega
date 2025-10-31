import mongoose from "mongoose";

const characterSchema = new mongoose.Schema(
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
    role: {
      type: String,
      enum: [
        "protagonist",
        "antagonist",
        "supporting",
        "npc",
        "quest-giver",
        "merchant",
        "guard",
        "other",
      ],
      required: true,
    },
    background: {
      race: String,
      class: String,
      profession: String,
      origin: String,
      age: Number,
    },
    personality: {
      traits: [String],
      motivations: [String],
      fears: [String],
      quirks: [String],
    },
    appearance: {
      physicalDescription: String,
      clothing: String,
      notableFeatures: [String],
    },
    abilities: {
      skills: [String],
      powers: [String],
      equipment: [String],
    },
    relationships: [
      {
        characterId: {
          type: mongoose.Schema.Types.ObjectId,
          ref: "Character",
        },
        relationship: String,
        description: String,
      },
    ],
    factionId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Faction",
    },
    dialogue: [
      {
        context: String,
        lines: [String],
        mood: String,
      },
    ],
    visualPrompts: {
      conceptArt: String,
      characterSheet: String,
      emotionalStates: [String],
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

export const Character = mongoose.model("Character", characterSchema);
