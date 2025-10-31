"""Character prompt generation nodes."""
from typing import Dict, Any
from RenderPrepAgent.services.prompt_engineering_service import PromptEngineeringService
from RenderPrepAgent.config import RenderConfig


def generate_character_prompts_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate optimized image prompts for characters.
    
    Transforms character data from Saga agent into professional image generation prompts
    using prompt engineering techniques from GUIDE.md and README.md.
    
    Args:
        state: RenderPrepState with saga_data
    
    Returns:
        Dict with character_prompts list
    """
    print("\n--- NODE: GENERATING CHARACTER PROMPTS ---")
    
    saga_data = state.get("saga_data", {})
    characters = saga_data.get("characters", [])
    concept = saga_data.get("concept", {})
    
    if not characters:
        print("⚠ No characters found in saga data")
        return {"character_prompts": []}
    
    # Get quality preset
    quality_preset_name = state.get("quality_preset", "standard")
    quality_preset = RenderConfig.get_quality_preset(quality_preset_name)
    
    # Get art style from concept
    art_style = concept.get("art_style", "fantasy") if isinstance(concept, dict) else "fantasy"
    
    character_prompts = []
    
    for char in characters:
        character_name = char.get("character_name", "Unknown Character")
        character_type = char.get("character_type", "NPC")
        appearance = char.get("appearance", "")
        pose = char.get("silhouette_design", "")
        color_palette = char.get("visual_themes", "")
        
        # Skip if no visual description
        if not appearance:
            print(f"⚠ Skipping {character_name}: no appearance description")
            continue
        
        print(f"  ✓ Processing: {character_name} ({character_type})")
        
        # Build optimized prompt using prompt engineering service
        prompts = PromptEngineeringService.build_character_prompt(
            character_name=character_name,
            character_type=character_type,
            appearance=appearance,
            art_style=art_style,
            pose=pose,
            color_palette=color_palette,
            quality_preset=quality_preset,
            additional_details={
                "personality": char.get("personality_traits", ""),
                "role": char.get("role_purpose", "")
            }
        )
        
        # Build character prompt data
        char_prompt = {
            "id": character_name.lower().replace(" ", "_"),
            "name": character_name,
            "type": character_type,
            "positive_prompt": prompts["positive_prompt"],
            "negative_prompt": prompts["negative_prompt"],
            "original_description": appearance,
            "metadata": {
                "character_type": character_type,
                "art_style": art_style,
                "quality_preset": quality_preset_name,
                "role": char.get("role_purpose", ""),
                "personality": char.get("personality_traits", ""),
                "backstory_summary": char.get("backstory", "")[:200] if char.get("backstory") else ""
            }
        }
        
        character_prompts.append(char_prompt)
    
    print(f"✓ Generated {len(character_prompts)} character prompts")
    
    return {"character_prompts": character_prompts}

