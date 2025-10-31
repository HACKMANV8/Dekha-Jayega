# ScriptEngine FastAPI Server

A RESTful API server for integrating the ScriptEngine Research and ArcueAgent workflows with frontend applications.

## Features

- ✅ **Research Integration**: Optional research phase before story generation
- ✅ **Human-in-the-Loop**: Interactive feedback at each workflow stage
- ✅ **Session Management**: Multi-session support with unique session IDs
- ✅ **WebSocket Support**: Real-time workflow updates
- ✅ **Stage-by-Stage Control**: Fine-grained control over the creative process
- ✅ **Flexible Configuration**: Customizable model settings, film length, and scene count

## Quick Start

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 2. Set Up Environment

Create a `.env` file with your API keys:

```bash
# API Keys - At least one model provider required
# Priority: OPENAI_API_KEY > GOOGLE_API_KEY
OPENAI_API_KEY=your_openai_api_key      # For GPT-5, GPT-4, etc. (default if provided)
GOOGLE_API_KEY=your_google_api_key      # For Gemini models (fallback)

# Required for research functionality
TAVILY_API_KEY=your_tavily_api_key

# Optional: API server configuration
API_HOST=0.0.0.0
API_PORT=8000

# Optional: Model configuration
# If not specified, auto-selects based on available API keys
MODEL=gpt-5                              # Main model for story generation
SUPERVISOR_MODEL=gpt-5                   # Model for supervisor orchestration
RESEARCH_MODEL=gpt-5                     # Model for research agent
MODEL_TEMPERATURE=0.7
RANDOM_SEED=42

# Supported Models:
# OpenAI: gpt-5, gpt-5-mini, gpt-5-nano, gpt-4, gpt-4-turbo, gpt-4o, gpt-3.5-turbo
# Google: gemini-2.5-pro, gemini-2.5-flash, gemini-1.5-pro, gemini-1.5-flash
```

### 3. Start the Server

```bash
python api_server.py
```

The server will start on `http://localhost:8000` by default.

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Model Configuration

### Supported Models

The API server supports both OpenAI and Google AI models with automatic selection based on available API keys.

#### Priority System
1. **OPENAI_API_KEY** is checked first → defaults to `gpt-5`
2. **GOOGLE_API_KEY** is checked second → defaults to `gemini-2.5-pro`
3. If neither is available, the server will fail with an error

#### Available Models

**OpenAI Models:**
- `gpt-5` (default for OpenAI)
- `gpt-5-mini`
- `gpt-5-nano`
- `gpt-4`
- `gpt-4-turbo`
- `gpt-4o`
- `gpt-3.5-turbo`

**Google Models:**
- `gemini-2.5-pro` (default for Google)
- `gemini-2.5-flash`
- `gemini-1.5-pro`
- `gemini-1.5-flash`

#### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL` | Main model for story generation | Auto-selected based on API keys |
| `SUPERVISOR_MODEL` | Model for supervisor/orchestration | Same as `MODEL` |
| `RESEARCH_MODEL` | Model for research agent | Same as `MODEL` |
| `RESEARCH_EVALUATOR_MODEL` | Model for research evaluation | Same as `RESEARCH_MODEL` |
| `MODEL_TEMPERATURE` | Creativity level (0.0 - 1.0) | `0.5` |
| `RANDOM_SEED` | Random seed for reproducibility | None |

#### Per-Request Model Override

You can override the default model for specific requests:

```json
{
  "topic": "Your story topic",
  "model": "gpt-4-turbo",
  "model_temperature": 0.8,
  "random_seed": 42
}
```

## API Endpoints

### Core Workflow Endpoints

#### `POST /workflow/start`
Start a new workflow with optional research.

**Request Body:**
```json
{
  "topic": "A detective in 1920s Chicago",
  "research_required": "required",
  "research_question": "What was detective work like in 1920s Chicago?",
  "film_length_seconds": 90,
  "number_of_scenes": 12,
  "model": "gpt-5",
  "model_temperature": 0.7,
  "random_seed": 42
}
```

**Response:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "current_stage": "draft",
  "awaiting_feedback": true,
  "data": {
    "draft": "...",
    "title": "Shadows of the Windy City",
    "genre": "Crime Thriller",
    "themes": ["justice", "corruption", "redemption"],
    "tone": "Dark and atmospheric",
    "research": {
      "compressed_research": "...",
      "raw_notes_count": 5
    }
  },
  "message": "Research completed and initial draft generated. Ready for feedback."
}
```

#### `POST /workflow/feedback`
Submit feedback for the current stage to regenerate content.

**Request Body:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "feedback": "Make the protagonist more cynical and add a femme fatale character"
}
```

**Response:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "current_stage": "draft",
  "awaiting_feedback": true,
  "data": {
    "draft": "... (regenerated with feedback) ...",
    "title": "Shadows of the Windy City"
  },
  "message": "Stage draft regenerated with feedback"
}
```

#### `POST /workflow/continue`
Continue to the next workflow stage.

**Request Body:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Response:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "current_stage": "characters",
  "awaiting_feedback": true,
  "data": {
    "characters": [
      {
        "name": "Jack Morrison",
        "role": "Protagonist",
        "persona_type": "male",
        "emotional_tone": "cynical",
        "description": "..."
      }
    ]
  },
  "message": "Moved to stage: characters"
}
```

#### `GET /workflow/state/{session_id}`
Get the current state of a workflow.

**Response:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "current_stage": "characters",
  "awaiting_feedback": true,
  "data": {
    "draft": "...",
    "characters": [...],
    "title": "Shadows of the Windy City"
  },
  "message": "Current workflow state"
}
```

### Research Endpoint

#### `POST /research/execute`
Execute research independently without starting a full workflow.

**Query Parameters:**
- `topic` (required): The research topic
- `research_question` (optional): Specific research question

**Response:**
```json
{
  "session_id": "temp-123e4567",
  "compressed_research": "Historical context about 1920s Chicago detective work...",
  "raw_notes": [
    "Note 1...",
    "Note 2..."
  ],
  "message": "Research completed successfully"
}
```

### Utility Endpoints

#### `DELETE /workflow/{session_id}`
Delete a workflow session.

#### `GET /health`
Health check endpoint.

#### `GET /`
API information and available endpoints.

## Workflow Stages

The workflow progresses through the following stages:

1. **initial** → Starting point
2. **research** → (Optional) Research phase
3. **draft** → Initial story draft
4. **characters** → Character creation
5. **plot** → Plot structure
6. **dialogue** → Dialogue scenes
7. **locations** → Location definitions
8. **visual_lookbook** → Visual style guide
9. **scenes** → Scene generation
10. **complete** → Workflow finished

## WebSocket Support

### Connect to WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/{session_id}');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Update:', data);
};
```

### Send Messages
```javascript
// Get current state
ws.send(JSON.stringify({
  type: 'get_state'
}));

// Submit feedback
ws.send(JSON.stringify({
  type: 'feedback',
  feedback: 'Make it more dramatic'
}));

// Continue to next stage
ws.send(JSON.stringify({
  type: 'continue'
}));
```

## Usage Examples

### Example 1: Story with Research

```python
import requests

# Start workflow with research
response = requests.post('http://localhost:8000/workflow/start', json={
    'topic': 'A cybersecurity expert discovers a conspiracy',
    'research_required': 'required',
    'research_question': 'What are common cybersecurity threats and investigation techniques?',
    'film_length_seconds': 120,
    'number_of_scenes': 15
})

session_id = response.json()['session_id']
print(f"Session started: {session_id}")

# Review draft and provide feedback
feedback_response = requests.post('http://localhost:8000/workflow/feedback', json={
    'session_id': session_id,
    'feedback': 'Add more technical details about hacking'
})

# Continue to characters
continue_response = requests.post('http://localhost:8000/workflow/continue', json={
    'session_id': session_id
})

# Continue through all stages...
for stage in ['characters', 'plot', 'dialogue', 'locations', 'visual_lookbook', 'scenes']:
    # Optionally provide feedback at each stage
    # Then continue
    requests.post('http://localhost:8000/workflow/continue', json={
        'session_id': session_id
    })
```

### Example 2: Story without Research

```python
import requests

# Start workflow without research
response = requests.post('http://localhost:8000/workflow/start', json={
    'topic': 'A robot who wants to be a screenwriter',
    'research_required': 'not_required',
    'film_length_seconds': 90,
    'number_of_scenes': 12
})

session_id = response.json()['session_id']

# Continue through stages without feedback
for i in range(7):  # 7 stages after draft
    requests.post('http://localhost:8000/workflow/continue', json={
        'session_id': session_id
    })

# Get final state
final_state = requests.get(f'http://localhost:8000/workflow/state/{session_id}')
print(final_state.json())
```

### Example 3: Research Only

```python
import requests

# Execute research without starting workflow
response = requests.post('http://localhost:8000/research/execute', params={
    'topic': '1920s Chicago detective work',
    'research_question': 'What were the methods and challenges of detective work in 1920s Chicago?'
})

research_data = response.json()
print(f"Research findings: {research_data['compressed_research']}")
```

## Frontend Integration

See `api_client_example.py` for a complete Python client example.

For JavaScript/TypeScript frontends:

```typescript
// TypeScript example
interface WorkflowStartRequest {
  topic: string;
  research_required: 'required' | 'not_required';
  research_question?: string;
  film_length_seconds?: number;
  number_of_scenes?: number;
}

async function startWorkflow(request: WorkflowStartRequest) {
  const response = await fetch('http://localhost:8000/workflow/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request)
  });
  return await response.json();
}

async function submitFeedback(sessionId: string, feedback: string) {
  const response = await fetch('http://localhost:8000/workflow/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, feedback })
  });
  return await response.json();
}

async function continueWorkflow(sessionId: string) {
  const response = await fetch('http://localhost:8000/workflow/continue', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId })
  });
  return await response.json();
}
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | Server host | `0.0.0.0` |
| `API_PORT` | Server port | `8000` |
| `GOOGLE_API_KEY` | Google Gemini API key | Required |
| `TAVILY_API_KEY` | Tavily search API key | Required for research |
| `SUPERVISOR_MODEL` | Model for supervision | `gemini-2.5-pro` |
| `MODEL_TEMPERATURE` | Default temperature | None |
| `RANDOM_SEED` | Random seed | None |

## Error Handling

The API returns standard HTTP status codes:

- `200` - Success
- `400` - Bad request (invalid input)
- `404` - Session not found
- `500` - Internal server error

Error responses include a detail message:

```json
{
  "detail": "Session 123 not found"
}
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install -e .

EXPOSE 8000

CMD ["python", "api_server.py"]
```

### Production Considerations

1. **Authentication**: Add authentication middleware for production
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Session Persistence**: Use Redis or a database for session storage
4. **CORS**: Configure CORS appropriately for your frontend domain
5. **HTTPS**: Use a reverse proxy (nginx, Caddy) with SSL certificates
6. **Monitoring**: Add logging and monitoring (Prometheus, Grafana)

## Troubleshooting

### Common Issues

**Issue**: "Session not found" error
- **Solution**: Session IDs expire when the server restarts. Store session IDs on the client and handle 404 errors.

**Issue**: Research fails with API errors
- **Solution**: Verify `TAVILY_API_KEY` is set correctly and has remaining credits.

**Issue**: Slow response times
- **Solution**: LLM calls can take time. Consider implementing progress updates via WebSocket.

**Issue**: WebSocket connection drops
- **Solution**: Implement reconnection logic on the client side.

## License

Same as the main ScriptEngine project.

