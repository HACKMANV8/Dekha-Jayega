## Syntax Guide in detail

### 1. Image Type

Why It Matters: Setting the image type first establishes how the AI interprets all other prompt elements.

Common Types

- Photography: photo, editorial photo, product shot, portrait
- Illustration: flat illustration, vector art, digital painting
- 3D: 3D render, CGI, octane render
- Traditional: oil painting, watercolor, pencil sketch

Example:

```
Editorial photo of a woman working on laptop in home office
```

### 2. Subject & Action

Why It Matters: The subject is your main focus. More descriptive prompts yield results closer to your vision.

Elements

- Who/What: person, object, animal, scenery
- Characteristics: age, appearance, features
- Action: running, sitting, looking, gesturing
- Mood: joyful, mysterious, confident

Example:

```
Indian woman, mid-50s, wearing red and yellow sari, gold earrings, talking and gesturing
```

### 3. Setting & Context

Why It Matters: Background and environment provide depth and storytelling.

Components

- Location: forest, office, city street, beach
- Time: morning, sunset, golden hour, night
- Weather: foggy, rainy, sunny, misty
- Environment details: flowers, skyscrapers, furniture

Example:

```
in a sunny home office, blue coffee mug on desk, plants in background
```

### 4. Artistic Style

Why It Matters: Style defines the visual aesthetic and artistic approach.

Style Categories

- Photography Styles: Cinematic, documentary, fashion, lifestyle, product photography
- Art Movements: Impressionism, art deco, cyberpunk, minimalist, surrealism
- Digital Styles: Flat design, isometric, low poly, pixel art, vaporwave
- Traditional Media: Oil painting, watercolor, charcoal, gouache, ink drawing

Example:

```
impressionist painting style, soft brush strokes
```

### 5. Lighting

Why It Matters: Lighting dramatically changes the look and feel of images.

Lighting Types

- Natural: golden hour, sunrise, overcast, window light
- Dramatic: hard light, chiaroscuro, rim light, backlit
- Studio: soft light, three-point lighting, studio setup
- Atmospheric: volumetric, fog, god rays, neon glow

Example:

```
soft natural lighting, golden hour glow, rim light on edges
```

### 6. Technical Specifications

Why It Matters: Technical details control quality and professional appearance.

Quality Terms

- High resolution, 8K, sharp focus, detailed, professional
- RAW photo, studio quality, ultra detailed

Camera Settings (For Photorealism)

- Camera: Nikon D6, Canon EOS R5, Sony A7
- Lens: 85mm portrait, wide-angle, macro lens
- Settings: shallow depth of field, bokeh, f/1.8

Render Quality (For 3D)

- Octane render, Unreal Engine, ray tracing, physically based rendering

Example:

```
8K, sharp focus, professional photography, shallow depth of field
```

## Best Practices

> IMPORTANT TIP: COPY THE README.md and GUIDE.md and PASTE at [Qwen-3](chat.qwen.ai) or [Gemini- AI Studio](https://aistudio.google.com) and ask your prompt and tell the LLM to modify it accordingly.

- Start simple: Begin with a minimum viable prompt and add details only if needed
- Place critical elements (subject, action) at the beginning since AI prioritizes words that appear early
- Write conversationally, describing as if to someone who can't see the image
- Be Specific, Not Generic: Use clear, descriptive language instead of vague terms like "award-winning" or "masterpiece"
- Leverage Negative Prompts: Always include negative prompts to avoid common AI issues (distorted anatomy, low quality, artifacts)
- Balance Your Prompts: Don't overload either positive or negative prompts—too many restrictions can confuse the AI
- Use prompt weighting (1.1-1.4x) for emphasis, but avoid over-weighting everything

