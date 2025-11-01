# RenderPrepAgent

**AI-Powered Image Prompt Generation for Game Narratives**

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/your-repo)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)](README_AGENT.md)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)

---

## What is RenderPrepAgent?

RenderPrepAgent transforms game narrative outputs from the **Saga Agent** and **Orchestrator** into professional-grade image generation prompts optimized for **Nano Banana** (Google DeepMind's AI image generator).

### Key Features

✅ **Professional Prompt Engineering** - Implements industry-standard techniques  
✅ **Multi-Category Support** - Characters, environments, items, storyboards  
✅ **Quality Presets** - Draft, standard, premium quality levels  
✅ **Nano Banana Integration** - Optional automated image generation  
✅ **LangGraph Workflow** - Sequential processing with checkpoints  
✅ **Comprehensive Exports** - JSON and Markdown formats

---

## Quick Start

```bash
# 1. Generate a saga (if you don't have one)
python -m SagaAgent.agent --topic "Cyberpunk Detective RPG"

# 2. Generate image prompts
python -m RenderPrepAgent.agent ./saga_exports/

# 3. View results in ./saga_exports/renders/
```

**That's it!** You now have professional image prompts ready to use.

---

## Example Output

**Input:** Character from saga
```json
{
  "character_name": "Elara Moonwhisper",
  "appearance": "Silver-haired elf mage with emerald eyes, wearing flowing robes adorned with arcane runes"
}
```

**Output:** Optimized prompt
```json
{
  "positive_prompt": "character portrait of ((Elara Moonwhisper, Protagonist)), ((silver hair)), ((emerald eyes)), ((flowing mage robes)), confident stance, [neutral background:0.8], ((fantasy art, concept art style, painterly, epic)), soft natural lighting, rim light on edges, 8K, sharp focus, professional",
  "negative_prompt": "extra limbs, extra fingers, bad anatomy, blurry, low quality, watermark, text"
}
```

---

## Documentation

📖 **[Complete Documentation](README_AGENT.md)** - Full feature guide and API reference  
🚀 **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes  
🔗 **[Integration Guide](INTEGRATION.md)** - Integrate with Saga/Orchestrator  
📝 **[Syntax Guide](GUIDE.md)** - Prompt engineering techniques  
📊 **[Project Structure](PROJECT_STRUCTURE.md)** - Code organization  
📦 **[Delivery Summary](DELIVERY_SUMMARY.md)** - What was delivered

---

## Usage

### CLI

```bash
# Basic usage
python -m RenderPrepAgent.agent ./saga_exports/

# With quality preset
python -m RenderPrepAgent.agent ./saga_exports/ --quality premium

# Generate actual images (requires API key)
export NANO_BANANA_API_KEY="your_key"
python -m RenderPrepAgent.agent ./saga_exports/ --generate-images
```

### Programmatic

```python
from RenderPrepAgent.agent import run_render_prep, load_saga_data
from RenderPrepAgent.config import AgentConfig

# Load saga data
saga_data = load_saga_data("./saga_exports/my_saga.json")

# Configure and run
config = AgentConfig(quality_preset="premium")
result = run_render_prep(saga_data, config)

# Access prompts
for char in result['character_prompts']:
    print(f"{char['name']}: {char['positive_prompt']}")
```

### Example Script

```bash
python RenderPrepAgent/run_example.py
```

---

## Architecture

```
Saga Agent Output → RenderPrepAgent → Optimized Prompts → Nano Banana → Images
```

**Workflow:**
1. Load saga data (concept, characters, world, plot)
2. Generate character prompts (with emphasis and negatives)
3. Generate environment prompts (locations, atmospheres)
4. Generate item prompts (weapons, artifacts)
5. Generate storyboard prompts (key plot moments)
6. Optionally generate images via Nano Banana API
7. Export to JSON and Markdown

---

## Prompt Engineering

RenderPrepAgent implements professional techniques:

### Structured Syntax

```
[Image Type] of [Subject] + [Action], [Setting/Context], [Style], [Lighting], [Technical Details]
```

### Emphasis Weighting

```
(word)       = 1.1x emphasis
((word))     = 1.2x emphasis
(((word)))   = 1.3x emphasis
((((word)))) = 1.4x emphasis
```

### Negative Prompts

Automatically includes:
- **Anatomy issues:** extra limbs, malformed features
- **Quality issues:** blurry, low resolution, artifacts  
- **Unwanted elements:** watermarks, text, logos

### Context-Aware Optimization

- 10 art style presets (fantasy, realistic, anime, etc.)
- 8 lighting presets (dramatic, soft, natural, etc.)
- Quality-based technical specifications

See **[GUIDE.md](GUIDE.md)** for complete syntax guide.

---

## Configuration

### Environment Variables

```bash
# Required
RENDER_EXPORT_DIR=./saga_exports/renders/

# Optional - Quality
RENDER_QUALITY=standard  # draft | standard | premium
RENDER_IMAGE_SIZE=1024x1024

# Optional - Nano Banana API
NANO_BANANA_API_KEY=your_api_key_here

# Optional - Model
RENDER_MODEL=gemini-2.0-flash-exp
RENDER_TEMPERATURE=0.7
```

---

## Integration

### With Saga Agent (CLI Pipeline)

```bash
# Generate saga
python -m SagaAgent.agent --topic "My Game"

# Generate prompts
python -m RenderPrepAgent.agent ./saga_exports/
```

### With Orchestrator (Automated)

```python
from RenderPrepAgent.agent import run_render_prep

# After saga completion
render_result = run_render_prep(saga_state, render_config)
```

See **[INTEGRATION.md](INTEGRATION.md)** for detailed integration patterns.

---

## Project Structure

```
RenderPrepAgent/
├── agent.py                              # Main LangGraph agent
├── config.py                             # Configuration
├── state.py                              # State management
├── services/
│   ├── prompt_engineering_service.py     # Core prompt engineering (600+ lines)
│   ├── nano_banana_service.py            # API integration
│   └── export_service.py                 # JSON/Markdown exporters
├── nodes/
│   ├── character_nodes.py                # Character prompts
│   ├── environment_nodes.py              # Environment prompts
│   ├── item_nodes.py                     # Item prompts
│   ├── storyboard_nodes.py               # Storyboard prompts
│   └── image_generation_node.py          # Image generation
└── [Documentation files]
```

---

## Statistics

- **Total Code:** 2,500+ lines
- **Documentation:** 2,000+ lines  
- **Files:** 22 files
- **Categories:** 4 (characters, environments, items, storyboards)
- **Quality Presets:** 3 (draft, standard, premium)
- **Art Styles:** 10+ presets
- **Lighting Presets:** 8+ presets

---

## Requirements

All dependencies already in `requirements.txt`:
- langchain, langgraph, langchain-core
- httpx (for async HTTP)
- pydantic (for models)
- dotenv (for config)

---

## Status

✅ **Production Ready**  
✅ **Fully Documented**  
✅ **Tested & Validated**  
✅ **Ready for Deployment**

---

## Support

- **Documentation:** [README_AGENT.md](README_AGENT.md)
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
- **Integration:** [INTEGRATION.md](INTEGRATION.md)
- **Examples:** [run_example.py](run_example.py)

---

## License

See LICENSE file for details.

---

<br>

---

<br>

# Original Prompt Engineering Guide

> **Note:** The sections below are from the original GUIDE.md and README.md,  
> preserved for reference. The RenderPrepAgent automatically applies these techniques.

---

# Prompt Weighting/Emphasis in Image Generation

<img width="1024" height="1024" alt="b347001f-f88d-414d-ae20-424548bf705e" src="https://github.com/user-attachments/assets/0f0a8743-02b5-4d1c-ad9e-9bce7ba7d032" />

Prompt weighting or Prompt Emphasis is a commonly used term in the AI image generation community—especially among users of models like Stable Diffusion but it's more of an informal, practical term than a formal technical one.

> So, how does this work?

When you write:

- (word) → it increases the attention weight or emphasis the model gives to that token during generation.
- [word:0.8] → It uses prompt interpolation or CFG (Classifier-Free Guidance) scaling per token.

So technically, you're adjusting the token influence or guidance scale per concept, not "weighting" in a strict ML sense. But `Prompt Weighting` has become the widely accepted shorthand.

### tl;dr:

- AUTOMATIC1111 WebUI (popular Stable Diffusion interface): Labels it as “emphasis” but users call it weighting.
- ComfyUI: Refer to it as `Prompt attention` or `emphasis syntax.`
- Research papers: Use terms like `token-level guidance scaling` or `per-token CFG.`

Let's understand the basics...

## Prompt Syntax Structure

AI image generators prioritize words at the beginning of prompts, so place your most important elements first.

### Basic Syntax

```
[Image Type] of [Subject] + [Action], [Setting/Context], [Style], [Lighting], [Technical Details]
```

Priority Order

- Image Type (photo, illustration, 3D render)
- Subject (main focus)
- Action (what the subject is doing)
- Setting/Context (environment, background)
- Style (artistic approach)
- Lighting (mood and illumination)
- Technical Details (quality, camera specs)

#### A detailed Guide on each type is mentioned here: [GUIDE.md](https://github.com/lucifertrj/Image-Prompt-Engineering/blob/main/GUIDE.md)

### Negative Prompts

Negative prompts specify what shouldn't be included in your image, helping filter out distortions, unwanted objects, or messy artifacts. Without negative prompts, even advanced AI models may produce distorted anatomy like extra limbs, blurry details, unnatural textures, or random artifacts.

When you enter a negative prompt, the AI assigns a lower probability to those terms, making it less likely to generate them. This is especially useful for common AI issues like malformed hands, asymmetrical faces, or unwanted background elements.

> Syntax

Basic Format:

- Positive Prompt: [Your main prompt]
- Negative Prompt: [Elements to exclude, separated by commas]

```
Weighted Negative Prompts: 
Negative Prompt: (extra fingers:1.3), blurry, (distorted face:1.2)
```

#### Common Negative Prompt Categories

Anatomy Issues:
```
extra limbs, extra fingers, missing fingers, poorly drawn hands, 
bad anatomy, extra arms, fused fingers, malformed limbs, 
poorly drawn face, distorted eyes, asymmetrical features
```

Quality Issues:
```
blurry, low quality, low resolution, worst quality, grainy, 
pixelated, jpeg artifacts, out of focus, bad composition
```

Unwanted Elements:
```
watermark, signature, text, logo, username, 
duplicate, cropped, out of frame
```

## Prompt Weighting or Prompt Emphasis

Weighting/Emphasis helps control which elements receive more or less emphasis in the final image.

> Syntax (Model-Dependent)

Parentheses Method:
```
(word) = 1.1x emphasis
((word)) = 1.2x emphasis  
(((word))) = 1.3x emphasis
```

Bracket Method:
```
[word:0.8] = 80% weight
[word:1.2] = 120% weight
```

Weight Distribution Guidelines:
```
Primary focus: 1.2-1.4x
Supporting elements: 1.0-1.2x
Background: 0.7-0.9x
Style/mood: 1.0-1.2x
```

### Examples

> Fantasy Scene

```
Positive Prompt:
(fantasy castle:1.4) carved into a floating obsidian monolith, (glowing rune-etched spires:1.3), (bioluminescent vines:1.2) winding through shattered gothic arches, (mist-wrapped spiral staircase ascending into storm clouds:1.3), (ethereal violet aurora:1.2) overhead, (moody indigo and emerald palette:1.3), ultra-detailed 8K, cinematic atmosphere, volumetric fog, no people, no fire, no torches

Negative Prompt:
(realistic:1.4), (modern:1.3), (marble:1.2), (sunlight:1.3), (warm tones:1.2), clutter, text, logo, symmetry
```

<img width="1024" height="1024" alt="75264ffb-96a3-48f4-a074-0dc3d753bbec" src="https://github.com/user-attachments/assets/bb9bf4b2-c45a-4c5c-89eb-c7b360df37cd" />

> Young Woman

```
(((portrait))) of ((young woman:1.3)), 
(flowing red hair:1.2), 
(freckles:0.9),
[forest background:0.8],
((soft lighting:1.2))
```

![unnamed](https://github.com/user-attachments/assets/a0f2ea06-e28b-4d7a-b440-63d813d2f3ab)

> Product Photography

```
Positive Prompt:
(product shot:1.3), (matte-finish smartwatch on brushed steel:1.4), soft ambient light from a north-facing window, subtle shadow play, muted greys and warm neutrals, (precision engineering aesthetic:1.3), shallow depth of field with tack-sharp watch face, (minimalist industrial still life:1.2), 8K, natural texture, no props, no styling

Negative Prompt:
(marble:1.5), (flowers:1.5), (wood:1.3), (white background:1.2), studio lighting, ring light, glow, reflection, blur, clutter, wrist, hand, logo, watermark
```
<img width="1024" height="1024" alt="Generated Image October 31, 2025 - 8_51PM" src="https://github.com/user-attachments/assets/b39f63e6-72c7-4f7f-8d87-e0ec43de3fd6" />

