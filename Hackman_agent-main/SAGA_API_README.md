# SagaEngine API Server

A FastAPI-based REST API server for **SagaAgent**, providing game narrative generation with human-in-the-loop workflows.

## Overview

The SagaEngine API enables frontend applications to integrate with SagaAgent for generating comprehensive game narratives including:

- **Game Concepts** - Core game design documents
- **World Lore** - Rich world-building and setting details
- **Factions** - Organizations, guilds, and political groups
- **Characters** - NPCs, companions, and player characters
- **Plot Arcs** - Main story arcs and narrative structure
- **Questlines** - Mission designs and side quests

## Features

- ✅ **Human-in-the-Loop Workflow** - Pause at each stage for review and feedback
- ✅ **Research Integration** - Optional research agent for grounding narratives
- ✅ **Real-time Updates** - WebSocket support for live progress tracking
- ✅ **Multiple Export Formats** - JSON and Markdown exports
- ✅ **Parallel Execution** - Optional parallel generation for 40-50% speedup
- ✅ **State Management** - Session-based workflow state tracking
- ✅ **Feedback Loop** - Regenerate any stage with user feedback

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file with your API keys:

```bash
# Required: At least one LLM API key
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here

# Optional: Customize server settings
API_PORT=8001
API_HOST=0.0.0.0

# Optional: Model configuration
SUPERVISOR_MODEL=gemini-2.0-flash
MODEL_TEMPERATURE=0.7
```

### Running the Server

```bash
# Start the API server
python saga_api_server.py
```

The server will start on `http://localhost:8001` by default.

### API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## API Endpoints

### Core Workflow Endpoints

#### `POST /workflow/start`
Start a new saga generation workflow.

**Request Body:**
```json
{
  "topic": "A steampunk RPG set in Victorian London",
  "research_required": "not_required",
  "model": "gemini-2.0-flash",
  "model_temperature": 0.7,
  "parallel_execution": false
}
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "current_stage": "concept",
  "awaiting_feedback": true,
  "data": {
    "concept": {
      "title": "Clockwork Chronicles",
      "genre": "Steampunk RPG",
      "elevator_pitch": "...",
      ...
    }
  },
  "message": "Game concept generated. Ready for feedback."
}
```

#### `POST /workflow/feedback`
Submit feedback for the current stage.

**Request Body:**
```json
{
  "session_id": "uuid-here",
  "feedback": "Make the setting darker and grittier"
}
```

#### `POST /workflow/continue`
Continue to the next stage of the workflow.

**Request Body:**
```json
{
  "session_id": "uuid-here"
}
```

#### `GET /workflow/state/{session_id}`
Get the current state of a workflow session.

#### `GET /workflow/{session_id}/export?format=markdown`
Export completed saga results.

**Query Parameters:**
- `format`: `"markdown"` or `"json"` (default: `"markdown"`)

#### `DELETE /workflow/{session_id}`
Delete a workflow session.

### Research Endpoints

#### `POST /research/execute`
Execute research independently without starting a full workflow.

**Query Parameters:**
- `topic`: Research topic
- `research_question`: Optional specific research question

### WebSocket Endpoint

#### `WS /ws/{session_id}`
Real-time workflow updates via WebSocket.

**Message Types:**
- `state_update` - Current state broadcast
- `feedback` - Submit feedback
- `continue` - Move to next stage
- `get_state` - Request current state

## Workflow Stages

The saga generation workflow progresses through these stages:

1. **INITIAL** → **CONCEPT** - Generate game concept document
2. **CONCEPT** → **WORLD_LORE** - Create world-building and lore
3. **WORLD_LORE** → **FACTIONS** - Design factions and organizations
4. **FACTIONS** → **CHARACTERS** - Create characters and NPCs
5. **CHARACTERS** → **PLOT_ARCS** - Structure main story arcs
6. **PLOT_ARCS** → **QUESTLINES** - Design quests and missions
7. **QUESTLINES** → **COMPLETE** - Workflow complete, ready for export

At each stage, the workflow pauses for human review and optional feedback.

## Usage Examples

### Example 1: Basic Workflow (No Research)

```python
import requests

API_BASE = "http://localhost:8001"

# 1. Start workflow
response = requests.post(f"{API_BASE}/workflow/start", json={
    "topic": "A dark fantasy RPG with souls-like combat",
    "research_required": "not_required"
})
session_id = response.json()["session_id"]

# 2. Review concept, submit feedback if needed
requests.post(f"{API_BASE}/workflow/feedback", json={
    "session_id": session_id,
    "feedback": "Add more emphasis on cosmic horror elements"
})

# 3. Continue to next stage
requests.post(f"{API_BASE}/workflow/continue", json={
    "session_id": session_id
})

# 4. Repeat for each stage...

# 5. Export when complete
response = requests.get(f"{API_BASE}/workflow/{session_id}/export?format=markdown")
print(response.json())
```

### Example 2: Workflow with Research

```python
# Start workflow with research
response = requests.post(f"{API_BASE}/workflow/start", json={
    "topic": "A cyberpunk RPG set in Neo-Tokyo",
    "research_required": "required",
    "research_question": "Cyberpunk themes, Neo-Tokyo culture, and transhumanism"
})

# Research is automatically performed and integrated into concept generation
session_id = response.json()["session_id"]
concept = response.json()["data"]["concept"]
research_summary = response.json()["data"]["research"]["compressed_research"]
```

### Example 3: WebSocket Integration

```javascript
const ws = new WebSocket(`ws://localhost:8001/ws/${sessionId}`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'state_update') {
    console.log('Current stage:', data.current_stage);
    console.log('Awaiting feedback:', data.awaiting_feedback);
    console.log('Data:', data.data);
  }
};

// Submit feedback via WebSocket
ws.send(JSON.stringify({
  type: 'feedback',
  feedback: 'Make the characters more diverse'
}));

// Continue to next stage
ws.send(JSON.stringify({
  type: 'continue'
}));
```

## Configuration Options

### Model Configuration

Configure LLM models via environment variables:

```bash
# Explicit supervisor model (used for concept generation with research)
SUPERVISOR_MODEL=gpt-4

# Default model for all stages
MODEL=gemini-2.0-flash

# Model temperature (0.0-1.0)
MODEL_TEMPERATURE=0.7

# Random seed for reproducibility
RANDOM_SEED=42
```

### Parallel Execution

Enable parallel generation for faster processing:

```bash
PARALLEL_EXECUTION=true
PARALLEL_MAX_WORKERS=3
PARALLEL_BATCH_SIZE=4
PARALLEL_RETRY_SEQUENTIAL=true
```

**Note:** Parallel execution requires `auto_continue=true` (no HITL interrupts).

## Advanced Features

### Session Persistence

Sessions are stored in-memory by default. For production:

1. Implement database-backed session storage
2. Use Redis for session caching
3. Configure checkpoint persistence via `CHECKPOINT_DB_PATH`

### Custom Export Paths

Configure export directory:

```bash
EXPORT_DIR=./custom_exports/
```

### Research Agent Integration

The Research Agent can be used to:
- Ground narratives in real-world research
- Provide historical/cultural context
- Research game mechanics and design patterns

```python
# Execute standalone research
response = requests.post(
    f"{API_BASE}/research/execute",
    params={
        "topic": "Norse mythology",
        "research_question": "Norse mythology themes for game design"
    }
)
research = response.json()["compressed_research"]
```

## Integration with Frontend

### React Example

```typescript
import { useState, useEffect } from 'react';

interface WorkflowState {
  sessionId: string;
  currentStage: string;
  awaitingFeedback: boolean;
  data: any;
}

function SagaGenerator() {
  const [state, setState] = useState<WorkflowState | null>(null);
  
  const startWorkflow = async (topic: string) => {
    const response = await fetch('http://localhost:8001/workflow/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, research_required: 'not_required' })
    });
    
    const data = await response.json();
    setState({
      sessionId: data.session_id,
      currentStage: data.current_stage,
      awaitingFeedback: data.awaiting_feedback,
      data: data.data
    });
  };
  
  const submitFeedback = async (feedback: string) => {
    const response = await fetch('http://localhost:8001/workflow/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: state?.sessionId, feedback })
    });
    
    const data = await response.json();
    setState({ ...state, data: data.data });
  };
  
  const continueWorkflow = async () => {
    const response = await fetch('http://localhost:8001/workflow/continue', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: state?.sessionId })
    });
    
    const data = await response.json();
    setState({
      ...state,
      currentStage: data.current_stage,
      awaitingFeedback: data.awaiting_feedback,
      data: data.data
    });
  };
  
  return (
    <div>
      {/* Your UI components here */}
    </div>
  );
}
```

## Troubleshooting

### Common Issues

**Issue: "No API keys found"**
- Ensure you have set either `OPENAI_API_KEY` or `GOOGLE_API_KEY` in your `.env` file

**Issue: "Session not found"**
- Sessions are stored in-memory and are lost on server restart
- Implement persistent session storage for production use

**Issue: Parallel execution fails**
- Ensure `AUTO_CONTINUE=true` when using parallel execution
- Check that all required dependencies are installed

**Issue: UTF-8 encoding errors on Windows**
- The server automatically configures UTF-8 encoding for Windows
- Ensure your terminal supports UTF-8 output

## Production Deployment

### Security Considerations

1. **CORS Configuration**: Update allowed origins in production
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

2. **Authentication**: Add authentication middleware
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Session Management**: Use database-backed session storage

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "saga_api_server.py"]
```

### Environment Variables

```bash
# Production settings
API_HOST=0.0.0.0
API_PORT=8001
OPENAI_API_KEY=your_key_here
SUPERVISOR_MODEL=gpt-4

# Checkpointing
CHECKPOINT_DB_PATH=/data/checkpoints.db

# Export directory
EXPORT_DIR=/data/exports/
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Frontend Client                     │
│            (React, Vue, or any HTTP client)          │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ HTTP/WebSocket
                   │
┌──────────────────▼──────────────────────────────────┐
│              SagaEngine API Server                   │
│                 (FastAPI + Uvicorn)                  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │          SessionManager                      │  │
│  │  - Session storage                          │  │
│  │  - State management                         │  │
│  │  - Model configuration                      │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │         Workflow Orchestration               │  │
│  │  - Stage progression                        │  │
│  │  - Feedback integration                     │  │
│  │  - Export management                        │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐  ┌────────▼────────┐
│ Research Agent │  │   SagaAgent     │
│                │  │                 │
│ - Web search   │  │ - Concept       │
│ - Note taking  │  │ - World Lore    │
│ - Compression  │  │ - Factions      │
└────────────────┘  │ - Characters    │
                    │ - Plot Arcs     │
                    │ - Questlines    │
                    └─────────────────┘
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review the SagaAgent documentation

---

**Version**: 1.0.0  
**Last Updated**: October 2025


