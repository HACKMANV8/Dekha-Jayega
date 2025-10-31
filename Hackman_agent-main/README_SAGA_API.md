# SagaEngine API Server 🎮

> AI-powered game narrative generation with human-in-the-loop workflows

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## What is SagaEngine API?

SagaEngine API is a REST API server that integrates **SagaAgent** - an AI-powered game narrative generator - with any frontend application. It enables you to generate comprehensive game narratives including concepts, world lore, factions, characters, plot arcs, and questlines through an easy-to-use HTTP interface.

### Key Features

- 🎮 **Complete Game Narrative Pipeline** - From concept to questlines
- 🔄 **Human-in-the-Loop Workflow** - Review and provide feedback at each stage
- 🔍 **Research Integration** - Optional research agent for grounded narratives
- ⚡ **Parallel Execution** - 40-50% faster generation
- 📤 **Multiple Export Formats** - JSON and Markdown
- 🔌 **WebSocket Support** - Real-time updates
- 🐳 **Docker Ready** - Easy deployment
- 📚 **Comprehensive Documentation** - Everything you need to get started

## Quick Links

| Document | Description |
|----------|-------------|
| [Quick Start Guide](QUICKSTART_SAGA_API.md) | Get started in 5 minutes |
| [Full API Documentation](SAGA_API_README.md) | Complete reference and examples |
| [Comparison: ArcueAgent vs SagaAgent](COMPARISON_ARCUE_VS_SAGA.md) | Choose the right API for your needs |
| [Delivery Summary](SAGA_API_DELIVERY_SUMMARY.md) | Implementation details and features |

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Configure

```bash
cp config.saga.example .env
# Edit .env and add your API key (OpenAI or Google)
```

### 3. Run

```bash
python saga_api_server.py
```

### 4. Test

Visit http://localhost:8001/docs for interactive API documentation.

Or make your first request:

```bash
curl -X POST "http://localhost:8001/workflow/start" \
  -H "Content-Type: application/json" \
  -d '{"topic": "A dark fantasy RPG with Norse mythology", "research_required": "not_required"}'
```

## Workflow Overview

```
Topic → Concept → World Lore → Factions → Characters → Plot Arcs → Questlines → Export
         ↓          ↓            ↓          ↓            ↓            ↓
      Review     Review       Review     Review       Review       Review
      Feedback   Feedback     Feedback   Feedback     Feedback     Feedback
```

## What Gets Generated?

| Stage | Output |
|-------|--------|
| **Concept** | Game title, genre, elevator pitch, core loop, mechanics, USP |
| **World Lore** | Setting, geography, history, cultures, magic/tech systems |
| **Factions** | Organizations with leaders, territories, relationships |
| **Characters** | NPCs with personalities, backstories, abilities, relationships |
| **Plot Arcs** | 3-act story structures with branching paths |
| **Questlines** | Missions with objectives, choices, and rewards |

## Example Output

### Input

```json
{
  "topic": "A steampunk RPG in Victorian London"
}
```

### Generated Concept

```json
{
  "title": "Clockwork Chronicles",
  "genre": "Steampunk RPG",
  "elevator_pitch": "Navigate the smog-filled streets of Victorian London where steam-powered machines and ancient magic collide...",
  "core_loop": "Explore districts, solve mysteries, customize gear, make moral choices",
  "key_mechanics": "Gear crafting, faction reputation, detective investigations, airship travel"
}
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/workflow/start` | POST | Start new saga generation |
| `/workflow/continue` | POST | Move to next stage |
| `/workflow/feedback` | POST | Submit feedback |
| `/workflow/state/{id}` | GET | Get current state |
| `/workflow/{id}/export` | GET | Export results |
| `/research/execute` | POST | Standalone research |
| `/health` | GET | Health check |

See [Full API Documentation](SAGA_API_README.md) for details.

## Integration Examples

### Python

```python
import requests

response = requests.post("http://localhost:8001/workflow/start", json={
    "topic": "A cyberpunk RPG in Neo-Tokyo"
})

session_id = response.json()["session_id"]
concept = response.json()["data"]["concept"]
```

### JavaScript

```javascript
fetch('http://localhost:8001/workflow/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ topic: 'A space exploration RPG' })
})
.then(res => res.json())
.then(data => console.log(data.data.concept));
```

### React

```typescript
const { data } = await axios.post('http://localhost:8001/workflow/start', {
  topic: 'A post-apocalyptic survival RPG'
});

setSessionId(data.session_id);
setConcept(data.data.concept);
```

## Deployment

### Docker

```bash
docker-compose -f docker-compose.saga.yml up -d
```

### Manual

```bash
export API_PORT=8001
export OPENAI_API_KEY=your-key
python saga_api_server.py
```

See [Deployment Guide](SAGA_API_README.md#production-deployment) for production setup.

## Use Cases

### 🎮 Game Development
- Rapid prototyping of game narratives
- Quest design and mission creation
- NPC and character generation
- World-building and lore creation

### 📝 Content Creation
- Game design documents
- Campaign sourcebooks for tabletop RPGs
- Interactive fiction and story games
- Narrative design templates

### 🧪 Research & Experimentation
- Narrative AI research
- Procedural content generation
- Game design pattern exploration
- Interactive storytelling

## Architecture

```
Frontend (React/Vue/etc)
    ↓ HTTP/WebSocket
SagaEngine API (FastAPI)
    ↓ 
┌──────────────┬──────────────┐
│  Research    │  SagaAgent   │
│  Agent       │              │
│  - Search    │  - Concept   │
│  - Research  │  - Lore      │
│  - Compress  │  - Factions  │
└──────────────┤  - Characters│
               │  - Plots     │
               │  - Quests    │
               └──────────────┘
```

## Features Comparison

| Feature | SagaAgent API | ArcueAgent API |
|---------|--------------|----------------|
| Purpose | Game Narratives | Screenplays |
| Stages | 6 | 6 |
| Parallel Execution | ✅ Yes | ❌ No |
| Output Type | Game Design Docs | Scripts |
| Default Port | 8001 | 8000 |

See [Full Comparison](COMPARISON_ARCUE_VS_SAGA.md)

## Documentation

- **[Quick Start Guide](QUICKSTART_SAGA_API.md)** - Get up and running in 5 minutes
- **[Full API Documentation](SAGA_API_README.md)** - Complete reference with examples
- **[API Comparison](COMPARISON_ARCUE_VS_SAGA.md)** - SagaAgent vs ArcueAgent
- **[Delivery Summary](SAGA_API_DELIVERY_SUMMARY.md)** - Technical implementation details
- **[Interactive Docs](http://localhost:8001/docs)** - Swagger UI (when server is running)

## Configuration

Key environment variables:

```bash
# Required: At least one API key
OPENAI_API_KEY=sk-your-key
GOOGLE_API_KEY=your-key

# Optional
API_PORT=8001
MODEL=gemini-2.0-flash
MODEL_TEMPERATURE=0.7
PARALLEL_EXECUTION=true
```

See [config.saga.example](config.saga.example) for all options.

## Testing

```bash
# Run test suite
python test_saga_api.py

# Manual testing
curl http://localhost:8001/health
```

## Performance

- **Sequential Execution**: ~5-10 minutes for complete saga
- **Parallel Execution**: ~3-5 minutes (40-50% faster)
- **Research Integration**: +2-3 minutes
- **Per-Stage**: ~30-60 seconds each

## Requirements

- Python 3.10+
- OpenAI API key OR Google API key
- 2GB RAM minimum
- Internet connection (for LLM APIs)

## Roadmap

- [ ] Database persistence (PostgreSQL/MongoDB)
- [ ] User authentication (JWT)
- [ ] Rate limiting
- [ ] Batch processing
- [ ] Advanced caching (Redis)
- [ ] Metrics and analytics
- [ ] Multi-tenancy support
- [ ] Game engine integrations (Unity/Unreal)

## Troubleshooting

**Server won't start?**  
→ Check [Troubleshooting Guide](SAGA_API_README.md#troubleshooting)

**Need help?**  
→ See [Quick Start Guide](QUICKSTART_SAGA_API.md)

**Want more features?**  
→ Check [Full Documentation](SAGA_API_README.md)

## Contributing

Contributions welcome! See the main repository for contribution guidelines.

## License

See LICENSE file for details.

## Support

- 📖 Documentation: [SAGA_API_README.md](SAGA_API_README.md)
- 🚀 Quick Start: [QUICKSTART_SAGA_API.md](QUICKSTART_SAGA_API.md)
- 💬 Issues: Open an issue on GitHub
- 🌐 API Docs: http://localhost:8001/docs

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [LangChain](https://www.langchain.com/) - LLM framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation

---

**Ready to build amazing game narratives?**  
Start with the [Quick Start Guide](QUICKSTART_SAGA_API.md) →

**Have questions?**  
Check the [Full Documentation](SAGA_API_README.md) →

**Want to see it in action?**  
Run `python test_saga_api.py` →

---

<div align="center">

**SagaEngine API** - Empowering Game Creators with AI 🎮✨

[Quick Start](QUICKSTART_SAGA_API.md) · [Documentation](SAGA_API_README.md) · [Comparison](COMPARISON_ARCUE_VS_SAGA.md)

</div>


