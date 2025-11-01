# RenderPrepAgent Quick Start Guide

Get started with RenderPrepAgent in 5 minutes!

---

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment (optional):**
```bash
# Create .env file
echo "RENDER_EXPORT_DIR=./saga_exports/renders/" >> .env
echo "RENDER_QUALITY=standard" >> .env
```

---

## Basic Usage

### Step 1: Generate a Saga (if you don't have one)

```bash
# Use Saga Agent to create a game narrative
export AUTO_CONTINUE=true
python -m SagaAgent.agent --topic "Cyberpunk Detective RPG"
```

This will create JSON files in `./saga_exports/`

### Step 2: Generate Image Prompts

```bash
# Generate image prompts from saga output
python -m RenderPrepAgent.agent ./saga_exports/
```

### Step 3: View Results

Check `./saga_exports/renders/` for:
- Character image prompts
- Environment image prompts
- Item image prompts
- Storyboard image prompts

Both JSON (machine-readable) and Markdown (human-readable) formats.

---

## Example Workflow

### 1. From Single JSON File

```bash
# Generate prompts from a single saga file
python -m RenderPrepAgent.agent ./saga_exports/My_Game_concept_20251031.json
```

### 2. From Directory

```bash
# Process all JSON files in a directory
python -m RenderPrepAgent.agent ./saga_exports/my_saga_folder/
```

### 3. With Quality Preset

```bash
# Use premium quality (maximum detail)
python -m RenderPrepAgent.agent ./saga_exports/ --quality premium

# Use draft quality (fast iteration)
python -m RenderPrepAgent.agent ./saga_exports/ --quality draft
```

### 4. Generate Actual Images (Optional)

Requires Nano Banana API key:

```bash
# Set API key
export NANO_BANANA_API_KEY="your_api_key_here"

# Generate images
python -m RenderPrepAgent.agent ./saga_exports/ --generate-images
```

---

## Understanding the Output

### Character Prompt Example

```json
{
  "id": "alex_cipher",
  "name": "Alex Cipher",
  "type": "Protagonist",
  "positive_prompt": "character portrait of ((Alex Cipher, Protagonist)), ((cybernetic implants)), ((neon-lit eyes)), ((leather jacket)), standing pose, confident stance, [neutral background:0.8], ((cyberpunk style, concept art)), dramatic lighting, 8K, sharp focus, professional",
  "negative_prompt": "extra limbs, bad anatomy, blurry, low quality, watermark, text, multiple people",
  "original_description": "Street-smart detective with cybernetic implants and neon-lit eyes",
  "metadata": {
    "character_type": "Protagonist",
    "art_style": "cyberpunk",
    "quality_preset": "standard"
  }
}
```

### What Each Field Means

- **positive_prompt**: Ready-to-use prompt for image generation
- **negative_prompt**: Elements to avoid in the image
- **original_description**: Source text from saga
- **metadata**: Additional context and settings

---

## Using the Generated Prompts

### Option 1: Copy-Paste to Image Generators

1. Open the Markdown file (e.g., `*_characters_prompts_*.md`)
2. Copy the positive and negative prompts
3. Paste into your image generator:
   - Nano Banana
   - Stable Diffusion
   - DALL-E
   - Midjourney
   - Leonardo.ai

### Option 2: Automated Generation (with API)

```bash
# Set API key and generate images automatically
export NANO_BANANA_API_KEY="your_key"
python -m RenderPrepAgent.agent ./saga_exports/ --generate-images
```

### Option 3: Programmatic Usage

```python
from RenderPrepAgent.agent import run_render_prep, load_saga_data
from RenderPrepAgent.config import AgentConfig

# Load saga
saga_data = load_saga_data("./saga_exports/my_saga.json")

# Configure
config = AgentConfig(quality_preset="premium")

# Generate prompts
result = run_render_prep(saga_data, config)

# Access prompts
for char_prompt in result['character_prompts']:
    print(f"{char_prompt['name']}: {char_prompt['positive_prompt']}")
```

---

## Tips for Best Results

### 1. **Quality Presets**

- **Draft:** Use for rapid prototyping and iteration
- **Standard:** Best balance of quality and speed (recommended)
- **Premium:** Maximum detail, best for final production

### 2. **Saga Input Quality**

Better saga descriptions = better prompts:

**Good:**
```json
{
  "appearance": "Tall elf warrior with silver armor, flowing red cape, and a legendary glowing sword"
}
```

**Better:**
```json
{
  "appearance": "Tall, muscular elf warrior with intricate silver plate armor adorned with nature motifs. Flowing crimson cape. Wielding the legendary sword 'Dawnbringer' that glows with golden holy light. Emerald eyes, long platinum blonde hair in a warrior's braid."
}
```

### 3. **Art Style Consistency**

Set a consistent art style in your saga's concept:
- `"art_style": "fantasy"` - Traditional fantasy art
- `"art_style": "realistic"` - Photorealistic
- `"art_style": "anime"` - Anime/manga style
- `"art_style": "cyberpunk"` - Futuristic cyberpunk
- `"art_style": "3D render"` - 3D CGI style

### 4. **Editing Prompts**

Generated prompts are optimized but can be customized:

```json
// Before
"positive_prompt": "character portrait of ((Hero)), ((sword)), fantasy art"

// After customization
"positive_prompt": "character portrait of (((Hero))), (((legendary flaming sword))), fantasy art, dramatic pose"
```

---

## Common Workflows

### Workflow 1: Game Concept Art Generation

```bash
# 1. Generate saga
python -m SagaAgent.agent --topic "My Game Idea"

# 2. Generate all image prompts
python -m RenderPrepAgent.agent ./saga_exports/ --quality premium

# 3. Use prompts in your preferred image generator
# 4. Integrate generated images into game design docs
```

### Workflow 2: Rapid Prototyping

```bash
# Quick iteration cycle
python -m SagaAgent.agent --topic "Quick Prototype"
python -m RenderPrepAgent.agent ./saga_exports/ --quality draft
# Review prompts, adjust saga, repeat
```

### Workflow 3: Production Pipeline

```bash
# Full production with image generation
export NANO_BANANA_API_KEY="your_key"
python -m SagaAgent.agent --topic "Production Game"
python -m RenderPrepAgent.agent ./saga_exports/ --quality premium --generate-images
# Images automatically generated and saved
```

---

## Troubleshooting

### Problem: "No characters found"

**Solution:** Check your saga JSON has a `characters` array with character data.

### Problem: "Prompts are too long"

**Solution:** Use `--quality draft` or adjust `RENDER_MAX_PROMPT_LENGTH`:
```bash
export RENDER_MAX_PROMPT_LENGTH=400
python -m RenderPrepAgent.agent ./saga_exports/
```

### Problem: "API key error"

**Solution:** Verify your Nano Banana API key is set:
```bash
echo $NANO_BANANA_API_KEY  # Should print your key
```

Or run without image generation:
```bash
python -m RenderPrepAgent.agent ./saga_exports/
# (don't use --generate-images flag)
```

---

## Next Steps

1. **Read the full documentation:** `README_AGENT.md`
2. **Learn prompt engineering:** `GUIDE.md` and `README.md`
3. **Explore examples:** Check the `examples/` directory
4. **Integrate with your workflow:** Use programmatic API

---

## Need Help?

- Check the full README: `README_AGENT.md`
- Review example outputs in `./saga_exports/renders/`
- Test with the included example saga data

Happy generating! 🎨✨

