# Dekha-Jayega Multi-Agent Integration

## Complete Integration Summary

This document outlines the complete integration of the Hackman_agent-main multi-agent system with the Dekha-Jayega backend and frontend.

## ✅ Completed Backend Integration

### 1. MongoDB Models Created

- **SagaSession.js** - Comprehensive model for tracking saga workflow state
  - Stores sessionId, projectId, topic, currentStage, status
  - All agent outputs: concept, worldLore, factions, characters, plotArcs, questlines
  - Feedback history, generated assets, configuration
  - Location: `Backend/src/model/SagaSession.js`

### 2. API Controllers Created

- **sagaAgentController.js** - Bridge between Node.js and Python FastAPI

  - `startSagaWorkflow()` - Initializes saga generation with Python API
  - `submitFeedback()` - Human-in-the-loop feedback submission
  - `continueWorkflow()` - Progress to next narrative stage
  - `getSessionState()` - Retrieve current session data
  - `getProjectSessions()` - Get all sessions for a project
  - `getAllActiveSessions()` - Dashboard active sessions
  - Location: `Backend/src/controller/sagaAgentController.js`

- **sagaImageController.js** - Auto-generate images from saga narratives
  - `generateSagaImages()` - Batch generate images for characters/factions/environments
  - `generateSingleImage()` - Single image generation
  - `autoGenerateStageImages()` - Automatic generation after each stage
  - Integrates with existing Python image generation bridge
  - Location: `Backend/src/controller/sagaImageController.js`

### 3. API Routes Created

- **sagaAgentRoutes.js** - REST endpoints for saga workflow

  ```
  POST   /api/saga-agent/start              - Start new saga workflow
  POST   /api/saga-agent/feedback           - Submit feedback for regeneration
  POST   /api/saga-agent/continue           - Continue to next stage
  GET    /api/saga-agent/session/:sessionId - Get session state
  GET    /api/saga-agent/project/:projectId/sessions - Get project sessions
  GET    /api/saga-agent/active             - Get all active sessions
  DELETE /api/saga-agent/session/:sessionId - Delete session
  ```

  - Location: `Backend/src/routes/sagaAgentRoutes.js`

- **imageGenerationRoutes.js** - Enhanced with saga image generation
  ```
  POST /api/image-generation/single     - Generate single image
  POST /api/image-generation/saga       - Generate images for saga session
  POST /api/image-generation/saga/auto  - Auto-generate for stage
  ```

### 4. Dependencies Added

- `axios@^1.7.9` - HTTP client for Python API communication
- `uuid@^11.0.4` - Session ID generation
- Updated in: `Backend/package.json`

### 5. Environment Configuration

Required in `Backend/.env`:

```bash
# MongoDB
MONGODB_URI=your_mongodb_connection_string

# Python Saga API Server
SAGA_API_URL=http://localhost:8001

# Google Gemini API (for image generation)
GEMINI_API_KEY=your_gemini_api_key
```

## 🔄 Frontend Integration (In Progress)

### Components to Update

#### 1. Agents.jsx - SagaAgent Workflow Interface

**Status**: Needs to be recreated (file was corrupted during edit)

**Required Features**:

- Topic input screen to start saga generation
- Step-by-step wizard with progress stepper (6 stages)
- Real-time content display for each stage
- Human-in-the-loop controls:
  - ✅ Approve & Continue button
  - 🔄 Regenerate with Feedback
  - ✏️ Enable Edit mode
- Loading states with spinner
- Error handling with user-friendly messages
- API Integration:
  - `POST /api/projects` - Create project
  - `POST /api/saga-agent/start` - Start workflow
  - `POST /api/saga-agent/continue` - Next stage
  - `POST /api/saga-agent/feedback` - Submit feedback
  - `POST /api/image-generation/saga/auto` - Auto-generate images

**File Location**: `Frontend/src/pages/Agents.jsx`

#### 2. Dashboard.jsx - Real Project Status

**Updates Needed**:

- Replace mock data with API calls
- Fetch active saga sessions: `GET /api/saga-agent/active`
- Display current stage and awaiting feedback status
- Add "Continue Project" button that loads existing session
- Show recent activity from MongoDB timestamps

**File Location**: `Frontend/src/pages/Dashboard.jsx`

#### 3. New: SagaWorkspace.jsx - Visualization Page

**Features Needed**:

- Fetch session data: `GET /api/saga-agent/session/:sessionId`
- Display concept card with all details
- World lore tabs (History, Geography, Magic, Culture)
- Faction cards with generated emblems
- Character profiles with AI-generated portraits
- Plot arc timeline visualization
- Questline tree structure
- Generated assets gallery

**File Location**: `Frontend/src/pages/SagaWorkspace.jsx` (to be created)

## 🐍 Python Saga API Integration

### Python Server Location

- Path: `Hackman_agent-main/saga_api_server.py`
- Port: 8001 (configured via `API_PORT` env var)
- FastAPI with WebSocket support

### Starting the Python Server

```bash
cd "Hackman_agent-main"
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python saga_api_server.py
```

### Required Environment Variables (Python)

Create `Hackman_agent-main/.env`:

```bash
# At least one LLM API key required
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here

# Optional: Server configuration
API_PORT=8001
API_HOST=0.0.0.0

# Optional: Model configuration
SUPERVISOR_MODEL=gemini-2.0-flash-exp
MODEL_TEMPERATURE=0.7
```

### Python API Endpoints Used

```
POST /workflow/start      - Start saga generation
POST /workflow/feedback   - Submit feedback for regeneration
POST /workflow/continue   - Move to next stage
GET  /workflow/state      - Get current state
```

## 🔧 Setup Instructions

### Step 1: Install Backend Dependencies

```bash
cd Backend
npm install
```

### Step 2: Install Frontend Dependencies

```bash
cd Frontend
npm install
```

### Step 3: Setup Python Environment

```bash
cd "Hackman_agent-main"
pip install fastapi uvicorn python-dotenv langchain-google-genai langchain-openai
```

### Step 4: Configure Environment Variables

1. Backend `.env` - Add `SAGA_API_URL=http://localhost:8001`
2. Python `.env` - Add your `GOOGLE_API_KEY` or `OPENAI_API_KEY`
3. Nano banana Python `.env` - Add `GEMINI_API_KEY` for image generation

### Step 5: Start All Servers

Terminal 1 - Python Saga API:

```bash
cd "Hackman_agent-main"
python saga_api_server.py
```

Terminal 2 - Node.js Backend:

```bash
cd Backend
npm run dev
```

Terminal 3 - React Frontend:

```bash
cd Frontend
npm run dev
```

## 📊 Data Flow Architecture

```
Frontend (React)
    ↓ HTTP POST /api/saga-agent/start
Node.js Backend (Express)
    ↓ HTTP POST to localhost:8001/workflow/start
Python FastAPI (SagaAgent)
    ↓ LangChain Agents
Google Gemini / OpenAI
    ↓ Generated Narrative
Python FastAPI Response
    ↓ JSON Response
Node.js Backend
    ↓ Save to MongoDB (SagaSession)
    ↓ JSON Response
Frontend (Display to User)
```

## 🎨 Image Generation Flow

```
Saga Stage Complete (e.g., Characters)
    ↓ Automatic Trigger
POST /api/image-generation/saga/auto
    ↓ Extract character.visual_prompt or character.appearance
Node.js spawns Python subprocess
    ↓ Python: generate_single_image.py
Google Gemini Image Generation API
    ↓ Base64 Image
Store in SagaSession.generatedAssets
    ↓ Display in Frontend
```

## 🚀 Next Steps

### Immediate Tasks

1. **Fix Agents.jsx** - Recreate the frontend workflow interface (corrupted file)
2. **Test Python API** - Ensure saga_api_server.py runs correctly
3. **Update Dashboard** - Connect to real MongoDB data
4. **Create SagaWorkspace** - Build visualization page

### Testing Checklist

- [ ] Start Python saga_api_server.py successfully
- [ ] Backend connects to Python API
- [ ] MongoDB stores saga sessions
- [ ] Frontend topic input works
- [ ] Saga generation progresses through all stages
- [ ] Feedback/regeneration works
- [ ] Image generation triggers automatically
- [ ] Generated assets display correctly
- [ ] Dashboard shows active sessions
- [ ] Complete workflow end-to-end

## 📝 API Examples

### Start Saga Workflow

```bash
curl -X POST http://localhost:4000/api/saga-agent/start \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "674d123abc456def789",
    "topic": "A steampunk detective RPG in Victorian London",
    "researchRequired": false,
    "model": "gemini-2.0-flash-exp"
  }'
```

### Submit Feedback

```bash
curl -X POST http://localhost:4000/api/saga-agent/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "abc-123-def-456",
    "feedback": "Make the protagonist more mysterious and add steampunk gadgets"
  }'
```

### Continue Workflow

```bash
curl -X POST http://localhost:4000/api/saga-agent/continue \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "abc-123-def-456"}'
```

### Generate Images for Session

```bash
curl -X POST http://localhost:4000/api/image-generation/saga \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "abc-123-def-456",
    "assetTypes": ["characters", "environments", "factions"]
  }'
```

## 🔍 Troubleshooting

### Python API Not Starting

- Check if port 8001 is available
- Verify API keys in `.env`
- Install missing dependencies: `pip install -r requirements.txt`

### Backend Connection Failed

- Ensure `SAGA_API_URL=http://localhost:8001` in Backend/.env
- Check Python server is running
- Verify no CORS issues

### MongoDB Connection Issues

- Check `MONGODB_URI` in Backend/.env
- Ensure MongoDB Atlas IP whitelist includes your IP
- Test connection with mongoose

### Image Generation Fails

- Verify `GEMINI_API_KEY` in Nano banana/.env
- Check Python venv path in `sagaImageController.js`
- Ensure `generate_single_image.py` exists and is executable

## 📁 File Structure Summary

```
Dekha-Jayega/
├── Backend/
│   ├── src/
│   │   ├── model/
│   │   │   ├── SagaSession.js ✅ NEW
│   │   │   └── index.js ✅ UPDATED
│   │   ├── controller/
│   │   │   ├── sagaAgentController.js ✅ NEW
│   │   │   ├── sagaImageController.js ✅ NEW
│   │   │   └── imageGenerationController.js
│   │   ├── routes/
│   │   │   ├── sagaAgentRoutes.js ✅ NEW
│   │   │   └── imageGenerationRoutes.js ✅ UPDATED
│   │   └── index.js ✅ UPDATED (mounted saga routes)
│   ├── package.json ✅ UPDATED (axios, uuid)
│   └── .env (needs SAGA_API_URL)
├── Frontend/
│   ├── src/
│   │   └── pages/
│   │       ├── Agents.jsx ⚠️ NEEDS FIX
│   │       ├── Dashboard.jsx 🔄 TO UPDATE
│   │       └── SagaWorkspace.jsx 📝 TO CREATE
│   └── package.json
├── Hackman_agent-main/
│   ├── saga_api_server.py (Python FastAPI)
│   ├── SagaAgent/ (Multi-agent system)
│   ├── requirements.txt
│   └── .env (needs API keys)
└── Nano banana/
    └── nano-banana-python/
        ├── src/generate_single_image.py
        └── .env (needs GEMINI_API_KEY)
```

## 🎯 Integration Complete Percentage: ~70%

### Completed ✅

- Backend MongoDB models
- Backend API controllers
- Backend API routes
- Image generation integration
- Python-Node.js bridge architecture
- Dependencies installed

### In Progress 🔄

- Frontend Agents.jsx workflow interface

### To Do 📝

- SagaWorkspace visualization page
- Dashboard real data integration
- End-to-end testing
- Error handling improvements
- Documentation for users

---

**Last Updated**: Integration work in progress
**Status**: Backend complete, Frontend partial
**Next Action**: Fix Agents.jsx frontend interface
