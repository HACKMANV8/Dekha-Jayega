# Project X - Multi-Agent LangGraph API Documentation

## Overview

Backend API for Project X - A multi-agent LangGraph system for generating game narratives and visual assets for next-gen world engines.

## Base URL

```
http://localhost:5000/api
```

## Architecture Overview

### Supervisor Agent Pattern

- **Supervisor**: Orchestrates the entire pipeline through project management endpoints
- **SagaAgent**: Interactive narrative generation with checkpointing
- **RenderPrepAgent**: Converts narratives to visual asset prompts

### Workflow Checkpoints

1. `concept` - Initial project concept
2. `world-lore` - World building and lore development
3. `factions` - Faction creation and relationships
4. `characters` - Character development and profiles
5. `plot-arcs` - Story structure and plot development
6. `quests` - Quest design and implementation
7. `dialogue` - Character interactions and dialogue
8. `render-prep` - Visual asset preparation

## Endpoints

### 1. Project Management

#### Create Project

```http
POST /projects
Content-Type: application/json

{
  "name": "Epic Fantasy Adventure",
  "description": "A medieval fantasy world with magic and dragons",
  "concept": "Players explore a world where ancient magic is returning",
  "genre": "fantasy",
  "metadata": {
    "targetAudience": "mature",
    "estimatedPlayTime": "50+ hours",
    "complexity": "complex"
  }
}
```

#### Get All Projects

```http
GET /projects
```

#### Get Project by ID

```http
GET /projects/{projectId}
```

#### Update Project Checkpoint

```http
PATCH /projects/{projectId}/checkpoint

{
  "checkpoint": "world-lore",
  "status": "world-building"
}
```

### 2. SagaAgent - Narrative Generation

#### Initialize World

```http
POST /projects/{projectId}/saga/initialize

{
  "name": "Aethermoor",
  "lore": {
    "history": "Ancient civilization fell due to magical catastrophe",
    "mythology": "Dragons are guardians of elemental forces",
    "magicSystem": "Elemental magic tied to emotional states",
    "technology": "Medieval with magical enhancements"
  },
  "geography": {
    "continents": ["Valeria", "Shadowlands"],
    "climateZones": ["temperate", "arctic", "desert"],
    "notableFeatures": ["Floating Islands", "Crystal Caves"]
  },
  "timeline": [
    {
      "era": "Age of Dragons",
      "events": ["Dragons establish territories", "First human settlements"],
      "significance": "Foundation of current world order"
    }
  ]
}
```

#### Create Factions

```http
POST /projects/{projectId}/saga/factions

{
  "factions": [
    {
      "name": "Order of the Crystal",
      "description": "Magical knights protecting ancient artifacts",
      "type": "order",
      "ideology": "Protection through strength",
      "goals": ["Protect magical artifacts", "Maintain world balance"],
      "leadership": {
        "structure": "Council of Elders",
        "leaders": ["Archmage Valdris", "Knight Commander Lyra"]
      },
      "territory": {
        "regions": ["Crystal Valley", "Northern Peaks"],
        "strongholds": ["Crystal Citadel", "Northwatch Tower"]
      }
    }
  ]
}
```

#### Create Characters

```http
POST /projects/{projectId}/saga/characters

{
  "characters": [
    {
      "name": "Lyra Stormwind",
      "description": "A fierce knight commander with mastery over lightning magic",
      "role": "protagonist",
      "background": {
        "race": "Human",
        "class": "Paladin",
        "profession": "Knight Commander",
        "origin": "Crystal Valley",
        "age": 28
      },
      "personality": {
        "traits": ["brave", "determined", "protective"],
        "motivations": ["protect the innocent", "master lightning magic"],
        "fears": ["losing her team", "magical corruption"],
        "quirks": ["always polishes her sword before battle"]
      },
      "appearance": {
        "physicalDescription": "Tall, athletic build with piercing blue eyes and silver hair",
        "clothing": "Crystal-enhanced plate armor with lightning motifs",
        "notableFeatures": ["Lightning-scarred left hand", "Crystal pendant"]
      },
      "abilities": {
        "skills": ["Swordsmanship", "Lightning Magic", "Leadership"],
        "powers": ["Storm Strike", "Lightning Shield", "Thunder Step"],
        "equipment": ["Stormbreaker Sword", "Crystal Armor", "Lightning Rod"]
      }
    }
  ]
}
```

#### Get World State

```http
GET /projects/{projectId}/saga/state
```

#### Approve Narrative Element

```http
PATCH /projects/{projectId}/saga/approve

{
  "elementType": "character",
  "elementId": "character_id_here",
  "approvalStatus": "approved",
  "feedback": "Great character design, approved for render prep"
}
```

### 3. RenderPrepAgent - Visual Asset Generation

#### Generate Character Concepts

```http
POST /projects/{projectId}/renderprep/character-concepts

{
  "characterIds": ["character_id_1", "character_id_2"],
  "stylePreferences": {
    "style": "realistic fantasy art",
    "mood": "heroic",
    "technique": "digital painting"
  }
}
```

#### Generate Environment Prompts

```http
POST /projects/{projectId}/renderprep/environment-prompts

{
  "locationIds": ["location_id_1", "location_id_2"],
  "environmentPreferences": {
    "style": "fantasy landscape",
    "colorPalette": ["mystical blues", "warm golds"]
  }
}
```

#### Generate Keyframe Sequences

```http
POST /projects/{projectId}/renderprep/keyframe-sequences

{
  "plotArcIds": ["plot_arc_id_1"],
  "questIds": ["quest_id_1"],
  "sequencePreferences": {
    "style": "cinematic storyboard",
    "frameDuration": 3
  }
}
```

#### Generate Storyboard (Veo-ready)

```http
POST /projects/{projectId}/renderprep/storyboard

{
  "assetIds": ["keyframe_id_1", "keyframe_id_2", "keyframe_id_3"],
  "storyboardPreferences": {
    "title": "Epic Battle Sequence",
    "transitions": "dynamic cuts with motion blur"
  }
}
```

#### Generate World Data (Genie-ready)

```http
POST /projects/{projectId}/renderprep/world-data

{
  "worldPreferences": {
    "interactivityLevel": "high",
    "proceduralGeneration": true
  }
}
```

### 4. Asset Management

#### Get Assets

```http
GET /projects/{projectId}/assets?type=character-concept&status=completed
```

#### Get Assets by Workflow

```http
GET /projects/{projectId}/assets/workflow?workflow=veo
# workflow options: 'veo', 'genie', 'concept-art'
```

#### Update Asset (after generation)

```http
PUT /projects/{projectId}/assets/{assetId}

{
  "status": "completed",
  "files": [
    {
      "url": "https://cloudinary.com/character_concept_1.jpg",
      "filename": "lyra_concept.jpg",
      "size": 2048000,
      "format": "jpg",
      "cloudinaryId": "character_concepts/lyra_stormwind"
    }
  ],
  "generation": {
    "model": "DALL-E 3",
    "parameters": {
      "style": "realistic fantasy",
      "quality": "hd"
    },
    "seed": 12345,
    "iterations": 1
  }
}
```

#### Approve Asset

```http
PATCH /projects/{projectId}/assets/{assetId}/approve

{
  "approvalStatus": "approved",
  "feedback": "Excellent character design, matches the narrative perfectly"
}
```

## Example Workflow

### 1. Create Project

```javascript
const project = await fetch("/api/projects", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: "Dragon's Legacy",
    description: "Epic fantasy adventure",
    concept: "Ancient dragons return to reclaim their world",
    genre: "fantasy",
  }),
});
```

### 2. Initialize World (SagaAgent)

```javascript
const world = await fetch(`/api/projects/${projectId}/saga/initialize`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: "Drakmoor",
    lore: {
      /* world lore data */
    },
    geography: {
      /* geography data */
    },
  }),
});
```

### 3. Generate Visual Assets (RenderPrepAgent)

```javascript
const characterConcepts = await fetch(
  `/api/projects/${projectId}/renderprep/character-concepts`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      characterIds: ["character_id_1"],
      stylePreferences: { style: "fantasy art" },
    }),
  }
);
```

### 4. Get Veo-Ready Assets

```javascript
const veoAssets = await fetch(
  `/api/projects/${projectId}/assets/workflow?workflow=veo`
);
```

## Response Format

All endpoints return responses in this format:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    /* response data */
  }
}
```

Error responses:

```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error message"
}
```

## Environment Variables

Create a `.env` file in the Backend directory:

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/project-x
NODE_ENV=development
```

## Getting Started

1. Install dependencies:

```bash
cd Backend
npm install
```

2. Add missing CORS dependency:

```bash
npm install cors
```

3. Start the server:

```bash
npm run dev
```

4. Test the health endpoint:

```bash
curl http://localhost:5000/api/health
```

The API is now ready to orchestrate your multi-agent LangGraph workflow for game narrative generation!
