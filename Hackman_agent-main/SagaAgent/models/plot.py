"""Plot arc model for video game narrative structure."""
from pydantic import BaseModel, Field


class PlotArc(BaseModel):
    """Structured plot arc document for video games with branching narrative support."""
    
    # Core Structure
    arc_title: str = Field(description="Memorable name for this story arc or campaign.")
    arc_type: str = Field(description="Main Quest, Faction Quest, Character Arc, Side Quest, DLC Campaign.")
    central_question: str = Field(description="The driving question players seek to answer: 'Can the hero defeat X?', 'Will Y betray us?'")
    theme: str = Field(description="Core theme explored: redemption, corruption, sacrifice, identity, power, etc.")
    estimated_playtime: str = Field(description="Expected completion time: 2-4 hours, 10-15 hours, etc.")
    
    # Act 1 - Setup (Tutorial/Introduction)
    act1_hook: str = Field(description="Opening moments that grab player attention immediately through action or mystery.")
    act1_worldbuilding: str = Field(description="Introduce setting, factions, key NPCs, and primary conflict in first act.")
    act1_tutorial: str = Field(description="Core gameplay mechanics introduced naturally through narrative context.")
    inciting_incident: str = Field(description="Event that disrupts status quo and forces player into the main conflict.")
    act1_player_goal: str = Field(description="What player is trying to achieve by end of Act 1, first major objective.")
    plot_point_1: str = Field(description="Decision/event that commits player to the journey, point of no return.")
    
    # Act 2 - Confrontation (Rising Action)
    act2_progression: str = Field(description="Series of challenges that escalate in difficulty and narrative stakes.")
    act2_complications: str = Field(description="New obstacles, betrayals, revelations that complicate the mission.")
    midpoint_twist: str = Field(description="Major revelation that recontextualizes everything, raises stakes dramatically.")
    act2_setbacks: str = Field(description="Failures, losses, defeats that push protagonist to lowest point.")
    companion_development: str = Field(description="How companion relationships evolve, loyalty tests, personal quests unlocked.")
    plot_point_2: str = Field(description="Crisis moment that forces final confrontation, all-or-nothing decision.")
    
    # Act 3 - Resolution (Climax)
    act3_final_prep: str = Field(description="Gathering allies, final upgrades, calm before storm, point-of-no-return warning.")
    climax_sequence: str = Field(description="Multi-stage final battle/confrontation with escalating intensity.")
    boss_mechanics: str = Field(description="Final boss phases, mechanics that test all learned skills.")
    resolution: str = Field(description="Immediate aftermath, fate of key characters, world state changes.")
    epilogue: str = Field(description="Long-term consequences, what happens to world/characters post-victory.")
    
    # Branching Narrative System
    major_choice_points: str = Field(description="3-5 critical decisions that branch the narrative into different paths.")
    choice_consequences: str = Field(description="How each major choice affects story, character fates, available endings.")
    conditional_content: str = Field(description="Story segments that only appear based on previous choices or faction allegiance.")
    multiple_endings: str = Field(description="Distinct endings based on player choices: 3-5 variations with different world states.")
    
    class Config:
        """Pydantic config."""
        extra = "allow"
