"""Environment prompt generation nodes."""
from typing import Dict, Any, List
from RenderPrepAgent.services.prompt_engineering_service import PromptEngineeringService
from RenderPrepAgent.config import RenderConfig


def generate_environment_prompts_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate optimized image prompts for environments/locations.
    
    Args:
        state: RenderPrepState with saga_data
    
    Returns:
        Dict with environment_prompts list
    """
    print("\n--- NODE: GENERATING ENVIRONMENT PROMPTS ---")
    
    saga_data = state.get("saga_data", {})
    world_lore = saga_data.get("world_lore", {})
    factions = saga_data.get("factions", [])
    concept = saga_data.get("concept", {})
    
    # Get quality preset
    quality_preset_name = state.get("quality_preset", "standard")
    quality_preset = RenderConfig.get_quality_preset(quality_preset_name)
    
    # Get art style from concept
    art_style = concept.get("art_style", "fantasy") if isinstance(concept, dict) else "fantasy"
    
    environment_prompts = []
    
    # === World Overview ===
    if world_lore:
        world_name = world_lore.get("world_name", "Unknown World")
        geography = world_lore.get("geography", "")
        atmosphere = world_lore.get("setting_overview", "Epic fantasy world")
        
        if geography:
            print(f"  ✓ Processing: {world_name} (World Overview)")
            
            prompts = PromptEngineeringService.build_environment_prompt(
                location_name=world_name,
                location_type="World Landscape",
                description=geography,
                atmosphere=atmosphere,
                art_style=art_style,
                key_features=[world_lore.get("magic_or_technology", "Magic")],
                quality_preset=quality_preset
            )
            
            env_prompt = {
                "id": f"{world_name.lower().replace(' ', '_')}_overview",
                "name": f"{world_name} - World Overview",
                "type": "World Landscape",
                "positive_prompt": prompts["positive_prompt"],
                "negative_prompt": prompts["negative_prompt"],
                "original_description": geography,
                "metadata": {
                    "location_type": "World Overview",
                    "art_style": art_style,
                    "quality_preset": quality_preset_name,
                    "climate": world_lore.get("climate_cosmology", ""),
                    "atmosphere": atmosphere
                }
            }
            
            environment_prompts.append(env_prompt)
    
    # === Faction Headquarters ===
    for faction in factions:
        faction_name = faction.get("faction_name", "Unknown Faction")
        headquarters = faction.get("headquarters", "")
        aesthetic = faction.get("aesthetic_identity", "")
        
        if headquarters:
            print(f"  ✓ Processing: {faction_name} Headquarters")
            
            # Combine headquarters description with aesthetic
            description = f"{headquarters}. {aesthetic}".strip()
            
            # Extract key features from description
            key_features = []
            if faction.get("military_strength"):
                key_features.append("fortifications")
            if "magic" in faction.get("core_ideology", "").lower():
                key_features.append("magical elements")
            
            prompts = PromptEngineeringService.build_environment_prompt(
                location_name=f"{faction_name} Headquarters",
                location_type="Headquarters",
                description=description,
                atmosphere=aesthetic or "Imposing and organized",
                art_style=art_style,
                key_features=key_features,
                quality_preset=quality_preset
            )
            
            env_prompt = {
                "id": f"{faction_name.lower().replace(' ', '_')}_hq",
                "name": f"{faction_name} Headquarters",
                "type": "Headquarters",
                "positive_prompt": prompts["positive_prompt"],
                "negative_prompt": prompts["negative_prompt"],
                "original_description": description,
                "metadata": {
                    "location_type": "Headquarters",
                    "faction": faction_name,
                    "art_style": art_style,
                    "quality_preset": quality_preset_name,
                    "aesthetic": aesthetic
                }
            }
            
            environment_prompts.append(env_prompt)
    
    # === Major Civilizations/Cities ===
    if world_lore and world_lore.get("civilizations"):
        civilizations = world_lore.get("civilizations", "")
        
        print(f"  ✓ Processing: Major City")
        
        prompts = PromptEngineeringService.build_environment_prompt(
            location_name="Major City",
            location_type="City",
            description=civilizations,
            atmosphere="Bustling and alive",
            art_style=art_style,
            key_features=["architecture", "streets", "markets"],
            quality_preset=quality_preset
        )
        
        env_prompt = {
            "id": "major_city",
            "name": "Major City",
            "type": "City",
            "positive_prompt": prompts["positive_prompt"],
            "negative_prompt": prompts["negative_prompt"],
            "original_description": civilizations,
            "metadata": {
                "location_type": "City",
                "art_style": art_style,
                "quality_preset": quality_preset_name
            }
        }
        
        environment_prompts.append(env_prompt)
    
    print(f"✓ Generated {len(environment_prompts)} environment prompts")
    
    return {"environment_prompts": environment_prompts}

