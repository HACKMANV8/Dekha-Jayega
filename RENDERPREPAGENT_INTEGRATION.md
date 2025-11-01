# RenderPrepAgent Integration - Complete Guide

## Overview

Successfully integrated RenderPrepAgent with the full stack application, enabling transformation of Saga narrative data into optimized image generation prompts and direct integration with Nano Banana for image generation.

## Architecture

```
Frontend (React)
    ↓
Backend API (Node.js/Express)
    ↓
RenderPrepAgent (Python)
    ↓
Nano Banana (Python Image Generation)
    ↓
MongoDB (Asset Storage)
```

## Components Created/Modified

### 1. Backend Controller: `renderPrepAgentController.js`

**Location:** `Backend/src/controller/renderPrepAgentController.js`

**Functions:**

- `generatePromptsFromSaga(req, res)` - Main function that:

  - Fetches saga session data from MongoDB
  - Creates temporary JSON file with saga data
  - Spawns Python process to run RenderPrepAgent
  - Parses exported prompts (characters, environments, items, storyboards)
  - Stores all prompts as Asset documents in MongoDB
  - Returns asset IDs and prompt data to frontend

- `generateImageFromAsset(req, res)` - Generates single image:

  - Fetches asset by ID
  - Extracts detailed prompt
  - Spawns Nano Banana Python process
  - Updates asset with generated image URL
  - Returns image data

- `batchGenerateImages(req, res)` - Batch image generation:

  - Accepts array of asset IDs
  - Generates images for all assets sequentially
  - Returns success/failure results for each

- `getProjectAssets(req, res)` - Fetches all assets for a project
  - Supports filtering by type and status

**Key Paths:**

```javascript
PYTHON_VENV_PATH: "../../../Hackman_agent-main/.venv/Scripts/python.exe";
RENDER_PREP_SCRIPT: "../../../Hackman_agent-main/run_render_prep.py";
NANO_BANANA_PYTHON: "../../../Nano banana/nano-banana-python/.venv/Scripts/python.exe";
NANO_BANANA_SCRIPT: "../../../Nano banana/nano-banana-python/src/generate_single_image.py";
```

### 2. Python Wrapper: `run_render_prep.py`

**Location:** `Hackman_agent-main/run_render_prep.py`

**Purpose:** Bridge between Node.js backend and RenderPrepAgent

**Features:**

- Accepts saga data JSON file path as argument
- Quality preset selection (draft, standard, high, cinematic)
- Optional image generation flag
- Exports prompts to JSON files
- Returns structured JSON output to stdout
- Error handling with proper exit codes

**Usage:**

```bash
python run_render_prep.py <saga_data_path> --quality standard --generate-images
```

### 3. Backend Routes: `renderPrepAgent.js`

**Location:** `Backend/src/routes/renderPrepAgent.js`

**Endpoints:**

- `POST /api/render-prep/generate-prompts` - Generate prompts from saga
- `POST /api/render-prep/generate-image/:assetId` - Generate single image
- `POST /api/render-prep/batch-generate-images` - Batch generate images
- `GET /api/render-prep/assets/:projectId` - Get project assets

### 4. Frontend: `RenderPrepAgent.jsx`

**Location:** `Frontend/src/pages/RenderPrepAgent.jsx`

**Features:**

#### Tab 1: Prompt Preview

- Lists all completed saga sessions
- Session selection dropdown
- Quality preset selector (draft/standard/high/cinematic)
- "Generate Prompts" button
- Session details display (topic, stage, character count, faction count)
- Error handling with visual feedback

#### Tab 2: Image Generation

- Grid display of all generated prompts
- Asset cards showing:
  - Type badge (character/environment/prop/storyboard)
  - Prompt preview with expand/collapse
  - Generate button (individual)
  - Download button (after generation)
  - Status indicator (pending/completed)
- "Generate All Images" batch button
- Real-time status updates

#### Tab 3 & 4: Video Storyboarding & World Layout

- Placeholder tabs for future features

**Key Functions:**

```javascript
fetchSagaSessions() - Load completed saga sessions
generatePrompts() - Call RenderPrepAgent via backend
generateSingleImage(assetId) - Generate one image
generateAllImages() - Batch generate all images
```

### 5. Database Model Updates

**SagaSession Model Enhancement:**

```javascript
renderPrepCompleted: Boolean
renderPrepAssets: [ObjectId ref 'Asset']
```

**Asset Model Fields Used:**

```javascript
{
  projectId: ObjectId,
  name: String,
  type: String, // 'character-concept' | 'environment' | 'prop' | 'storyboard'
  category: 'image',
  prompts: {
    detailed: String,
    style: String,
    technical: String
  },
  metadata: {
    resolution: String,
    aspectRatio: String,
    style: String,
    tags: [String],
    sourceData: Object
  },
  status: String, // 'pending' | 'completed' | 'failed'
  url: String, // Generated image URL
  generatedAt: Date
}
```

## Data Flow

### Step 1: Generate Prompts

```
User selects saga session + quality preset
  ↓
Frontend POST /api/render-prep/generate-prompts
  ↓
Backend fetches saga data from MongoDB
  ↓
Backend writes temp JSON file
  ↓
Backend spawns: python run_render_prep.py saga_data.json --quality standard
  ↓
RenderPrepAgent processes saga data through 5 nodes:
  - character_prompts
  - environment_prompts
  - item_prompts
  - storyboard_prompts
  ↓
RenderPrepAgent exports JSON files to exports/render_prep/
  ↓
Backend reads exported JSON files
  ↓
Backend creates Asset documents for each prompt
  ↓
Backend returns asset list to frontend
  ↓
Frontend displays asset cards in Image Generation tab
```

### Step 2: Generate Images

```
User clicks "Generate All Images" or individual "Generate" button
  ↓
Frontend POST /api/render-prep/generate-image/:assetId (or batch endpoint)
  ↓
Backend fetches asset prompt from MongoDB
  ↓
Backend spawns: python generate_single_image.py --prompt "..."
  ↓
Nano Banana generates image
  ↓
Backend receives image URL/data via stdout
  ↓
Backend updates Asset with url and status='completed'
  ↓
Backend returns image data to frontend
  ↓
Frontend updates UI to show generated image
```

## Prompt Types Generated

### 1. Character Prompts

- Full character description
- Visual appearance details
- Style tags
- Technical requirements (resolution, aspect ratio)
- Stored as type: "character-concept"

### 2. Environment Prompts

- Location/setting descriptions
- Atmosphere and lighting
- Geographic features
- Stored as type: "environment"

### 3. Item Prompts

- Item/prop descriptions
- Material and texture details
- Usage context
- Stored as type: "prop"

### 4. Storyboard Prompts

- Scene compositions
- Camera angles
- Action sequences
- Stored as type: "storyboard"

## Quality Presets

- **Draft**: Basic prompts, fast generation
- **Standard**: Balanced quality and detail (default)
- **High**: Enhanced details and specifications
- **Cinematic**: Maximum quality with cinematic descriptions

## Error Handling

### Backend

- Saga session validation
- Python process error capture
- JSON parse error handling
- File system error handling
- Asset status tracking (pending/completed/failed)

### Frontend

- Network error handling
- Loading states for all async operations
- Error message display with AlertCircle icon
- Disabled states during processing
- Graceful fallbacks for missing data

## Installation Steps

### 1. Install Python Dependencies

```bash
cd Hackman_agent-main
pip install -r requirements.txt
```

### 2. Install Nano Banana

```bash
cd "Nano banana/nano-banana-python"
pip install -r requirements.txt
```

### 3. Backend Setup

No additional dependencies needed - uses existing Express setup

### 4. Frontend Setup

No additional dependencies needed - uses existing React setup

## Usage Guide

### 1. Complete a Saga

- Go to Agents page
- Create and complete a saga workflow
- Ensure saga reaches "completed" status

### 2. Generate Prompts

- Navigate to RenderPrepAgent page
- Select completed saga from dropdown
- Choose quality preset
- Click "Generate Prompts"
- Wait for processing (status shown in button)

### 3. Generate Images

- Automatically switches to Image Generation tab
- View all generated prompts as cards
- Options:
  - Click "Generate All Images" for batch processing
  - Click individual "Generate" buttons for selective generation
- View generated images in cards
- Download images using Download button

### 4. Monitor Progress

- Loading spinners show active processes
- Status badges show completion state
- Error messages display if issues occur

## API Endpoints Reference

### Generate Prompts

```http
POST /api/render-prep/generate-prompts
Content-Type: application/json

{
  "sessionId": "mongo_session_id",
  "qualityPreset": "standard",
  "generateImages": false
}

Response:
{
  "success": true,
  "message": "Prompts generated successfully",
  "data": {
    "sessionId": "...",
    "prompts": {...},
    "assets": [...],
    "totalPrompts": 12
  }
}
```

### Generate Single Image

```http
POST /api/render-prep/generate-image/:assetId

Response:
{
  "success": true,
  "message": "Image generated successfully",
  "data": {
    "assetId": "...",
    "imageUrl": "...",
    "name": "Character Name",
    "type": "character-concept"
  }
}
```

### Batch Generate Images

```http
POST /api/render-prep/batch-generate-images
Content-Type: application/json

{
  "assetIds": ["id1", "id2", "id3"]
}

Response:
{
  "success": true,
  "message": "Batch generation completed",
  "data": {
    "successful": [...],
    "failed": [...],
    "totalProcessed": 10,
    "successCount": 8,
    "errorCount": 2
  }
}
```

### Get Project Assets

```http
GET /api/render-prep/assets/:projectId?type=character-concept&status=completed

Response:
{
  "success": true,
  "data": [...],
  "count": 5
}
```

## File Structure

```
Dekha-Jayega/
├── Backend/
│   └── src/
│       ├── controller/
│       │   └── renderPrepAgentController.js ✨ NEW
│       ├── routes/
│       │   └── renderPrepAgent.js ✨ NEW
│       ├── model/
│       │   └── SagaSession.js (updated)
│       └── index.js (updated)
├── Frontend/
│   └── src/
│       └── pages/
│           └── RenderPrepAgent.jsx ✨ UPDATED
└── Hackman_agent-main/
    └── run_render_prep.py ✨ NEW
```

## Testing Checklist

- [ ] Backend server starts without errors
- [ ] Saga sessions load in dropdown
- [ ] Prompt generation completes successfully
- [ ] Assets stored in MongoDB
- [ ] Individual image generation works
- [ ] Batch image generation works
- [ ] Images display in UI
- [ ] Download button works
- [ ] Error states display correctly
- [ ] Loading states work properly

## Troubleshooting

### Python Process Fails

- Check Python venv paths in controller
- Verify RenderPrepAgent dependencies installed
- Check temp file write permissions
- Review stderr output in backend logs

### Images Not Generating

- Verify Nano Banana setup
- Check Python script paths
- Ensure GPU/CPU resources available
- Review Nano Banana logs

### Assets Not Saving

- Check MongoDB connection
- Verify Asset model schema
- Check projectId references
- Review backend error logs

## Future Enhancements

1. **Video Storyboarding Tab**

   - Sequence planning
   - Animation timelines
   - Scene transitions

2. **World Layout Tab**

   - Map generation
   - Location relationships
   - Navigation flows

3. **Prompt Editing**

   - In-app prompt refinement
   - Style transfer options
   - Prompt templates

4. **Asset Management**

   - Asset library
   - Version control
   - Batch operations

5. **Queue System**
   - Background job processing
   - Progress tracking
   - Notification system

## Notes

- RenderPrepAgent processes saga data synchronously
- Image generation is sequential (can be parallelized in future)
- Temporary JSON files are cleaned up after processing
- Assets are linked to both project and saga session
- All prompts stored in MongoDB for persistence
- Frontend state updates in real-time during generation

---

**Integration Status:** ✅ COMPLETE
**Last Updated:** 2024
**Version:** 1.0.0
