import mongoose from "mongoose";

const sagaSessionSchema = new mongoose.Schema(
  {
    sessionId: {
      type: String,
      required: true,
      unique: true,
      index: true,
    },
    projectId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Project",
      required: true,
    },
    topic: {
      type: String,
      required: true,
    },
    currentStage: {
      type: String,
      enum: [
        "initial",
        "research",
        "concept",
        "world_lore",
        "factions",
        "characters",
        "plot_arcs",
        "questlines",
        "complete",
      ],
      default: "initial",
    },
    awaitingFeedback: {
      type: Boolean,
      default: false,
    },
    status: {
      type: String,
      enum: ["active", "paused", "completed", "error"],
      default: "active",
    },
    // Research data
    researchRequired: {
      type: Boolean,
      default: false,
    },
    researchQuestion: {
      type: String,
    },
    compressedResearch: {
      type: String,
    },
    rawNotes: [String],
    // Concept stage
    concept: {
      title: String,
      genre: String,
      elevator_pitch: String,
      core_loop: String,
      key_mechanics: String,
      progression: String,
      world_setting: String,
      art_style: String,
      target_audience: String,
      monetization: String,
      usp: String,
    },
    // World Lore stage
    worldLore: {
      world_name: String,
      setting: String,
      history: String,
      geography: String,
      magic_system: String,
      technology: String,
      culture: String,
      social_structures: String,
      economy: String,
      conflicts: String,
      lore_hooks: String,
    },
    // Factions stage
    factions: [
      {
        name: String,
        faction_type: String,
        philosophy: String,
        goals: String,
        structure: String,
        members: String,
        resources: String,
        influence: String,
        history: String,
        relationships: String,
        quests: String,
        visual_identity: String,
        lore_ties: String,
      },
    ],
    // Characters stage
    characters: [
      {
        name: String,
        archetype: String,
        background: String,
        personality: String,
        appearance: String,
        role: String,
        motivations: String,
        relationships: String,
        class_abilities: String,
        arc: String,
        dialogue_style: String,
        visual_prompt: String,
      },
    ],
    // Plot Arcs stage
    plotArcs: [mongoose.Schema.Types.Mixed],
    // Questlines stage
    questlines: [mongoose.Schema.Types.Mixed],
    // Feedback tracking
    feedbackHistory: [
      {
        stage: String,
        feedback: String,
        timestamp: Date,
      },
    ],
    // Generated assets (images)
    generatedAssets: [
      {
        assetType: {
          type: String,
          enum: ["character", "environment", "item", "storyboard"],
        },
        name: String,
        prompt: String,
        imageUrl: String,
        model: String,
        aspectRatio: String,
        createdAt: Date,
      },
    ],
    // RenderPrep integration
    renderPrepCompleted: {
      type: Boolean,
      default: false,
    },
    renderPrepAssets: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Asset",
      },
    ],
    // Configuration
    config: {
      model: String,
      model_temperature: Number,
      random_seed: Number,
      parallel_execution: Boolean,
      parallel_max_workers: Number,
    },
    // Metadata
    error: {
      message: String,
      stage: String,
      timestamp: Date,
    },
  },
  {
    timestamps: true,
  }
);

// Index for faster queries
sagaSessionSchema.index({ projectId: 1, status: 1 });
sagaSessionSchema.index({ createdAt: -1 });

export const SagaSession = mongoose.model("SagaSession", sagaSessionSchema);
