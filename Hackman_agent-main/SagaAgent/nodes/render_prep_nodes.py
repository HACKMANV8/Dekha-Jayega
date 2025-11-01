"""RenderPrep nodes for converting narrative to visual asset prompts."""
from typing import Dict, Any
from datetime import datetime
from SagaAgent.models.render_prep import (
    CharacterVisualPrompt,
    EnvironmentPrompt,
    ItemPrompt,
    StoryboardFrame,
    RenderPrepOutput
)
from SagaAgent.utils.state import SagaState


def prepare_characters_node(state: SagaState) -> Dict[str, Any]:
    """Convert game characters to visual generation prompts."""
    characters = state.get("characters", [])
    concept = state.get("concept", {})
    
    char_prompts = []
    for char in characters:
        prompt = CharacterVisualPrompt(
            character_id=char.get('character_name', 'unknown').lower().replace(' ', '_'),
            character_name=char.get('character_name', 'Unknown'),
            character_type=char.get('character_type', 'NPC'),
            visual_description=char.get('appearance', ''),
            art_style=concept.get('art_style', 'Fantasy'),
            pose_reference=char.get('silhouette_design', 'Standing pose'),
            color_palette=f"{char.get('visual_themes', '')}",
            generation_prompt=f"Create character art for {char.get('character_name')}: {char.get('appearance')}",
            tags=['character', 'concept_art']
        )
        char_prompts.append(prompt)
    
    return {
        "character_prompts": [p.model_dump() for p in char_prompts]
    }


def prepare_locations_node(state: SagaState) -> Dict[str, Any]:
    """Convert world lore locations to visual generation prompts."""
    world_lore = state.get("world_lore", {})
    concept = state.get("concept", {})
    
    loc_prompts = []
    
    # Extract major locations from lore
    locations_info = [
        {
            "name": world_lore.get('world_name', 'Unknown World'),
            "type": "World Overview",
            "description": world_lore.get('geography', '')
        },
        {
            "name": "Major Settlement",
            "type": "City",
            "description": world_lore.get('civilizations', '')
        }
    ]
    
    for loc in locations_info:
        prompt = EnvironmentPrompt(
            location_id=loc['name'].lower().replace(' ', '_'),
            location_name=loc['name'],
            location_type=loc['type'],
            visual_description=loc['description'][:500],
            atmosphere=world_lore.get('setting_overview', 'Epic and immersive'),
            key_features=[world_lore.get('magic_or_technology', 'Magic system')],
            art_style=concept.get('art_style', 'Fantasy'),
            generation_prompt=f"Create environment art for {loc['name']}: {loc['description'][:200]}",
            tags=['location', 'environment', 'concept_art']
        )
        loc_prompts.append(prompt)
    
    return {
        "location_prompts": [p.model_dump() for p in loc_prompts]
    }


def prepare_items_node(state: SagaState) -> Dict[str, Any]:
    """Convert quest/plot artifacts to visual generation prompts."""
    plot_arcs = state.get("plot_arcs", [])
    concept = state.get("concept", {})
    
    item_prompts = []
    
    # Extract key artifacts from plot arcs
    if plot_arcs:
        plot = plot_arcs[0]
        items_info = [
            {
                "name": "Quest Artifact",
                "type": "Magical Item",
                "description": plot.get('central_question', 'Important quest item')
            }
        ]
        
        for item in items_info:
            prompt = ItemPrompt(
                item_id=item['name'].lower().replace(' ', '_'),
                item_name=item['name'],
                item_type=item['type'],
                visual_description=item['description'],
                materials="Magical materials",
                special_properties=["Glows with power"],
                scale_reference="Hand-held",
                art_style=concept.get('art_style', 'Fantasy'),
                generation_prompt=f"Create item art for {item['name']}: {item['description']}",
                tags=['item', 'artifact', 'concept_art']
            )
            item_prompts.append(prompt)
    
    return {
        "item_prompts": [p.model_dump() for p in item_prompts]
    }


def assemble_storyboards_node(state: SagaState) -> Dict[str, Any]:
    """Convert plot arcs to storyboard frame prompts."""
    plot_arcs = state.get("plot_arcs", [])
    characters = state.get("characters", [])
    world_lore = state.get("world_lore", {})
    concept = state.get("concept", {})
    
    storyboard_prompts = []
    
    for idx, plot in enumerate(plot_arcs):
        # Create storyboard frames for major plot points
        frames_info = [
            {
                "name": "Act 1 Hook",
                "description": plot.get('act1_hook', 'Opening scene'),
                "seq": 1
            },
            {
                "name": "Climax",
                "description": plot.get('climax_sequence', 'Final battle'),
                "seq": 2
            },
            {
                "name": "Resolution",
                "description": plot.get('epilogue', 'Story ending'),
                "seq": 3
            }
        ]
        
        for frame in frames_info:
            char_ids = [c.get('character_name', '').lower().replace(' ', '_') for c in characters[:2]]
            prompt = StoryboardFrame(
                frame_id=f"plot{idx}_frame{frame['seq']}",
                scene_name=frame['name'],
                sequence_number=frame['seq'],
                visual_composition=f"Cinematic composition for {frame['name']}",
                key_elements=frame['description'].split()[:5],
                narrative_context=frame['description'],
                mood_tone="Epic and dramatic",
                color_palette=concept.get('art_style', 'Vibrant'),
                generation_prompt=f"Create storyboard art for: {frame['description']}",
                related_characters=char_ids,
                related_locations=[world_lore.get('world_name', 'unknown').lower().replace(' ', '_')],
                tags=['storyboard', 'key_art', 'concept_art']
            )
            storyboard_prompts.append(prompt)
    
    return {
        "storyboard_prompts": [p.model_dump() for p in storyboard_prompts]
    }
