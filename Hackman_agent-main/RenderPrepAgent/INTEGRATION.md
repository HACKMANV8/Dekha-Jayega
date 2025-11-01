# RenderPrepAgent Integration Guide

Complete guide for integrating RenderPrepAgent with Saga and Orchestrator agents.

---

## Overview

RenderPrepAgent seamlessly integrates with the existing YakLZ ecosystem:

```
Research Agent → Saga Agent → Orchestrator Agent → RenderPrep Agent
                                                          ↓
                                                   Image Prompts
                                                          ↓
                                                   Nano Banana API
                                                          ↓
                                                   Final Images
```

---

## Integration Patterns

### Pattern 1: CLI Pipeline (Recommended for Manual Workflows)

Sequential command-line execution:

```bash
# Step 1: Research (optional)
python -m Research.run_research --query "Cyberpunk RPG mechanics"

# Step 2: Generate Saga
export AUTO_CONTINUE=true
export TOPIC="Neon Shadows: A Cyberpunk Detective Story"
python -m SagaAgent.agent

# Step 3: Generate Image Prompts
python -m RenderPrepAgent.agent ./saga_exports/ --quality premium

# Step 4: (Optional) Generate Images
export NANO_BANANA_API_KEY="your_key"
python -m RenderPrepAgent.agent ./saga_exports/ --generate-images
```

### Pattern 2: Orchestrator Integration (Automated Workflow)

Extend the Orchestrator to automatically trigger RenderPrep:

**Step 1:** Create Orchestrator extension:

```python
# OrchestratorAgent/extensions/render_integration.py

from RenderPrepAgent.agent import run_render_prep, load_saga_data
from RenderPrepAgent.config import AgentConfig


def trigger_render_prep(saga_export_path: str, quality: str = "standard"):
    """Trigger RenderPrepAgent after saga completion."""
    print("\n[ORCHESTRATOR] Triggering RenderPrepAgent...")
    
    # Load saga data
    saga_data = load_saga_data(saga_export_path)
    
    # Configure render agent
    render_config = AgentConfig(
        quality_preset=quality,
        generate_images=False,
        auto_continue=True
    )
    
    # Run render prep
    result = run_render_prep(saga_data, render_config)
    
    print(f"[ORCHESTRATOR] RenderPrep complete: {len(result['character_prompts'])} character prompts generated")
    
    return result
```

**Step 2:** Add to Orchestrator workflow:

```python
# In orchestrator_saga.py or orchestrator.py

from OrchestratorAgent.extensions.render_integration import trigger_render_prep

# After saga completion
if saga_complete:
    export_path = saga_result.get("export_path")
    render_result = trigger_render_prep(export_path, quality="premium")
    
    # Store render results in orchestrator state
    state["render_prompts"] = render_result
```

### Pattern 3: API Integration (For Web Services)

Use the saga_api_server to expose RenderPrep as an API endpoint:

**Step 1:** Add RenderPrep endpoint to `saga_api_server.py`:

```python
from fastapi import FastAPI, HTTPException
from RenderPrepAgent.agent import run_render_prep
from RenderPrepAgent.config import AgentConfig

@app.post("/api/render-prep")
async def generate_render_prompts(
    saga_data: dict,
    quality: str = "standard",
    generate_images: bool = False
):
    """Generate image prompts from saga data."""
    try:
        config = AgentConfig(
            quality_preset=quality,
            generate_images=generate_images,
            auto_continue=True
        )
        
        result = run_render_prep(saga_data, config)
        
        return {
            "success": True,
            "character_prompts": result.get("character_prompts", []),
            "environment_prompts": result.get("environment_prompts", []),
            "item_prompts": result.get("item_prompts", []),
            "storyboard_prompts": result.get("storyboard_prompts", []),
            "export_path": result.get("export_path")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Step 2:** Call from client:

```python
import httpx

# Generate saga first
saga_response = httpx.post("http://localhost:8000/api/saga/generate", json={
    "topic": "My Game Idea",
    "auto_continue": True
})
saga_data = saga_response.json()

# Generate render prompts
render_response = httpx.post("http://localhost:8000/api/render-prep", json={
    "saga_data": saga_data,
    "quality": "premium",
    "generate_images": False
})
prompts = render_response.json()

print(f"Generated {len(prompts['character_prompts'])} character prompts")
```

### Pattern 4: Programmatic Integration

Direct Python integration for custom workflows:

```python
from SagaAgent.agent import saga_agent
from RenderPrepAgent.agent import run_render_prep
from RenderPrepAgent.config import AgentConfig

# Step 1: Generate saga
saga_config = {"configurable": {"thread_id": "my_saga"}}
saga_inputs = {"topic": "Epic Fantasy Adventure", "messages": []}
saga_state = saga_agent.invoke(saga_inputs, config=saga_config)

# Step 2: Generate render prompts
render_config = AgentConfig(
    quality_preset="premium",
    generate_images=False
)
render_state = run_render_prep(saga_state, render_config)

# Step 3: Use the prompts
for char_prompt in render_state['character_prompts']:
    print(f"Character: {char_prompt['name']}")
    print(f"Prompt: {char_prompt['positive_prompt']}")
    
    # Send to image generation service
    # image = your_image_generator.generate(char_prompt['positive_prompt'])
```

---

## Data Flow

### Input: Saga Agent Output

RenderPrepAgent expects this structure:

```json
{
  "concept": {
    "title": "Game Title",
    "art_style": "fantasy | realistic | anime | cyberpunk | etc.",
    "genre": "RPG | Strategy | etc."
  },
  "world_lore": {
    "world_name": "World Name",
    "geography": "Description of the world",
    "setting_overview": "Overview text"
  },
  "characters": [
    {
      "character_name": "Character Name",
      "character_type": "Protagonist | Companion | NPC | Villain",
      "appearance": "Visual description",
      "silhouette_design": "Pose description",
      "visual_themes": "Color palette",
      "personality_traits": "Personality",
      "combat_style": "Combat description"
    }
  ],
  "factions": [
    {
      "faction_name": "Faction Name",
      "headquarters": "HQ description",
      "aesthetic_identity": "Visual style"
    }
  ],
  "plot_arcs": [
    {
      "arc_title": "Arc Name",
      "act1_hook": "Opening scene",
      "midpoint_twist": "Midpoint scene",
      "climax_sequence": "Climax scene",
      "epilogue": "Ending scene"
    }
  ]
}
```

### Output: Render Prompts

RenderPrepAgent generates:

```json
{
  "character_prompts": [
    {
      "id": "character_id",
      "name": "Character Name",
      "type": "Character Type",
      "positive_prompt": "Optimized prompt text with ((emphasis))",
      "negative_prompt": "Elements to avoid",
      "original_description": "Source text",
      "metadata": {...}
    }
  ],
  "environment_prompts": [...],
  "item_prompts": [...],
  "storyboard_prompts": [...],
  "export_path": "./saga_exports/renders/",
  "json_files": ["file1.json", ...],
  "markdown_files": ["file1.md", ...]
}
```

---

## Configuration

### Environment Variables

Add to your `.env` file:

```bash
# === RENDERPREPAGENT CONFIGURATION ===

# Export settings
RENDER_EXPORT_DIR=./saga_exports/renders/
RENDER_CHECKPOINT_DB=./saga_exports/render_checkpoints.db

# Quality settings
RENDER_QUALITY=standard  # draft | standard | premium
RENDER_IMAGE_SIZE=1024x1024
RENDER_NUM_IMAGES=1
RENDER_USE_WEIGHTING=true
RENDER_MAX_PROMPT_LENGTH=500

# Nano Banana API (optional - for image generation)
NANO_BANANA_API_KEY=your_api_key_here
NANO_BANANA_ENDPOINT=https://api.google.com/nano-banana/v1

# Model settings
RENDER_MODEL=gemini-2.0-flash-exp
RENDER_TEMPERATURE=0.7
```

### Python Configuration

```python
from RenderPrepAgent.config import AgentConfig, RenderConfig

# Customize configuration
config = AgentConfig(
    thread_id="custom_thread",
    quality_preset="premium",
    generate_images=False,
    model_name="gemini-2.0-flash-exp",
    model_temperature=0.7
)

# Access render config
quality_preset = RenderConfig.get_quality_preset("premium")
print(quality_preset)
# {"technical_details": "8K, ultra detailed, ...", "emphasis_weight": 1.3}
```

---

## Extending RenderPrepAgent

### Custom Prompt Engineering

Add your own prompt builders:

```python
# RenderPrepAgent/services/custom_prompts.py

from RenderPrepAgent.services.prompt_engineering_service import PromptEngineeringService

class CustomPromptService(PromptEngineeringService):
    
    @classmethod
    def build_vehicle_prompt(
        cls,
        vehicle_name: str,
        vehicle_type: str,
        description: str,
        art_style: str,
        quality_preset: dict
    ) -> dict:
        """Build prompt for vehicles/mounts."""
        # Implement custom logic
        return {
            "positive_prompt": "...",
            "negative_prompt": "..."
        }
```

### Custom Image Generation Service

Support additional APIs:

```python
# RenderPrepAgent/services/stable_diffusion_service.py

class StableDiffusionService:
    """Integration with Stable Diffusion API."""
    
    async def generate_image(self, positive_prompt: str, negative_prompt: str):
        # Implement Stable Diffusion API calls
        pass
```

### Custom Export Formats

Add new export formats:

```python
# RenderPrepAgent/services/export_service.py

class RenderExportService:
    
    @staticmethod
    def export_prompts_csv(prompts: List[Dict], prompt_type: str, state: dict) -> str:
        """Export prompts to CSV format."""
        import csv
        
        filename = f"{export_dir}{title}_{prompt_type}_prompts_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'positive_prompt', 'negative_prompt'])
            writer.writeheader()
            writer.writerows(prompts)
        
        return filename
```

---

## Testing Integration

### Unit Tests

```python
# tests/test_render_integration.py

import unittest
from RenderPrepAgent.agent import run_render_prep
from RenderPrepAgent.config import AgentConfig

class TestRenderIntegration(unittest.TestCase):
    
    def test_saga_to_render(self):
        """Test complete saga to render pipeline."""
        saga_data = {
            "concept": {"title": "Test", "art_style": "fantasy"},
            "characters": [{"character_name": "Test", "appearance": "Test desc"}]
        }
        
        config = AgentConfig(quality_preset="draft")
        result = run_render_prep(saga_data, config)
        
        self.assertGreater(len(result['character_prompts']), 0)
        self.assertIn('positive_prompt', result['character_prompts'][0])
```

### Integration Tests

```bash
# tests/integration/test_full_pipeline.sh

#!/bin/bash

# Full pipeline test
echo "Testing full pipeline..."

# Generate saga
python -m SagaAgent.agent --topic "Test Game" --auto-continue

# Generate renders
python -m RenderPrepAgent.agent ./saga_exports/ --quality draft

# Check outputs exist
if [ -d "./saga_exports/renders/" ]; then
    echo "✓ Integration test passed"
else
    echo "✗ Integration test failed"
    exit 1
fi
```

---

## Performance Optimization

### Parallel Processing

For large sagas, process categories in parallel:

```python
from concurrent.futures import ThreadPoolExecutor
from RenderPrepAgent.nodes import (
    generate_character_prompts_node,
    generate_environment_prompts_node
)

with ThreadPoolExecutor(max_workers=4) as executor:
    char_future = executor.submit(generate_character_prompts_node, state)
    env_future = executor.submit(generate_environment_prompts_node, state)
    
    char_result = char_future.result()
    env_result = env_future.result()
```

### Caching

Cache generated prompts to avoid regeneration:

```python
import hashlib
import json
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_prompt_generation(character_json: str) -> str:
    """Cache prompt generation results."""
    character = json.loads(character_json)
    # Generate prompt
    return prompt
```

---

## Deployment

### Docker Integration

Add RenderPrep to docker-compose:

```yaml
# docker-compose.yml

services:
  saga-agent:
    # ... existing config
  
  render-prep-agent:
    build:
      context: .
      dockerfile: Dockerfile.render
    environment:
      - RENDER_EXPORT_DIR=/exports/renders/
      - RENDER_QUALITY=standard
      - NANO_BANANA_API_KEY=${NANO_BANANA_API_KEY}
    volumes:
      - ./saga_exports:/exports
    depends_on:
      - saga-agent
```

### Kubernetes Deployment

```yaml
# k8s/render-prep-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: render-prep-agent
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: render-prep
        image: yaklz/render-prep-agent:latest
        env:
        - name: RENDER_QUALITY
          value: "standard"
        - name: NANO_BANANA_API_KEY
          valueFrom:
            secretKeyRef:
              name: render-secrets
              key: api-key
```

---

## Best Practices

### 1. Error Handling

```python
try:
    result = run_render_prep(saga_data, config)
except FileNotFoundError:
    print("Saga data not found. Run Saga Agent first.")
except Exception as e:
    print(f"RenderPrep failed: {e}")
    # Fallback or retry logic
```

### 2. Validation

```python
def validate_saga_data(saga_data: dict) -> bool:
    """Validate saga data before render prep."""
    required_keys = ["concept", "characters"]
    
    for key in required_keys:
        if key not in saga_data:
            print(f"Warning: Missing {key} in saga data")
            return False
    
    if not saga_data["characters"]:
        print("Warning: No characters found")
        return False
    
    return True

# Use validation
if validate_saga_data(saga_data):
    result = run_render_prep(saga_data, config)
```

### 3. Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RenderPrep")

logger.info("Starting render prep workflow")
result = run_render_prep(saga_data, config)
logger.info(f"Generated {len(result['character_prompts'])} character prompts")
```

---

## Troubleshooting Integration Issues

### Issue: Saga data not found

**Solution:** Check export path and ensure Saga Agent completed successfully:

```python
import os

saga_export_path = "./saga_exports/"
if not os.path.exists(saga_export_path):
    print("Run Saga Agent first to generate data")
```

### Issue: Prompts missing character data

**Solution:** Verify characters have required fields:

```python
for char in saga_data.get("characters", []):
    if not char.get("appearance"):
        print(f"Warning: {char.get('character_name')} missing appearance")
```

### Issue: Memory issues with large sagas

**Solution:** Process in batches:

```python
characters = saga_data["characters"]
batch_size = 10

for i in range(0, len(characters), batch_size):
    batch = characters[i:i+batch_size]
    # Process batch
```

---

## Support & Resources

- **Full Documentation:** `README_AGENT.md`
- **Quick Start:** `QUICKSTART.md`
- **Prompt Engineering Guide:** `GUIDE.md` and `README.md`
- **Example Script:** `run_example.py`

---

## Contributing

When extending RenderPrepAgent:

1. Follow existing patterns (services, nodes, state)
2. Add tests for new features
3. Update documentation
4. Maintain compatibility with Saga/Orchestrator outputs

---

**Happy Integrating! 🚀**

