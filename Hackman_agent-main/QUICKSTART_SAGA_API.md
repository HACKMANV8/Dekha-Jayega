# SagaEngine API - Quick Start Guide

Get started with the SagaEngine API in 5 minutes! 🚀

## Prerequisites

- Python 3.10 or higher
- OpenAI API key OR Google API key
- Git (to clone the repository)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Copy the example configuration:

```bash
cp config.saga.example .env
```

Edit `.env` and add your API key:

```bash
# At minimum, set ONE of these:
OPENAI_API_KEY=sk-your-openai-key-here
# OR
GOOGLE_API_KEY=your-google-api-key-here
```

## Running the Server

### Start the API Server

```bash
python saga_api_server.py
```

You should see:

```
[START] Starting SagaEngine API Server
   Host: 0.0.0.0
   Port: 8001

📚 API Documentation:
   Swagger UI: http://0.0.0.0:8001/docs
   ReDoc: http://0.0.0.0:8001/redoc
```

### Test the Server

Open your browser to: http://localhost:8001/docs

You'll see the interactive API documentation (Swagger UI).

## Your First Request

### Using cURL

```bash
curl -X POST "http://localhost:8001/workflow/start" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "A dark fantasy RPG with Norse mythology",
    "research_required": "not_required"
  }'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8001/workflow/start",
    json={
        "topic": "A dark fantasy RPG with Norse mythology",
        "research_required": "not_required"
    }
)

data = response.json()
print(f"Session ID: {data['session_id']}")
print(f"Current Stage: {data['current_stage']}")
print(f"Concept: {data['data']['concept']['title']}")
```

### Using JavaScript/Fetch

```javascript
fetch('http://localhost:8001/workflow/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    topic: 'A dark fantasy RPG with Norse mythology',
    research_required: 'not_required'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Session ID:', data.session_id);
  console.log('Current Stage:', data.current_stage);
  console.log('Concept:', data.data.concept);
});
```

## Complete Workflow Example

Here's a complete workflow from start to finish:

```python
import requests

API_BASE = "http://localhost:8001"

# 1. Start the workflow
print("1. Starting workflow...")
response = requests.post(f"{API_BASE}/workflow/start", json={
    "topic": "A cyberpunk RPG in Neo-Tokyo 2099"
})
session_id = response.json()["session_id"]
print(f"   ✓ Session created: {session_id}")

# 2. Review the concept
concept = response.json()["data"]["concept"]
print(f"\n2. Generated Concept:")
print(f"   Title: {concept['title']}")
print(f"   Genre: {concept['genre']}")
print(f"   Pitch: {concept['elevator_pitch']}")

# 3. Submit feedback (optional)
print("\n3. Submitting feedback...")
requests.post(f"{API_BASE}/workflow/feedback", json={
    "session_id": session_id,
    "feedback": "Add more cyberpunk noir atmosphere"
})
print("   ✓ Feedback submitted")

# 4. Continue through stages
stages = ["world_lore", "factions", "characters", "plot_arcs", "questlines"]

for stage in stages:
    print(f"\n4. Continuing to {stage}...")
    response = requests.post(f"{API_BASE}/workflow/continue", json={
        "session_id": session_id
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Stage: {data['current_stage']}")
        
        if data["current_stage"] == "complete":
            print("\n🎉 Workflow complete!")
            break

# 5. Export results
print("\n5. Exporting results...")
response = requests.get(f"{API_BASE}/workflow/{session_id}/export?format=markdown")
if response.status_code == 200:
    files = response.json()["files"]
    print(f"   ✓ Exported {len(files)} files")
    for file in files:
        print(f"      - {file}")

print("\n✅ All done!")
```

## Run the Test Suite

We've included a comprehensive test suite:

```bash
python test_saga_api.py
```

This will:
- ✅ Check server health
- ✅ Test basic workflow
- ✅ Test feedback submission
- ✅ Test stage progression
- ✅ Test session management

## Common Options

### With Research Integration

```json
{
  "topic": "A medieval RPG",
  "research_required": "required",
  "research_question": "Medieval warfare, castle sieges, and feudal systems"
}
```

### With Parallel Execution (Faster!)

```json
{
  "topic": "A space exploration RPG",
  "research_required": "not_required",
  "parallel_execution": true,
  "parallel_max_workers": 3
}
```

**Note**: Parallel execution only works with `AUTO_CONTINUE=true` in `.env` (no human feedback).

### With Custom Model

```json
{
  "topic": "A post-apocalyptic RPG",
  "research_required": "not_required",
  "model": "gpt-4",
  "model_temperature": 0.8
}
```

## API Endpoints Cheat Sheet

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/workflow/start` | POST | Start new saga workflow |
| `/workflow/continue` | POST | Move to next stage |
| `/workflow/feedback` | POST | Submit feedback for current stage |
| `/workflow/state/{id}` | GET | Get current workflow state |
| `/workflow/{id}/export` | GET | Export completed saga |
| `/workflow/{id}` | DELETE | Delete workflow session |
| `/research/execute` | POST | Execute standalone research |
| `/health` | GET | Check server health |
| `/ws/{id}` | WS | WebSocket for real-time updates |

## Troubleshooting

### Server Won't Start

**Error**: "No API keys found"

**Solution**: Add at least one API key to your `.env` file:
```bash
OPENAI_API_KEY=sk-your-key-here
# OR
GOOGLE_API_KEY=your-key-here
```

### Port Already in Use

**Error**: "Address already in use"

**Solution**: Change the port in `.env`:
```bash
API_PORT=8002  # Use a different port
```

### Module Not Found

**Error**: "ModuleNotFoundError: No module named 'X'"

**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Connection Refused

**Error**: "Connection refused"

**Solution**: Make sure the server is running:
```bash
python saga_api_server.py
```

## Next Steps

1. **Read the Full Documentation**: See [SAGA_API_README.md](SAGA_API_README.md)
2. **Compare APIs**: See [COMPARISON_ARCUE_VS_SAGA.md](COMPARISON_ARCUE_VS_SAGA.md)
3. **Deploy with Docker**: See [Dockerfile.saga](Dockerfile.saga)
4. **Integrate with Frontend**: Check the React examples in the full README

## Example Use Cases

### 🎮 RPG Quest Generator

```python
response = requests.post(f"{API_BASE}/workflow/start", json={
    "topic": "Generate side quests for a fantasy RPG",
    "research_required": "not_required"
})
```

### 🌍 World Building Tool

```python
response = requests.post(f"{API_BASE}/workflow/start", json={
    "topic": "Create a rich sci-fi universe with multiple factions",
    "research_required": "required",
    "research_question": "Space colonization, terraforming, and interstellar politics"
})
```

### 👥 Character Creation Suite

```python
response = requests.post(f"{API_BASE}/workflow/start", json={
    "topic": "Design diverse NPCs and companions for an open-world RPG",
    "research_required": "not_required"
})
```

## Getting Help

- **Documentation**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **Test Script**: `python test_saga_api.py`
- **Issues**: Open an issue on GitHub

## What's Next?

Once you're comfortable with the basics:

1. **Explore WebSocket Integration** for real-time updates
2. **Enable Parallel Execution** for faster generation
3. **Integrate Research Agent** for grounded narratives
4. **Deploy to Production** with Docker
5. **Build a Frontend** with React/Vue/Svelte

Happy saga building! 🎮✨

---

**Questions?** Check out [SAGA_API_README.md](SAGA_API_README.md) for detailed documentation.


