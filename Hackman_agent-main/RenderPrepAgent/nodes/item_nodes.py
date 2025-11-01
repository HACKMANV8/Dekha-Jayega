"""Item prompt generation nodes."""
from typing import Dict, Any
from RenderPrepAgent.services.prompt_engineering_service import PromptEngineeringService
from RenderPrepAgent.config import RenderConfig


def generate_item_prompts_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate optimized image prompts for items/equipment.
    
    Args:
        state: RenderPrepState with saga_data
    
    Returns:
        Dict with item_prompts list
    """
    print("\n--- NODE: GENERATING ITEM PROMPTS ---")
    
    saga_data = state.get("saga_data", {})
    plot_arcs = saga_data.get("plot_arcs", [])
    characters = saga_data.get("characters", [])
    concept = saga_data.get("concept", {})
    
    # Get quality preset
    quality_preset_name = state.get("quality_preset", "standard")
    quality_preset = RenderConfig.get_quality_preset(quality_preset_name)
    
    # Get art style from concept
    art_style = concept.get("art_style", "fantasy") if isinstance(concept, dict) else "fantasy"
    
    item_prompts = []
    
    # === Extract items from plot arcs (artifacts, quest items) ===
    for idx, plot in enumerate(plot_arcs):
        arc_title = plot.get("arc_title", f"Arc {idx + 1}")
        central_question = plot.get("central_question", "")
        
        # Check if plot mentions artifacts or items
        if any(keyword in central_question.lower() for keyword in ["artifact", "item", "weapon", "relic", "treasure"]):
            print(f"  ✓ Processing: Quest Artifact from {arc_title}")
            
            # Extract item description from plot
            item_description = central_question[:200]
            
            prompts = PromptEngineeringService.build_item_prompt(
                item_name=f"Quest Artifact - {arc_title}",
                item_type="Magical Artifact",
                description=item_description,
                materials="Ancient magical materials, enchanted metal",
                art_style=art_style,
                special_properties=["glowing with power", "mystical aura"],
                scale_reference="hand-held size",
                quality_preset=quality_preset
            )
            
            item_prompt = {
                "id": f"artifact_{idx}",
                "name": f"Quest Artifact - {arc_title}",
                "type": "Magical Artifact",
                "positive_prompt": prompts["positive_prompt"],
                "negative_prompt": prompts["negative_prompt"],
                "original_description": item_description,
                "metadata": {
                    "item_type": "Magical Artifact",
                    "art_style": art_style,
                    "quality_preset": quality_preset_name,
                    "related_arc": arc_title
                }
            }
            
            item_prompts.append(item_prompt)
    
    # === Extract weapons/equipment from characters ===
    for char in characters:
        character_name = char.get("character_name", "Unknown")
        combat_style = char.get("combat_style", "")
        class_abilities = char.get("class_abilities", "")
        
        # Check if character has signature weapon mentioned
        weapon_keywords = ["sword", "staff", "bow", "dagger", "axe", "hammer", "spear", "wand"]
        
        for keyword in weapon_keywords:
            if keyword in combat_style.lower() or keyword in class_abilities.lower():
                print(f"  ✓ Processing: {character_name}'s {keyword.title()}")
                
                # Build weapon description
                weapon_description = f"{character_name}'s signature {keyword}. {combat_style[:100]}"
                
                # Determine materials based on character type
                char_type = char.get("character_type", "")
                if "mage" in char_type.lower() or "wizard" in char_type.lower():
                    materials = "enchanted wood, mystical crystals"
                    special_props = ["magical glow", "arcane runes"]
                elif "warrior" in char_type.lower() or "knight" in char_type.lower():
                    materials = "forged steel, leather grip"
                    special_props = ["battle-worn", "masterwork craftsmanship"]
                else:
                    materials = "fine crafted materials"
                    special_props = ["expert quality"]
                
                prompts = PromptEngineeringService.build_item_prompt(
                    item_name=f"{character_name}'s {keyword.title()}",
                    item_type=keyword.title(),
                    description=weapon_description,
                    materials=materials,
                    art_style=art_style,
                    special_properties=special_props,
                    scale_reference="weapon size",
                    quality_preset=quality_preset
                )
                
                item_prompt = {
                    "id": f"{character_name.lower().replace(' ', '_')}_{keyword}",
                    "name": f"{character_name}'s {keyword.title()}",
                    "type": keyword.title(),
                    "positive_prompt": prompts["positive_prompt"],
                    "negative_prompt": prompts["negative_prompt"],
                    "original_description": weapon_description,
                    "metadata": {
                        "item_type": keyword.title(),
                        "art_style": art_style,
                        "quality_preset": quality_preset_name,
                        "owner": character_name,
                        "combat_style": combat_style
                    }
                }
                
                item_prompts.append(item_prompt)
                break  # Only extract one weapon per character
    
    print(f"✓ Generated {len(item_prompts)} item prompts")
    
    return {"item_prompts": item_prompts}

