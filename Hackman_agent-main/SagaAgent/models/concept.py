"""Concept model for game concept generation."""
from pydantic import BaseModel, Field


class ConceptDoc(BaseModel):
    """Structured video game concept document."""
    title: str = Field(description="A catchy working title for the game.")
    genre: str = Field(description="Primary and sub-genres, e.g., 'Action RPG, Roguelite'.")
    elevator_pitch: str = Field(description="1-2 sentence pitch capturing the essence and hook.")
    core_loop: str = Field(description="Bullet-style description of what players repeatedly do.")
    key_mechanics: str = Field(description="Key mechanics and systems that define gameplay.")
    progression: str = Field(description="How players progress: meta, unlocks, difficulty, story.")
    world_setting: str = Field(description="Setting, tone, and brief world lore.")
    art_style: str = Field(description="Art direction references and visual style notes.")
    target_audience: str = Field(description="Intended players and platforms.")
    monetization: str = Field(description="Premium/Free-to-Play model and ethical considerations.")
    usp: str = Field(description="Unique Selling Proposition: what makes this stand out.")
    
    class Config:
        """Pydantic config."""
        extra = "allow"
