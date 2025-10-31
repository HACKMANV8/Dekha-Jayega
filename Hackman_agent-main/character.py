# Video Game Character Agent - LangGraph Workflow
from typing import TypedDict, Literal
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

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
    
    # Quest Integration
    personal_questline: str = Field(description="Character-specific story arc: 3-5 quests exploring their backstory and growth.")
    side_activities: str = Field(description="Optional interactions: banter, camp conversations, mini-games, training sessions.")
    branching_outcomes: str = Field(description="How player choices affect character's fate: death, betrayal, redemption, ascension.")
    
    # Dynamic Behavior
    approval_system: str = Field(description="What actions increase/decrease their approval of the player, thresholds for consequences.")
    contextual_reactions: str = Field(description="How they react to story events, player choices, faction allegiances, moral decisions.")
    leaving_conditions: str = Field(description="Circumstances that cause them to leave the party or turn hostile.")
    
    # Voice & Dialogue
    voice_direction: str = Field(description="Voice type, accent, tone, pacing, emotional range for voice actors.")
    dialogue_examples: str = Field(description="5-6 sample lines showing personality: greeting, combat, approval, disapproval, romance, betrayal.")
    
    # For NPCs/Bosses
    ai_behavior: str = Field(description="Combat AI patterns, tactics, phase transitions, attack telegraphs.")
    loot_rewards: str = Field(description="Drops, unique items, achievements, story unlocks from defeating/helping them.")
    
    # Integration Notes
    thematic_resonance: str = Field(description="How character reflects game's themes, serves as foil to protagonist, or symbolizes concepts.")
    player_impact: str = Field(description="How character meaningfully changes player experience vs being cosmetic addition.")

class CharacterReview(BaseModel):
    """Evaluator review for video game character."""
    decision: Literal["accept", "revise"] = Field(
        description="Accept if character has distinct personality, clear gameplay identity, and compelling arc; otherwise revise."
    )
    feedback: str = Field(description="Specific improvements: flat personality, generic design, weak mechanics, unclear purpose.")

class CharacterState(TypedDict):
    character_prompt: str
    character_type: str  # "playable", "companion", "npc", "boss"
    game_context: str  # Genre, setting, faction
    character_md: str
    feedback: str
    decision: str

# Prepare evaluator
evaluator = llm.with_structured_output(CharacterReview, method="json_schema")

def generate_character(state: CharacterState):
    """Generate character with personality depth and gameplay integration."""
    character_prompt = state["character_prompt"]
    character_type = state.get("character_type", "companion")
    game_context = state.get("game_context", "")
    
    guidance = (
        f"You are an expert character designer and narrative director. "
        f"Create a {character_type} character based on: '{character_prompt}'. "
        "CRITICAL RULES:\n"
        "- Create a DISTINCT personality with contradictions and depth, not flat archetypes\n"
        "- Design recognizable silhouette elements for instant visual identification\n"
        "- Give them a clear character arc showing growth or transformation\n"
        "- Ensure gameplay mechanics match personality (aggressive fighter = aggressive personality)\n"
        "- Include 5-6 sample dialogue lines demonstrating voice and personality\n"
        "- Make approval system reflect their values, not generic 'good/evil' choices\n"
        "- Create branching outcomes where player choices genuinely affect their fate\n"
        "- Avoid clichés: give unexpected combinations of traits\n"
        "- Make backstory reveal gradually through gameplay, not exposition dumps"
    )
    
    if game_context:
        guidance += f"\n\nGame Context: {game_context}"
    
    if state.get("feedback"):
        guidance += f"\n\nIMPORTANT - Address this feedback: {state['feedback']}"
    
    schema = llm.with_structured_output(GameCharacter, method="json_schema")
    character = schema.invoke(guidance)
    
    md = (
        f"# {character.character_name}\n\n"
        f"**\"{character.tagline_quote}\"**\n\n"
        f"**Type**: {character.character_type} | **Role**: {character.role_purpose}\n\n"
        f"---\n\n"
        f"## Visual Design\n\n"
        f"### Appearance\n{character.appearance}\n\n"
        f"### Silhouette Design\n{character.silhouette_design}\n\n"
        f"### Costume & Style\n{character.costume_design}\n\n"
        f"### Visual Themes\n{character.visual_themes}\n\n"
        f"---\n\n"
        f"## Personality & Psychology\n\n"
        f"### Core Traits\n{character.personality_traits}\n\n"
        f"### Motivations\n{character.motivations}\n\n"
        f"### Moral Alignment\n{character.moral_alignment}\n\n"
        f"### Character Arc\n{character.character_arc}\n\n"
        f"### Quirks & Mannerisms\n{character.quirks_mannerisms}\n\n"
        f"---\n\n"
        f"## Background\n\n"
        f"### Backstory\n{character.backstory}\n\n"
        f"### Relationships\n{character.relationships}\n\n"
        f"### Secrets & Reveals\n{character.secrets_reveals}\n\n"
        f"---\n\n"
        f"## Gameplay Mechanics\n\n"
        f"### Combat Style\n{character.combat_style}\n\n"
        f"### Abilities & Powers\n{character.class_abilities}\n\n"
        f"### Stats & Attributes\n{character.stats_attributes}\n\n"
        f"### Playstyle Identity\n{character.playstyle_identity}\n\n"
        f"---\n\n"
        f"## Player Interaction\n\n"
        f"### Recruitment\n{character.recruitment_conditions}\n\n"
        f"### Dialogue System\n{character.dialogue_system}\n\n"
        f"### Companion Mechanics\n{character.companion_mechanics}\n\n"
        f"### Romance & Friendship\n{character.romance_friendship}\n\n"
        f"---\n\n"
        f"## Quest Content\n\n"
        f"### Personal Questline\n{character.personal_questline}\n\n"
        f"### Side Activities\n{character.side_activities}\n\n"
        f"### Branching Outcomes\n{character.branching_outcomes}\n\n"
        f"---\n\n"
        f"## Dynamic Behavior\n\n"
        f"### Approval System\n{character.approval_system}\n\n"
        f"### Contextual Reactions\n{character.contextual_reactions}\n\n"
        f"### Leaving Conditions\n{character.leaving_conditions}\n\n"
        f"---\n\n"
        f"## Voice & Dialogue\n\n"
        f"### Voice Direction\n{character.voice_direction}\n\n"
        f"### Sample Dialogue\n{character.dialogue_examples}\n\n"
        f"---\n\n"
        f"## Technical Implementation\n\n"
        f"### AI Behavior\n{character.ai_behavior}\n\n"
        f"### Loot & Rewards\n{character.loot_rewards}\n\n"
        f"---\n\n"
        f"## Narrative Integration\n\n"
        f"### Thematic Resonance\n{character.thematic_resonance}\n\n"
        f"### Player Impact\n{character.player_impact}\n"
    )
    
    return {"character_md": md}

def evaluate_character(state: CharacterState):
    """Evaluate character for depth, distinctiveness, and gameplay integration."""
    character_md = state["character_md"]
    character_type = state.get("character_type", "companion")
    
    rubric = (
        f"Evaluate this {character_type} character for:\n\n"
        "1. **Personality Depth**: Contradictory traits? Internal conflicts? Or flat archetype?\n"
        "2. **Visual Distinctiveness**: Recognizable silhouette? Unique design? Or generic appearance?\n"
        "3. **Character Arc**: Clear transformation? Emotional growth? Or static personality?\n"
        "4. **Gameplay Integration**: Mechanics match personality? Unique playstyle? Or generic stats?\n"
        "5. **Dialogue Quality**: Distinct voice in sample lines? Personality shines through? Or bland speech?\n"
        "6. **Approval Logic**: Values-based reactions? Or arbitrary good/evil system?\n"
        "7. **Branching Outcomes**: Meaningful fate variations? Player choice impact? Or linear path?\n"
        "8. **Originality**: Unexpected trait combinations? Fresh take? Or tired clichés?\n"
        "9. **Purpose Clarity**: Clear narrative function? Player impact? Or forgettable addition?\n\n"
        "REJECT if character is:\n"
        "- Pure archetype without contradictions (noble knight, evil wizard, etc.)\n"
        "- Visually generic without memorable features\n"
        "- Has no clear arc or growth\n"
        "- Mechanically identical to existing classes\n"
        "- Sample dialogue could be anyone speaking\n\n"
        "ACCEPT only if character is memorable, mechanically distinct, and narratively purposeful."
    )
    
    review = evaluator.invoke(f"{rubric}\n\nCHARACTER:\n{character_md}")
    return {"decision": review.decision, "feedback": review.feedback}

def route_character(state: CharacterState):
    """Route to finish on accept; loop back with feedback to revise."""
    if state["decision"] == "accept":
        return "Accepted"
    else:
        return "Revise"

# Build workflow
builder = StateGraph(CharacterState)
builder.add_node("generate_character", generate_character)
builder.add_node("evaluate_character", evaluate_character)
builder.add_edge(START, "generate_character")
builder.add_edge("generate_character", "evaluate_character")
builder.add_conditional_edges(
    "evaluate_character",
    route_character,
    {
        "Accepted": END,
        "Revise": "generate_character",
    },
)

character_workflow = builder.compile()

# Example invocations
if __name__ == "__main__":
    # Example 1: Companion character
    result1 = character_workflow.invoke({
        "character_prompt": "Disgraced knight seeking redemption but struggles with alcoholism",
        "character_type": "companion",
        "game_context": "Dark fantasy RPG with moral choice system, medieval setting with corruption themes"
    })
    print(result1["character_md"])
    print("\n" + "="*80 + "\n")
    
    # Example 2: Boss character
    result2 = character_workflow.invoke({
        "character_prompt": "Corporate CEO who uploaded consciousness but lost humanity",
        "character_type": "boss",
        "game_context": "Cyberpunk action RPG, themes of transhumanism and identity"
    })
    print(result2["character_md"])
    print("\n" + "="*80 + "\n")
    
    # Example 3: Romance option
    result3 = character_workflow.invoke({
        "character_prompt": "Rogue scientist who experiments on themselves, balancing genius with madness",
        "character_type": "companion",
        "game_context": "Post-apocalyptic RPG, romance and companion mechanics, moral grey areas"
    })
    print(result3["character_md"])
    print("\n" + "="*80 + "\n")
    
    # Example 4: Quest NPC
    result4 = character_workflow.invoke({
        "character_prompt": "Cheerful merchant with dark secret past as assassin",
        "character_type": "npc",
        "game_context": "Fantasy adventure game with faction system and hidden backstories"
    })
    print(result4["character_md"])
