"""World lore model for fictional universe generation."""
from pydantic import BaseModel, Field


class WorldLore(BaseModel):
    """Structured world lore document for fictional universes."""
    world_name: str = Field(description="Evocative name for this world or realm.")
    setting_overview: str = Field(description="High-level description: genre, tone, and core concept.")
    
    # Physical World
    geography: str = Field(description="Major continents, regions, terrain, natural barriers, landmarks.")
    climate_cosmology: str = Field(description="Climate zones, celestial bodies, astronomical phenomena.")
    flora_fauna: str = Field(description="Unique creatures, ecosystems, magical beasts, sentient species.")
    
    # History & Timeline
    creation_myth: str = Field(description="Origin story: how the world came to be, creation deities.")
    historical_eras: str = Field(description="Major historical periods, wars, golden ages, cataclysms.")
    current_age: str = Field(description="Present era setting: what's happening now, recent events.")
    
    # Cultural & Social
    civilizations: str = Field(description="Major nations, empires, tribes, city-states and their cultures.")
    social_structures: str = Field(description="Class systems, governance, power distribution, hierarchies.")
    religions_beliefs: str = Field(description="Pantheons, religious systems, spiritual practices, taboos.")
    
    # Systems & Mechanics
    magic_or_technology: str = Field(description="Magic system OR tech level: rules, limitations, accessibility.")
    economy_resources: str = Field(description="Currency, trade, valuable resources, economic systems.")
    conflicts_tensions: str = Field(description="Current wars, political tensions, faction rivalries.")
    
    # Narrative Hooks
    mysteries_legends: str = Field(description="Unsolved mysteries, lost artifacts, legendary locations.")
    story_potential: str = Field(description="Key narrative opportunities and dramatic possibilities.")
    
    class Config:
        """Pydantic config."""
        extra = "allow"
