"""Questline model for video game quest design."""
from pydantic import BaseModel, Field


class Questline(BaseModel):
    """Structured questline document for video games with branching objectives."""
    
    # Core Identity
    quest_name: str = Field(description="Memorable, evocative quest name that hints at content.")
    quest_type: str = Field(description="Main Quest, Side Quest, Faction Quest, Companion Quest, Radiant/Repeatable, Daily/Weekly.")
    difficulty: str = Field(description="Easy/Medium/Hard/Elite, recommended level/power range.")
    estimated_time: str = Field(description="Expected completion time: 10 mins, 30 mins, 1-2 hours, etc.")
    
    # Hook & Discovery
    discovery_method: str = Field(description="How players find quest: NPC approach, notice board, exploration, overhearing, item pickup.")
    quest_giver: str = Field(description="Who gives quest: NPC name, personality, relationship to player, location.")
    hook_pitch: str = Field(description="The compelling pitch: what's at stake, why player should care, immediate intrigue.")
    urgency_factor: str = Field(description="Time pressure: timed quest, failing other quests, NPC in danger, optional urgency.")
    
    # Objectives Structure
    primary_objectives: str = Field(description="Main objectives in order: numbered list with clear verbs (Retrieve X, Escort Y, Defeat Z).")
    optional_objectives: str = Field(description="Bonus goals for extra rewards: collectibles, alternate solutions, challenge modes.")
    nested_objectives: str = Field(description="Sub-tasks breaking large goals into manageable chunks with progress tracking.")
    failure_conditions: str = Field(description="What causes quest failure: NPC death, time expiry, detected by guards, item destroyed.")
    
    # Branching Paths
    choice_points: str = Field(description="Decisions that branch quest into different paths: 2-3 major choices with distinct outcomes.")
    path_outcomes: str = Field(description="Different quest resolutions based on player choices, each with unique rewards/consequences.")
    skill_checks: str = Field(description="Optional skill-based shortcuts: persuasion, lockpicking, hacking, stealth, intimidation.")
    faction_variations: str = Field(description="How quest changes based on player's faction allegiance or reputation.")
    
    # Gameplay Integration
    mechanics_introduced: str = Field(description="New gameplay mechanics this quest teaches or tests.")
    combat_encounters: str = Field(description="Enemy types, difficulty spikes, boss fights, optional stealth/pacifist routes.")
    puzzle_elements: str = Field(description="Logic puzzles, environmental puzzles, riddles, investigation/detective work.")
    exploration_required: str = Field(description="Areas to explore, hidden locations, environmental clues, collectibles to find.")
    
    # Narrative Elements
    story_beats: str = Field(description="Key narrative moments: betrayals, reveals, emotional peaks, character development.")
    npc_interactions: str = Field(description="Significant character moments, relationship changes, approval/disapproval impacts.")
    environmental_storytelling: str = Field(description="Story told through environment: notes, corpses, destroyed areas, visual clues.")
    lore_reveals: str = Field(description="World lore discovered through quest: history, faction secrets, character backstories.")
    
    # Rewards & Progression
    reward_structure: str = Field(description="Experience points, currency, unique items, perks unlocked, ability progression.")
    reputation_changes: str = Field(description="Faction reputation gains/losses, NPC relationship changes, title unlocks.")
    unlocks_consequences: str = Field(description="Quests/areas/NPCs unlocked by completion, permanent world changes, trade routes, vendors.")
    
    class Config:
        """Pydantic config."""
        extra = "allow"
