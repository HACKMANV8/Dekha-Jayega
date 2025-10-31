# Video Game Faction Agent - LangGraph Workflow
from typing import TypedDict, Literal
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

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
    
    # Player Choice Impact
    multiple_endings: str = Field(description="How faction choice affects endgame, world state, available endings.")
    companion_reactions: str = Field(description="How companions approve/disapprove of faction membership.")
    world_consequences: str = Field(description="How faction victory/defeat changes the game world visually and mechanically.")
    
    # Unique Mechanics
    signature_gameplay: str = Field(description="Unique mechanics this faction introduces: stealth missions, naval combat, diplomacy, etc.")
    faction_abilities: str = Field(description="Special powers, skill trees, or perks exclusive to members.")
    endgame_content: str = Field(description="Post-main-quest content: raids, PvP, territory control, faction wars.")

class FactionReview(BaseModel):
    """Evaluator review for video game faction."""
    decision: Literal["accept", "revise"] = Field(
        description="Accept if faction has clear gameplay identity, compelling questlines, and meaningful player choice; otherwise revise."
    )
    feedback: str = Field(description="Specific improvements: weak mechanics, generic quests, unclear progression, missing player agency.")

class FactionState(TypedDict):
    faction_prompt: str
    game_genre: str  # RPG, Strategy, MMO, etc.
    world_context: str  # Optional world lore
    faction_md: str
    feedback: str
    decision: str

# Prepare evaluator
evaluator = llm.with_structured_output(FactionReview, method="json_schema")

def generate_faction(state: FactionState):
    """Generate faction with deep gameplay integration."""
    faction_prompt = state["faction_prompt"]
    game_genre = state.get("game_genre", "Action RPG")
    world_context = state.get("world_context", "")
    
    guidance = (
        f"You are a veteran game designer specializing in {game_genre}. "
        f"Create a fully playable faction based on: '{faction_prompt}'. "
        "CRITICAL: Focus on gameplay mechanics, not just lore. "
        "Make joining feel earned. Create 5-8 memorable quests with branching choices. "
        "Ensure faction membership meaningfully changes how the player experiences the game. "
        "Design conflicts that force difficult moral choices. "
        "Give specific, implementable mechanics—not vague descriptions."
    )
    
    if world_context:
        guidance += f"\n\nWorld Context: {world_context}"
    
    if state.get("feedback"):
        guidance += f"\n\nIMPORTANT - Address this feedback: {state['feedback']}"
    
    schema = llm.with_structured_output(GameFaction, method="json_schema")
    faction = schema.invoke(guidance)
    
    md = (
        f"# {faction.faction_name}\n\n"
        f"**\"{faction.motto_tagline}\"**\n\n"
        f"**Type**: {faction.faction_type}\n\n"
        f"---\n\n"
        f"## Identity & Aesthetic\n\n"
        f"### Core Ideology\n{faction.core_ideology}\n\n"
        f"### Visual Identity\n{faction.aesthetic_identity}\n\n"
        f"---\n\n"
        f"## Leadership & Key NPCs\n\n"
        f"### Faction Leader\n{faction.leader_profile}\n\n"
        f"### Hierarchy & Ranks\n{faction.hierarchy}\n\n"
        f"### Notable NPCs\n{faction.notable_npcs}\n\n"
        f"### Organizational Culture\n{faction.organizational_culture}\n\n"
        f"---\n\n"
        f"## Territory & Power\n\n"
        f"### Headquarters\n{faction.headquarters}\n\n"
        f"### Controlled Regions\n{faction.controlled_regions}\n\n"
        f"### Military Strength\n{faction.military_strength}\n\n"
        f"### Economic Power\n{faction.economic_power}\n\n"
        f"---\n\n"
        f"## Gameplay Mechanics\n\n"
        f"### Joining the Faction\n{faction.joining_requirements}\n\n"
        f"### Reputation System\n{faction.reputation_system}\n\n"
        f"### Member Benefits\n{faction.exclusive_benefits}\n\n"
        f"### Rank Progression\n{faction.rank_progression}\n\n"
        f"---\n\n"
        f"## Quests & Content\n\n"
        f"### Main Questline\n{faction.faction_questline}\n\n"
        f"### Repeatable Activities\n{faction.repeatable_activities}\n\n"
        f"### Moral Dilemmas\n{faction.moral_dilemmas}\n\n"
        f"### Betrayal & Consequences\n{faction.betrayal_consequences}\n\n"
        f"---\n\n"
        f"## Faction Relations\n\n"
        f"### Allied Factions\n{faction.allied_factions}\n\n"
        f"### Rival Factions\n{faction.rival_factions}\n\n"
        f"### Neutral Factions\n{faction.neutral_factions}\n\n"
        f"### Faction War Mechanics\n{faction.faction_war_mechanics}\n\n"
        f"---\n\n"
        f"## Player Choice & Consequences\n\n"
        f"### Multiple Endings\n{faction.multiple_endings}\n\n"
        f"### Companion Reactions\n{faction.companion_reactions}\n\n"
        f"### World Consequences\n{faction.world_consequences}\n\n"
        f"---\n\n"
        f"## Unique Features\n\n"
        f"### Signature Gameplay\n{faction.signature_gameplay}\n\n"
        f"### Faction Abilities\n{faction.faction_abilities}\n\n"
        f"### Endgame Content\n{faction.endgame_content}\n"
    )
    
    return {"faction_md": md}

def evaluate_faction(state: FactionState):
    """Evaluate faction for gameplay depth and player agency."""
    faction_md = state["faction_md"]
    game_genre = state.get("game_genre", "Action RPG")
    
    rubric = (
        f"Evaluate this {game_genre} faction for:\n\n"
        "1. **Gameplay Identity**: Does it offer unique mechanics/playstyle vs generic content?\n"
        "2. **Meaningful Choice**: Does joining have consequences? Are there moral dilemmas?\n"
        "3. **Progression System**: Clear rank-up path? Satisfying rewards per tier?\n"
        "4. **Quest Quality**: Specific questlines with branching outcomes vs generic fetch quests?\n"
        "5. **Faction Conflicts**: Compelling rivalries? Mutually exclusive choices?\n"
        "6. **Player Agency**: Can player betray/leave? Multiple faction endings?\n"
        "7. **Mechanical Depth**: Concrete systems (reputation numbers, unique abilities) vs vague descriptions?\n\n"
        "Accept only if faction significantly changes how the game is played. "
        "Reject generic 'join→do quests→get rewards' structures without unique hooks."
    )
    
    review = evaluator.invoke(f"{rubric}\n\nFACTION:\n{faction_md}")
    return {"decision": review.decision, "feedback": review.feedback}

def route_faction(state: FactionState):
    """Route to finish on accept; loop back with feedback to revise."""
    if state["decision"] == "accept":
        return "Accepted"
    else:
        return "Revise"

# Build workflow
builder = StateGraph(FactionState)
builder.add_node("generate_faction", generate_faction)
builder.add_node("evaluate_faction", evaluate_faction)
builder.add_edge(START, "generate_faction")
builder.add_edge("generate_faction", "evaluate_faction")
builder.add_conditional_edges(
    "evaluate_faction",
    route_faction,
    {
        "Accepted": END,
        "Revise": "generate_faction",
    },
)

faction_workflow = builder.compile()

# Example invocations
if __name__ == "__main__":
    # Example 1: Dark Brotherhood-style assassin guild
    result1 = faction_workflow.invoke({
        "faction_prompt": "Secret assassin guild that worships death itself",
        "game_genre": "Open-world RPG",
        "world_context": "Medieval fantasy with dark magic and political intrigue"
    })
    print(result1["faction_md"])
    print("\n" + "="*80 + "\n")
    
    # Example 2: Sci-fi corporate faction
    result2 = faction_workflow.invoke({
        "faction_prompt": "Mega-corporation controlling interstellar trade routes",
        "game_genre": "Space RPG",
        "world_context": "Post-Earth humanity scattered across star systems"
    })
    print(result2["faction_md"])
    
    # Example 3: Strategy game faction
    result3 = faction_workflow.invoke({
        "faction_prompt": "Nomadic desert tribes with sand-manipulation magic",
        "game_genre": "4X Strategy",
        "world_context": "Desert planet with scarce water resources"
    })
    print(result3["faction_md"])
