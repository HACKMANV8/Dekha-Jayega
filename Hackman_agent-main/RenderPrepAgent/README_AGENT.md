# RenderPrepAgent: AI-Powered Image Prompt Generation

**Version:** 1.0.0  
**Status:** Production Ready

---

## Overview

RenderPrepAgent is an intelligent image prompt generation system that transforms game narrative outputs from the Saga Agent and Orchestrator into professional-grade image generation prompts optimized for **Nano Banana** (Google DeepMind's AI image generator).

### What It Does

1. **Ingests** Saga/Orchestrator narrative outputs (JSON format)
2. **Analyzes** characters, environments, items, and plot moments
3. **Generates** optimized image prompts using professional prompt engineering techniques
4. **Applies** emphasis weighting, negative prompts, and structured formatting
5. **Optionally generates** actual images via Nano Banana API
6. **Exports** prompts in JSON and Markdown formats

### Key Features

✅ **Professional Prompt Engineering**
- Implements techniques from industry-standard prompt engineering guides
- Structured syntax: `[Image Type] of [Subject] + [Action], [Setting], [Style], [Lighting], [Technical]`
- Emphasis weighting using parentheses method: `(word)`, `((word))`, `(((word)))`
- Comprehensive negative prompts to avoid common AI issues

✅ **Multi-Category Support**
- Character portraits (protagonists, companions, NPCs, villains)
- Environment/location art (worlds, cities, headquarters, dungeons)
- Item/equipment concept art (weapons, artifacts, magical items)
- Storyboard frames (key plot moments, cinematic scenes)

✅ **Quality Presets**
- **Draft:** Fast iterations (4K, good focus)
- **Standard:** Production quality (8K, sharp focus, professional)
- **Premium:** Maximum quality (8K, ultra detailed, photorealistic, ray tracing)

✅ **Nano Banana Integration**
- Optional image generation via API
- Batch processing support
- Mock mode for testing without API key

✅ **LangGraph Workflow**
- Sequential processing pipeline
- Checkpoint persistence
- Error handling and recovery

---

## Installation

### Prerequisites

- Python 3.10+
- Saga Agent and/or Orchestrator Agent outputs
- (Optional) Nano Banana API key for image generation

### Setup

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**

Create a `.env` file or set environment variables:

```bash
# Required
RENDER_EXPORT_DIR=./saga_exports/renders/

# Optional - Nano Banana API (for actual image generation)
NANO_BANANA_API_KEY=your_api_key_here
NANO_BANANA_ENDPOINT=https://api.google.com/nano-banana/v1

# Optional - Quality settings
RENDER_QUALITY=standard  # draft, standard, premium
RENDER_IMAGE_SIZE=1024x1024
RENDER_USE_WEIGHTING=true

# Optional - Model settings
RENDER_MODEL=gemini-2.0-flash-exp
RENDER_TEMPERATURE=0.7
```

---

## Usage

### Basic Usage

Generate image prompts from Saga output:

```bash
python -m RenderPrepAgent.agent ./saga_exports/my_saga_concept.json
```

### With Quality Preset

```bash
python -m RenderPrepAgent.agent ./saga_exports/ --quality premium
```

### Generate Actual Images

Requires Nano Banana API key:

```bash
python -m RenderPrepAgent.agent ./saga_exports/ --generate-images
```

### From Directory

Process all JSON files in a directory:

```bash
python -m RenderPrepAgent.agent ./saga_exports/my_saga/
```

---

## Input Format

RenderPrepAgent accepts Saga/Orchestrator outputs in JSON format:

### Single File

```json
{
  "concept": {
    "title": "My Epic Game",
    "art_style": "fantasy",
    ...
  },
  "characters": [...],
  "world_lore": {...},
  "factions": [...],
  "plot_arcs": [...],
  "questlines": [...]
}
```

### Multiple Files

Directory structure:
```
saga_exports/
├── My_Epic_Game_concept_20251031_120000.json
├── My_Epic_Game_characters_20251031_120000.json
├── My_Epic_Game_world_lore_20251031_120000.json
├── My_Epic_Game_factions_20251031_120000.json
├── My_Epic_Game_plot_arcs_20251031_120000.json
└── My_Epic_Game_questlines_20251031_120000.json
```

---

## Output Format

### Generated Files

For each category, RenderPrepAgent generates:

1. **JSON files** (structured data):
   - `{title}_characters_prompts_{timestamp}.json`
   - `{title}_environments_prompts_{timestamp}.json`
   - `{title}_items_prompts_{timestamp}.json`
   - `{title}_storyboards_prompts_{timestamp}.json`
   - `{title}_render_summary_{timestamp}.json`

2. **Markdown files** (human-readable):
   - `{title}_characters_prompts_{timestamp}.md`
   - `{title}_environments_prompts_{timestamp}.md`
   - `{title}_items_prompts_{timestamp}.md`
   - `{title}_storyboards_prompts_{timestamp}.md`

### Example Output Structure

```json
{
  "id": "elara_moonwhisper",
  "name": "Elara Moonwhisper",
  "type": "Protagonist",
  "positive_prompt": "character portrait of ((Elara Moonwhisper, Protagonist)), ((silver hair)), ((emerald eyes)), ((flowing mage robes)), confident stance, [neutral background:0.8], ((fantasy art, concept art style, painterly, epic)), soft natural lighting, rim light on edges, 8K, sharp focus, professional",
  "negative_prompt": "extra limbs, extra fingers, missing fingers, poorly drawn hands, bad anatomy, extra arms, fused fingers, malformed limbs, poorly drawn face, distorted eyes, asymmetrical features, blurry, low quality, low resolution, worst quality, grainy, pixelated, jpeg artifacts, out of focus, bad composition, watermark, signature, text, logo, username, duplicate, cropped, out of frame, multiple people, crowd, group",
  "original_description": "Silver-haired elf mage with emerald eyes, wearing flowing robes adorned with arcane runes",
  "metadata": {
    "character_type": "Protagonist",
    "art_style": "fantasy",
    "quality_preset": "standard",
    "role": "The wise mentor guiding the player",
    "personality": "Mysterious, wise, compassionate"
  }
}
```

---

## Prompt Engineering Techniques

RenderPrepAgent implements professional techniques from the included guides:

### 1. **Structured Syntax**

Every prompt follows the optimal order:
```
[Image Type] of [Subject] + [Action], [Setting/Context], [Style], [Lighting], [Technical Details]
```

### 2. **Emphasis Weighting**

- `(word)` = 1.1x emphasis
- `((word))` = 1.2x emphasis  
- `(((word)))` = 1.3x emphasis
- `((((word))))` = 1.4x emphasis

Applied to:
- **Primary focus:** 1.2-1.4x (main subject, key features)
- **Supporting elements:** 1.0-1.2x (secondary features)
- **Background:** 0.7-0.9x (environment, setting)
- **Style/mood:** 1.0-1.2x (art style, atmosphere)

### 3. **Negative Prompts**

Every prompt includes comprehensive negative prompts:

**Anatomy Issues:**
```
extra limbs, extra fingers, missing fingers, poorly drawn hands, bad anatomy, 
extra arms, fused fingers, malformed limbs, poorly drawn face, distorted eyes, 
asymmetrical features
```

**Quality Issues:**
```
blurry, low quality, low resolution, worst quality, grainy, pixelated, 
jpeg artifacts, out of focus, bad composition
```

**Unwanted Elements:**
```
watermark, signature, text, logo, username, duplicate, cropped, out of frame
```

### 4. **Art Style Presets**

Automatically applies style-specific optimizations:

- **Fantasy:** concept art, painterly, epic
- **Realistic:** photorealistic, cinematic, professional photography
- **Anime:** cel shaded, vibrant colors, manga style
- **3D:** CGI, octane render, physically based rendering
- **And more...**

### 5. **Lighting Presets**

Context-aware lighting selection:

- **Dramatic:** Hard light, chiaroscuro, rim light
- **Soft:** Diffused light, gentle illumination
- **Natural:** Golden hour, soft shadows
- **Atmospheric:** Volumetric fog, god rays
- **Magical:** Ethereal glow, bioluminescent

---

## Architecture

### Workflow Pipeline

```
START
  ↓
Character Prompts
  ↓
Environment Prompts
  ↓
Item Prompts
  ↓
Storyboard Prompts
  ↓
Generate Images (optional)
  ↓
Export All
  ↓
END
```

### Core Services

1. **PromptEngineeringService**
   - Implements GUIDE.md and README.md techniques
   - Builds optimized prompts with proper weighting
   - Generates category-specific negative prompts

2. **NanoBananaService**
   - Integrates with Nano Banana API
   - Supports batch image generation
   - Includes mock mode for testing

3. **RenderExportService**
   - Exports prompts to JSON and Markdown
   - Creates master summary
   - Organizes outputs by category

### State Management

Uses LangGraph's `RenderPrepState` TypedDict:

```python
class RenderPrepState(TypedDict):
    saga_data: Dict[str, Any]  # Input from Saga/Orchestrator
    character_prompts: List[Dict[str, Any]]
    environment_prompts: List[Dict[str, Any]]
    item_prompts: List[Dict[str, Any]]
    storyboard_prompts: List[Dict[str, Any]]
    generated_images: List[Dict[str, Any]]  # Optional
    # ... and more
```

---

## Integration with Saga/Orchestrator

### Option 1: CLI Pipeline

```bash
# 1. Generate saga
python -m SagaAgent.agent --topic "Epic Fantasy RPG"

# 2. Generate image prompts
python -m RenderPrepAgent.agent ./saga_exports/
```

### Option 2: Programmatic

```python
from RenderPrepAgent.agent import run_render_prep, load_saga_data
from RenderPrepAgent.config import AgentConfig

# Load saga data
saga_data = load_saga_data("./saga_exports/my_saga.json")

# Configure agent
config = AgentConfig(
    quality_preset="premium",
    generate_images=False
)

# Run render prep
final_state = run_render_prep(saga_data, config)

print(f"Generated {len(final_state['character_prompts'])} character prompts")
```

### Option 3: Orchestrator Integration

The Orchestrator can automatically trigger RenderPrepAgent after saga completion:

```python
# In orchestrator workflow
if saga_complete:
    render_state = run_render_prep(saga_state, render_config)
```

---

## Examples

### Character Prompt Example

**Input:**
```json
{
  "character_name": "Kael Ironheart",
  "character_type": "Warrior",
  "appearance": "Scarred veteran with short black hair, wearing battle-worn plate armor, wielding a legendary greatsword"
}
```

**Generated Positive Prompt:**
```
character portrait of ((Kael Ironheart, Warrior)), ((scarred veteran)), ((short black hair)), ((battle-worn plate armor)), ((legendary greatsword)), standing pose, confident stance, [neutral background:0.8], ((fantasy art, concept art style, painterly, epic)), soft natural lighting, rim light on edges, 8K, sharp focus, professional
```

**Generated Negative Prompt:**
```
extra limbs, extra fingers, missing fingers, poorly drawn hands, bad anatomy, extra arms, fused fingers, malformed limbs, poorly drawn face, distorted eyes, asymmetrical features, blurry, low quality, low resolution, worst quality, grainy, pixelated, jpeg artifacts, out of focus, bad composition, watermark, signature, text, logo, username, duplicate, cropped, out of frame, multiple people, crowd, group
```

### Environment Prompt Example

**Input:**
```json
{
  "location_name": "Shadowspire Citadel",
  "location_type": "Fortress",
  "description": "Dark obsidian fortress built into mountainside, glowing magical wards, ominous architecture"
}
```

**Generated Positive Prompt:**
```
environment concept art of ((Fortress)), Dark obsidian fortress built into mountainside, glowing magical wards, ominous architecture, clear day, ((Imposing and organized)), ((fantasy art, concept art style, painterly, epic)), dramatic lighting, hard light, chiaroscuro, rim light, 8K, sharp focus, professional, no people
```

---

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `RENDER_EXPORT_DIR` | `./saga_exports/renders/` | Export directory |
| `RENDER_QUALITY` | `standard` | Quality preset |
| `RENDER_IMAGE_SIZE` | `1024x1024` | Image dimensions |
| `RENDER_USE_WEIGHTING` | `true` | Enable emphasis weighting |
| `RENDER_MAX_PROMPT_LENGTH` | `500` | Max prompt length |
| `NANO_BANANA_API_KEY` | `` | API key (optional) |
| `NANO_BANANA_ENDPOINT` | `https://api.google.com/nano-banana/v1` | API endpoint |
| `RENDER_MODEL` | `gemini-2.0-flash-exp` | LLM model |
| `RENDER_TEMPERATURE` | `0.7` | Generation temperature |

### Quality Presets

| Preset | Technical Details | Render Quality | Emphasis Weight |
|--------|-------------------|----------------|-----------------|
| **draft** | 4K, good focus | standard quality | 1.1x |
| **standard** | 8K, sharp focus, professional | high quality, detailed | 1.2x |
| **premium** | 8K, ultra detailed, sharp focus, professional | ultra high quality, photorealistic, ray tracing | 1.3x |

---

## Troubleshooting

### Common Issues

**1. No characters/environments generated**

Check that your saga data contains the required fields:
- `characters` array with `character_name` and `appearance`
- `world_lore` object with `geography` or `civilizations`

**2. Prompts too long**

Adjust `RENDER_MAX_PROMPT_LENGTH` in config or use `draft` quality preset.

**3. Nano Banana API errors**

- Verify `NANO_BANANA_API_KEY` is set correctly
- Check API endpoint is accessible
- Use mock mode for testing: don't set API key

**4. Import errors**

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

---

## Performance

### Benchmarks

- **Prompt Generation:** ~100-200 prompts/second (without API calls)
- **Batch Image Generation:** Depends on API rate limits
- **Export:** ~500 prompts/second

### Optimization Tips

1. Use `draft` preset for rapid iteration
2. Disable image generation (`--generate-images=false`) for prompt-only workflow
3. Process large sagas in batches
4. Cache generated prompts for reuse

---

## Roadmap

### Planned Features

- [ ] Support for additional image generation APIs (DALL-E, Midjourney, Stable Diffusion)
- [ ] Interactive prompt refinement with human-in-the-loop
- [ ] Style transfer between different art styles
- [ ] Automatic prompt A/B testing
- [ ] Integration with asset management systems
- [ ] Video generation support (when available)

---

## Credits

**Prompt Engineering Techniques:** Based on industry-standard guides for AI image generation  
**Nano Banana:** Google DeepMind's AI image generation technology  
**LangGraph:** Workflow orchestration framework

---

## License

See LICENSE file for details.

---

## Support

For issues, questions, or contributions, please refer to the main project repository.

