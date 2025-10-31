"""Faction model for video game faction generation."""
from pydantic import BaseModel, Field


class GameFaction(BaseModel):
    """Structured faction document for video games with gameplay mechanics."""
    
    # Core Identity
    faction_name: str = Field(description="Memorable name with in-world significance.")
    motto_tagline: str = Field(description="Catchphrase that defines their philosophy and appears in UI.")
    faction_type: str = Field(description="Classification: Guild, Military, Religious, Criminal, Corporate, Tribal, etc.")
    core_ideology: str = Field(description="Central beliefs and worldview that drives their actions.")
    aesthetic_identity: str = Field(description="Visual style, color palette, architecture, fashion, symbolism.")
    
    # Leadership & Structure
    leader_profile: str = Field(description="Main leader(s): name, personality, background, player interaction potential.")
    hierarchy: str = Field(description="Rank system from initiate to master, progression path.")
    notable_npcs: str = Field(description="Key characters: questgivers, merchants, trainers, rivals, romance options.")
    organizational_culture: str = Field(description="Internal culture, rituals, code of conduct, member treatment.")
    
    # Territory & Power
    headquarters: str = Field(description="Main base location, appearance, facilities, fast travel points.")
    controlled_regions: str = Field(description="Territory, outposts, influence zones, contested areas.")
    military_strength: str = Field(description="Troop types, combat style, special units, tactical advantages.")
    economic_power: str = Field(description="Wealth sources, trade networks, unique goods, economic influence.")
    
    # Gameplay Integration
    joining_requirements: str = Field(description="How players join: quests, skill checks, reputation threshold, moral choices.")
    reputation_system: str = Field(description="Reputation tiers (Hostile→Neutral→Friendly→Honored→Exalted), rewards per tier.")
    exclusive_benefits: str = Field(description="Member-only rewards: unique gear, abilities, merchants, quests, housing.")
    rank_progression: str = Field(description="Advancement quests, rank-up requirements, titles, responsibilities.")
    
    # Quest & Mission Design
    faction_questline: str = Field(description="Main story arc: 5-8 major quests with branching outcomes.")
    repeatable_activities: str = Field(description="Daily/weekly missions, bounties, reputation grinds, radiant quests.")
    moral_dilemmas: str = Field(description="Ethical choices that test player loyalty and affect reputation.")
    betrayal_consequences: str = Field(description="What happens if player betrays faction or joins rivals.")
    
    # Relations & Conflict
    allied_factions: str = Field(description="Friendly groups, shared quests, joint reputation benefits.")
    rival_factions: str = Field(description="Enemy groups, mutually exclusive memberships, conflict zones.")
    neutral_factions: str = Field(description="Groups with complex/conditional relationships.")
    faction_war_mechanics: str = Field(description="How faction conflicts play out in gameplay, territory battles, dynamic events.")
    
    class Config:
        """Pydantic config."""
        extra = "allow"
