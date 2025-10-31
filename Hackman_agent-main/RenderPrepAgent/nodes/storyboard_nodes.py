"""Storyboard prompt generation nodes."""
from typing import Dict, Any
from RenderPrepAgent.services.prompt_engineering_service import PromptEngineeringService
from RenderPrepAgent.config import RenderConfig


def generate_storyboard_prompts_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate optimized image prompts for storyboard frames/key art.
    
    Args:
        state: RenderPrepState with saga_data
    
    Returns:
        Dict with storyboard_prompts list
    """
    print("\n--- NODE: GENERATING STORYBOARD PROMPTS ---")
    
    saga_data = state.get("saga_data", {})
    plot_arcs = saga_data.get("plot_arcs", [])
    characters = saga_data.get("characters", [])
    world_lore = saga_data.get("world_lore", {})
    concept = saga_data.get("concept", {})
    
    if not plot_arcs:
        print("⚠ No plot arcs found in saga data")
        return {"storyboard_prompts": []}
    
    # Get quality preset
    quality_preset_name = state.get("quality_preset", "standard")
    quality_preset = RenderConfig.get_quality_preset(quality_preset_name)
    
    # Get art style from concept
    art_style = concept.get("art_style", "fantasy") if isinstance(concept, dict) else "fantasy"
    
    storyboard_prompts = []
    
    # === Generate storyboards for key plot moments ===
    for arc_idx, plot in enumerate(plot_arcs):
        arc_title = plot.get("arc_title", f"Arc {arc_idx + 1}")
        theme = plot.get("theme", "")
        
        print(f"  ✓ Processing: {arc_title}")
        
        # === Act 1: Opening/Hook ===
        act1_hook = plot.get("act1_hook", "")
        if act1_hook:
            # Get first 2 characters for the scene
            scene_characters = [c.get("character_name", "") for c in characters[:2]]
            
            prompts = PromptEngineeringService.build_storyboard_prompt(
                scene_name=f"{arc_title} - Opening",
                visual_composition="Wide establishing shot, cinematic framing",
                key_elements=scene_characters + ["environment", "atmosphere"],
                narrative_context=act1_hook,
                mood_tone="Intriguing and mysterious",
                art_style=art_style,
                color_palette=theme if theme else "",
                quality_preset=quality_preset
            )
            
            storyboard_prompt = {
                "id": f"arc{arc_idx}_act1",
                "name": f"{arc_title} - Act 1 Opening",
                "type": "Storyboard Frame",
                "sequence_number": 1,
                "positive_prompt": prompts["positive_prompt"],
                "negative_prompt": prompts["negative_prompt"],
                "original_description": act1_hook,
                "metadata": {
                    "arc_title": arc_title,
                    "act": "Act 1",
                    "scene_type": "Opening",
                    "art_style": art_style,
                    "quality_preset": quality_preset_name,
                    "characters": scene_characters,
                    "theme": theme
                }
            }
            
            storyboard_prompts.append(storyboard_prompt)
        
        # === Act 2: Midpoint Twist ===
        midpoint = plot.get("midpoint_twist", "")
        if midpoint:
            prompts = PromptEngineeringService.build_storyboard_prompt(
                scene_name=f"{arc_title} - Midpoint",
                visual_composition="Dynamic angle, tension in framing",
                key_elements=["revelation", "conflict", "turning point"],
                narrative_context=midpoint,
                mood_tone="Tense and dramatic",
                art_style=art_style,
                color_palette="contrasting colors, dramatic lighting",
                quality_preset=quality_preset
            )
            
            storyboard_prompt = {
                "id": f"arc{arc_idx}_midpoint",
                "name": f"{arc_title} - Midpoint Twist",
                "type": "Storyboard Frame",
                "sequence_number": 2,
                "positive_prompt": prompts["positive_prompt"],
                "negative_prompt": prompts["negative_prompt"],
                "original_description": midpoint,
                "metadata": {
                    "arc_title": arc_title,
                    "act": "Act 2",
                    "scene_type": "Midpoint",
                    "art_style": art_style,
                    "quality_preset": quality_preset_name,
                    "theme": theme
                }
            }
            
            storyboard_prompts.append(storyboard_prompt)
        
        # === Act 3: Climax ===
        climax = plot.get("climax_sequence", "")
        if climax:
            prompts = PromptEngineeringService.build_storyboard_prompt(
                scene_name=f"{arc_title} - Climax",
                visual_composition="Epic wide shot, heroic framing",
                key_elements=["action", "conflict", "resolution", "heroes"],
                narrative_context=climax,
                mood_tone="Epic and triumphant",
                art_style=art_style,
                color_palette="vibrant, high contrast",
                quality_preset=quality_preset
            )
            
            storyboard_prompt = {
                "id": f"arc{arc_idx}_climax",
                "name": f"{arc_title} - Climax",
                "type": "Storyboard Frame",
                "sequence_number": 3,
                "positive_prompt": prompts["positive_prompt"],
                "negative_prompt": prompts["negative_prompt"],
                "original_description": climax,
                "metadata": {
                    "arc_title": arc_title,
                    "act": "Act 3",
                    "scene_type": "Climax",
                    "art_style": art_style,
                    "quality_preset": quality_preset_name,
                    "boss_mechanics": plot.get("boss_mechanics", ""),
                    "theme": theme
                }
            }
            
            storyboard_prompts.append(storyboard_prompt)
        
        # === Resolution/Epilogue ===
        epilogue = plot.get("epilogue", "")
        if epilogue:
            prompts = PromptEngineeringService.build_storyboard_prompt(
                scene_name=f"{arc_title} - Resolution",
                visual_composition="Peaceful composition, balance restored",
                key_elements=["characters", "reflection", "aftermath"],
                narrative_context=epilogue,
                mood_tone="Hopeful and resolved",
                art_style=art_style,
                color_palette="warm, balanced tones",
                quality_preset=quality_preset
            )
            
            storyboard_prompt = {
                "id": f"arc{arc_idx}_resolution",
                "name": f"{arc_title} - Resolution",
                "type": "Storyboard Frame",
                "sequence_number": 4,
                "positive_prompt": prompts["positive_prompt"],
                "negative_prompt": prompts["negative_prompt"],
                "original_description": epilogue,
                "metadata": {
                    "arc_title": arc_title,
                    "act": "Act 3",
                    "scene_type": "Resolution",
                    "art_style": art_style,
                    "quality_preset": quality_preset_name,
                    "theme": theme
                }
            }
            
            storyboard_prompts.append(storyboard_prompt)
    
    print(f"✓ Generated {len(storyboard_prompts)} storyboard prompts")
    
    return {"storyboard_prompts": storyboard_prompts}

