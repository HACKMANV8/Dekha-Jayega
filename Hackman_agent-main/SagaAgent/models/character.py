"""Character model for video game character generation."""
from pydantic import BaseModel, Field


class GameCharacter(BaseModel):
    """Structured character document for video games with gameplay mechanics."""
    
    # Core Identity
    character_name: str = Field(description="Memorable name with cultural/thematic significance.")
    character_type: str = Field(description="Protagonist, Companion, Quest NPC, Merchant, Boss, Romance Option, etc.")
    role_purpose: str = Field(description="Narrative function: mentor, rival, comic relief, betrayer, love interest.")
    tagline_quote: str = Field(description="Signature catchphrase or memorable quote that defines them.")
    
    # Visual Design
    appearance: str = Field(description="Detailed physical description: build, height, age, distinctive features, scars, tattoos.")
    silhouette_design: str = Field(description="Instantly recognizable silhouette elements for visual identification.")
    costume_design: str = Field(description="Clothing, armor, accessories, color palette, cultural influences.")
    visual_themes: str = Field(description="Symbolic elements, motifs, color psychology, visual storytelling.")
    
    # Personality & Psychology
    personality_traits: str = Field(description="Core traits using Big Five or similar: openness, conscientiousness, extraversion, agreeableness, neuroticism.")
    motivations: str = Field(description="What drives them: desires, fears, needs, ambitions, internal conflicts.")
    moral_alignment: str = Field(description="Ethical stance: lawful/chaotic, good/evil, or custom alignment system.")
    character_arc: str = Field(description="How they change throughout the story: growth, fall, redemption, corruption.")
    quirks_mannerisms: str = Field(description="Unique behaviors, speech patterns, gestures, habits that make them memorable.")
    
    # Background & History
    backstory: str = Field(description="Origin, upbringing, formative events, traumas, achievements, losses.")
    relationships: str = Field(description="Connections to other characters, factions, family, mentors, rivals.")
    secrets_reveals: str = Field(description="Hidden truths revealed through gameplay, plot twists, betrayals.")
    
    # Gameplay Mechanics
    combat_style: str = Field(description="Fighting approach: melee/ranged, aggressive/defensive, weapon types, signature moves.")
    class_abilities: str = Field(description="Special powers, skill trees, unique mechanics they introduce.")
    stats_attributes: str = Field(description="Numerical stats: STR/DEX/INT/etc., HP, mana, resistances, weaknesses.")
    playstyle_identity: str = Field(description="How playing as/with this character feels different mechanically.")
    
    # Player Interaction
    recruitment_conditions: str = Field(description="How player obtains/recruits them: quests, choices, skill checks, faction requirements.")
    dialogue_system: str = Field(description="Conversation trees, persuasion checks, relationship-building mechanics.")
    companion_mechanics: str = Field(description="If companion: commands, tactics, combo moves, loyalty system.")
    romance_friendship: str = Field(description="Relationship progression: gifts, dialogue choices, romance quests, breakup possibilities.")
    
    class Config:
        """Pydantic config."""
        extra = "allow"
