"""Models for RenderPrep visual asset generation."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CharacterVisualPrompt(BaseModel):
    """Structured prompt for character sheet generation via Veo/Genie."""
    character_id: str = Field(description="Unique identifier for the character")
    character_name: str = Field(description="Character name")
    character_type: str = Field(description="Protagonist, Companion, NPC, etc.")
    visual_description: str = Field(description="Detailed visual appearance for generation")
    art_style: str = Field(description="Art style matching the game aesthetic")
    pose_reference: str = Field(description="Suggested pose or stance for character sheet")
    color_palette: str = Field(description="Primary and secondary colors")
    generation_prompt: str = Field(description="Complete prompt ready for Veo/Genie")
    tags: List[str] = Field(default=[], description="Additional metadata tags")


class EnvironmentPrompt(BaseModel):
    """Structured prompt for environment/location visualization."""
    location_id: str = Field(description="Unique identifier for the location")
    location_name: str = Field(description="Name of the location")
    location_type: str = Field(description="Headquarters, Dungeon, Town, etc.")
    visual_description: str = Field(description="Detailed location appearance")
    atmosphere: str = Field(description="Mood and lighting description")
    key_features: List[str] = Field(description="Notable architectural/design elements")
    art_style: str = Field(description="Art style matching the game aesthetic")
    generation_prompt: str = Field(description="Complete prompt ready for Veo/Genie")
    tags: List[str] = Field(default=[], description="Additional metadata tags")


class ItemPrompt(BaseModel):
    """Structured prompt for item/equipment visualization."""
    item_id: str = Field(description="Unique identifier for the item")
    item_name: str = Field(description="Name of the item")
    item_type: str = Field(description="Weapon, Armor, Artifact, etc.")
    visual_description: str = Field(description="Detailed item appearance")
    materials: str = Field(description="Material composition and texture")
    special_properties: List[str] = Field(description="Magical/special visual effects")
    scale_reference: str = Field(description="Size relative to human hand/body")
    art_style: str = Field(description="Art style matching the game aesthetic")
    generation_prompt: str = Field(description="Complete prompt ready for Veo/Genie")
    tags: List[str] = Field(default=[], description="Additional metadata tags")


class StoryboardFrame(BaseModel):
    """Structured prompt for storyboard/key art generation."""
    frame_id: str = Field(description="Unique identifier for this storyboard frame")
    scene_name: str = Field(description="Name of the story scene")
    sequence_number: int = Field(description="Order in the narrative sequence")
    visual_composition: str = Field(description="Framing, camera angle, and composition")
    key_elements: List[str] = Field(description="Characters, objects, and environmental elements to include")
    narrative_context: str = Field(description="What's happening narratively in this frame")
    mood_tone: str = Field(description="Emotional tone and atmosphere")
    color_palette: str = Field(description="Color scheme for visual cohesion")
    generation_prompt: str = Field(description="Complete prompt ready for Veo/Genie")
    related_characters: List[str] = Field(default=[], description="Character IDs in this frame")
    related_locations: List[str] = Field(default=[], description="Location IDs in this frame")
    tags: List[str] = Field(default=[], description="Additional metadata tags")


class RenderPrepOutput(BaseModel):
    """Complete render prep output with all visual assets."""
    timestamp: str = Field(description="Generation timestamp")
    concept_id: Optional[str] = Field(description="Associated concept document ID")
    characters: List[CharacterVisualPrompt] = Field(default=[], description="Generated character prompts")
    environments: List[EnvironmentPrompt] = Field(default=[], description="Generated location prompts")
    items: List[ItemPrompt] = Field(default=[], description="Generated item prompts")
    storyboards: List[StoryboardFrame] = Field(default=[], description="Generated storyboard frames")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")
    
    class Config:
        """Pydantic config."""
        extra = "allow"
