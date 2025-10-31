# Video Game Questlines Agent - LangGraph Workflow
from typing import TypedDict, Literal
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

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
    
    # Progression & Pacing
    act_structure: str = Field(description="Quest beats: Introduction → Investigation → Complication → Climax → Resolution.")
    intensity_curve: str = Field(description="Pacing: quiet exploration → action spike → breather → final confrontation.")
    checkpoint_placement: str = Field(description="Natural save/rest points, fast travel unlock, point-of-no-return warnings.")
    player_agency_moments: str = Field(description="Moments where player has control: dialogue choices, approach selection, moral decisions.")
    
    # Rewards & Consequences
    xp_rewards: str = Field(description="Experience points for completion, bonus XP for optional objectives.")
    item_rewards: str = Field(description="Loot: unique weapons, armor, consumables, crafting materials, quest-specific items.")
    currency_rewards: str = Field(description="Gold/credits amount, scaling with difficulty, bonus for speed/stealth runs.")
    reputation_changes: str = Field(description="Faction reputation gains/losses, how this affects future quests/interactions.")
    unlocked_content: str = Field(description="New areas, merchants, companions, abilities, follow-up quests unlocked.")
    world_state_changes: str = Field(description="Permanent world changes: NPC deaths, settlement saved, faction power shifts.")
    
    # Failure & Retry
    failure_handling: str = Field(description="What happens on failure: retry immediately, quest fails permanently, alternate path opens.")
    death_consequences: str = Field(description="Checkpoint respawn, lose progress, lose items, NPC can die permanently.")
    quest_abandonment: str = Field(description="Can player abandon quest? Consequences for doing so? Can they restart later?")
    
    # Replayability Features
    alternate_solutions: str = Field(description="Multiple valid approaches: combat, stealth, diplomacy, hacking, ally assistance.")
    hidden_content: str = Field(description="Secrets only discoverable on replays or with specific skills/faction membership.")
    speedrun_potential: str = Field(description="Sequence breaks, skips, optimal paths for fast completion.")
    challenge_modes: str = Field(description="Hard mode variants, no-damage runs, restricted loadouts, time trials.")
    
    # Technical Implementation
    quest_tracking: str = Field(description="How quest appears in journal, map markers, compass indicators, distance tracking.")
    dialogue_volume: str = Field(description="Estimated lines of dialogue, fully voiced vs text-only, language localization needs.")
    cutscene_requirements: str = Field(description="In-engine cutscenes vs gameplay, length, skippability, player control during scenes.")
    bug_prevention: str = Field(description="Common quest-breaking scenarios to avoid: item despawn, NPC pathing, objective triggers.")
    
    # Quality Metrics
    player_engagement: str = Field(description="What makes this quest memorable vs generic fetch quest, emotional hooks.")
    avoid_frustration: str = Field(description="How to prevent: vague objectives, tedious backtracking, unclear fail states, soft locks.")
    accessibility_options: str = Field(description="Quest markers, difficulty scaling, color-blind friendly indicators, skip options.")

class QuestReview(BaseModel):
    """Evaluator review for questline."""
    decision: Literal["accept", "revise"] = Field(
        description="Accept if quest has clear objectives, meaningful choices, proper pacing, avoids tedium; otherwise revise."
    )
    feedback: str = Field(description="Specific improvements: vague objectives, no player agency, tedious backtracking, unclear progression.")

class QuestState(TypedDict):
    quest_prompt: str
    quest_type: str  # main, side, faction, companion
    game_context: str  # Genre, setting, mechanics
    quest_md: str
    feedback: str
    decision: str

# Prepare evaluator
evaluator = llm.with_structured_output(QuestReview, method="json_schema")

def generate_quest(state: QuestState):
    """Generate detailed questline with branching objectives and player agency."""
    quest_prompt = state["quest_prompt"]
    quest_type = state.get("quest_type", "side quest")
    game_context = state.get("game_context", "")
    
    guidance = (
        f"You are a master quest designer specializing in engaging, non-generic missions. "
        f"Create a {quest_type} based on: '{quest_prompt}'. "
        "CRITICAL QUEST DESIGN PRINCIPLES:\n\n"
        "**AVOID GENERIC FETCH QUESTS:**\n"
        "- NO simple 'go here, get item, return' without narrative context\n"
        "- NO tedious collect 10 bear asses without story justification\n"
        "- NO vague 'search the area' without specific clues\n"
        "- NO mandatory backtracking through empty areas\n\n"
        "**CREATE ENGAGING OBJECTIVES:**\n"
        "- Use strong action verbs: Infiltrate, Rescue, Investigate, Sabotage, Defend\n"
        "- Break large tasks into nested objectives with progress tracking\n"
        "- Provide 2-3 valid approaches (combat/stealth/diplomacy)\n"
        "- Include moral choices with no obvious right answer\n"
        "- Make failure interesting (alternative paths, not just reload)\n\n"
        "**BRANCHING NARRATIVE:**\n"
        "- Design 2-3 decision points that genuinely change quest outcome\n"
        "- Skill checks should unlock shortcuts, not gate content arbitrarily\n"
        "- Faction reputation affects NPC reactions and available options\n"
        "- Choices have consequences beyond this quest (affect future content)\n\n"
        "**PACING & FLOW:**\n"
        "- Start with immediate hook (NPC in danger, mystery discovered, betrayal)\n"
        "- Investigation/buildup → Complication → Climax → Resolution\n"
        "- Mix gameplay types: combat, stealth, dialogue, puzzle, exploration\n"
        "- Include rest/save points after intense sequences\n"
        "- Point-of-no-return warnings before major commitments\n\n"
        "**MEANINGFUL REWARDS:**\n"
        "- Unique items that match quest narrative (traitor's dagger, rescued mage's spell)\n"
        "- Reputation changes that unlock future content\n"
        "- World state changes visible to player (NPC survives, settlement saved)\n"
        "- Avoid pure RNG drops—guarantee quest-specific rewards\n\n"
        "**PLAYER AGENCY:**\n"
        "- Let players express themselves through approach and dialogue\n"
        "- Multiple valid solutions to objectives\n"
        "- Can question quest giver's motives or refuse quest\n"
        "- Consequences match player's moral choices (merciful vs ruthless)\n\n"
        "**TECHNICAL POLISH:**\n"
        "- Clear objective markers and journal updates\n"
        "- Prevent soft locks (objectives uncompletable due to bugs)\n"
        "- Allow quest abandonment if player gets stuck\n"
        "- Skippable cutscenes, especially on replays"
    )
    
    if game_context:
        guidance += f"\n\nGame Context: {game_context}"
    
    if state.get("feedback"):
        guidance += f"\n\nIMPORTANT - Address this feedback: {state['feedback']}"
    
    schema = llm.with_structured_output(Questline, method="json_schema")
    quest = schema.invoke(guidance)
    
    md = (
        f"# {quest.quest_name}\n\n"
        f"**Type**: {quest.quest_type} | **Difficulty**: {quest.difficulty} | **Time**: {quest.estimated_time}\n\n"
        f"---\n\n"
        f"## Quest Discovery\n\n"
        f"### How to Start\n{quest.discovery_method}\n\n"
        f"### Quest Giver\n{quest.quest_giver}\n\n"
        f"### Hook & Pitch\n{quest.hook_pitch}\n\n"
        f"### Urgency\n{quest.urgency_factor}\n\n"
        f"---\n\n"
        f"## Objectives Structure\n\n"
        f"### Primary Objectives\n{quest.primary_objectives}\n\n"
        f"### Optional Objectives\n{quest.optional_objectives}\n\n"
        f"### Nested Sub-Tasks\n{quest.nested_objectives}\n\n"
        f"### Failure Conditions\n{quest.failure_conditions}\n\n"
        f"---\n\n"
        f"## Branching Paths\n\n"
        f"### Major Choice Points\n{quest.choice_points}\n\n"
        f"### Path Outcomes\n{quest.path_outcomes}\n\n"
        f"### Skill Checks & Shortcuts\n{quest.skill_checks}\n\n"
        f"### Faction Variations\n{quest.faction_variations}\n\n"
        f"---\n\n"
        f"## Gameplay Elements\n\n"
        f"### Mechanics Introduced\n{quest.mechanics_introduced}\n\n"
        f"### Combat Encounters\n{quest.combat_encounters}\n\n"
        f"### Puzzle Elements\n{quest.puzzle_elements}\n\n"
        f"### Exploration Requirements\n{quest.exploration_required}\n\n"
        f"---\n\n"
        f"## Narrative Beats\n\n"
        f"### Story Moments\n{quest.story_beats}\n\n"
        f"### NPC Interactions\n{quest.npc_interactions}\n\n"
        f"### Environmental Storytelling\n{quest.environmental_storytelling}\n\n"
        f"### Lore Reveals\n{quest.lore_reveals}\n\n"
        f"---\n\n"
        f"## Pacing & Structure\n\n"
        f"### Act Structure\n{quest.act_structure}\n\n"
        f"### Intensity Curve\n{quest.intensity_curve}\n\n"
        f"### Checkpoint Placement\n{quest.checkpoint_placement}\n\n"
        f"### Player Agency Moments\n{quest.player_agency_moments}\n\n"
        f"---\n\n"
        f"## Rewards & Consequences\n\n"
        f"### Experience Rewards\n{quest.xp_rewards}\n\n"
        f"### Item Rewards\n{quest.item_rewards}\n\n"
        f"### Currency Rewards\n{quest.currency_rewards}\n\n"
        f"### Reputation Changes\n{quest.reputation_changes}\n\n"
        f"### Unlocked Content\n{quest.unlocked_content}\n\n"
        f"### World State Changes\n{quest.world_state_changes}\n\n"
        f"---\n\n"
        f"## Failure & Retry\n\n"
        f"### Failure Handling\n{quest.failure_handling}\n\n"
        f"### Death Consequences\n{quest.death_consequences}\n\n"
        f"### Quest Abandonment\n{quest.quest_abandonment}\n\n"
        f"---\n\n"
        f"## Replayability\n\n"
        f"### Alternate Solutions\n{quest.alternate_solutions}\n\n"
        f"### Hidden Content\n{quest.hidden_content}\n\n"
        f"### Speedrun Potential\n{quest.speedrun_potential}\n\n"
        f"### Challenge Modes\n{quest.challenge_modes}\n\n"
        f"---\n\n"
        f"## Technical Implementation\n\n"
        f"### Quest Tracking UI\n{quest.quest_tracking}\n\n"
        f"### Dialogue Volume\n{quest.dialogue_volume}\n\n"
        f"### Cutscene Requirements\n{quest.cutscene_requirements}\n\n"
        f"### Bug Prevention\n{quest.bug_prevention}\n\n"
        f"---\n\n"
        f"## Quality Assurance\n\n"
        f"### Player Engagement\n{quest.player_engagement}\n\n"
        f"### Frustration Prevention\n{quest.avoid_frustration}\n\n"
        f"### Accessibility Options\n{quest.accessibility_options}\n"
    )
    
    return {"quest_md": md}

def evaluate_quest(state: QuestState):
    """Evaluate questline for engagement, clarity, player agency, and anti-tedium."""
    quest_md = state["quest_md"]
    quest_type = state.get("quest_type", "side quest")
    
    rubric = (
        f"Evaluate this {quest_type} for:\n\n"
        "**CRITICAL RED FLAGS (Auto-Reject):**\n"
        "❌ Generic fetch quest with no narrative justification\n"
        "❌ Vague objectives like 'search the area' without clues\n"
        "❌ Mandatory tedious backtracking through empty zones\n"
        "❌ 'Collect 10 X' without story reason or interesting gameplay\n"
        "❌ Only one solution path (no combat/stealth/diplomacy options)\n"
        "❌ Fake choices that don't affect quest outcome\n"
        "❌ Unclear failure conditions or soft lock potential\n"
        "❌ Rewards don't match quest narrative (generic loot for epic story)\n\n"
        "**OBJECTIVE CLARITY (Critical):**\n"
        "1. Are objectives specific with strong action verbs?\n"
        "2. Are nested objectives properly broken down with progress tracking?\n"
        "3. Does quest journal provide enough info without holding player's hand?\n"
        "4. Are failure conditions clearly communicated?\n\n"
        "**PLAYER AGENCY (Critical):**\n"
        "5. Do 2-3 major choices genuinely branch quest outcomes?\n"
        "6. Are there multiple valid approaches (combat/stealth/diplomacy)?\n"
        "7. Do skill checks unlock shortcuts vs gating content arbitrarily?\n"
        "8. Can player question quest giver or refuse quest ethically?\n\n"
        "**NARRATIVE ENGAGEMENT:**\n"
        "9. Does opening hook grab attention immediately?\n"
        "10. Are story beats emotionally impactful vs expository?\n"
        "11. Do NPC interactions feel meaningful vs transactional?\n"
        "12. Is lore revealed through gameplay vs text dumps?\n\n"
        "**PACING & VARIETY:**\n"
        "13. Does intensity curve mix action/exploration/dialogue/puzzle?\n"
        "14. Are checkpoints placed after intense sequences?\n"
        "15. Point-of-no-return warnings before major commitments?\n"
        "16. Estimated time matches actual content (not padded)?\n\n"
        "**REWARDS & CONSEQUENCES:**\n"
        "17. Are rewards narratively appropriate (traitor's weapon, rescued mage's spell)?\n"
        "18. Do reputation changes affect future content meaningfully?\n"
        "19. Are world state changes visible (NPC survives, settlement saved)?\n"
        "20. No pure RNG—quest-specific rewards guaranteed?\n\n"
        "**REPLAYABILITY:**\n"
        "21. Are there hidden solutions discoverable on replays?\n"
        "22. Does faction allegiance meaningfully change quest experience?\n"
        "23. Speedrun potential without breaking immersion?\n\n"
        "**TECHNICAL POLISH:**\n"
        "24. Clear quest markers and journal updates?\n"
        "25. Bug prevention for common soft locks addressed?\n"
        "26. Can player abandon if stuck? Cutscenes skippable?\n\n"
        "**SCORING:**\n"
        "- Accept if 20+ criteria met and NO red flags present\n"
        "- Revise if any red flags or <15 criteria met\n"
        "- Provide specific, actionable feedback for improvements"
    )
    
    review = evaluator.invoke(f"{rubric}\n\nQUESTLINE:\n{quest_md}")
    return {"decision": review.decision, "feedback": review.feedback}

def route_quest(state: QuestState):
    """Route to finish on accept; loop back with feedback to revise."""
    if state["decision"] == "accept":
        return "Accepted"
    else:
        return "Revise"

# Build workflow
builder = StateGraph(QuestState)
builder.add_node("generate_quest", generate_quest)
builder.add_node("evaluate_quest", evaluate_quest)
builder.add_edge(START, "generate_quest")
builder.add_edge("generate_quest", "evaluate_quest")
builder.add_conditional_edges(
    "evaluate_quest",
    route_quest,
    {
        "Accepted": END,
        "Revise": "generate_quest",
    },
)

quest_workflow = builder.compile()

# Example invocations
if __name__ == "__main__":
    # Example 1: Morally grey side quest
    result1 = quest_workflow.invoke({
        "quest_prompt": "Village elder asks you to eliminate bandits, but bandits claim they're refugees driven to desperation",
        "quest_type": "side quest",
        "game_context": "Dark fantasy RPG with moral choice system, investigation mechanics, reputation system"
    })
    print(result1["quest_md"])
    print("\n" + "="*80 + "\n")
    
    # Example 2: Stealth infiltration quest
    result2 = quest_workflow.invoke({
        "quest_prompt": "Infiltrate corporate headquarters to steal AI prototype, can ally with inside whistleblower",
        "quest_type": "main quest",
        "game_context": "Cyberpunk RPG, multiple approach options, hacking and stealth mechanics"
    })
    print(result2["quest_md"])
    print("\n" + "="*80 + "\n")
    
    # Example 3: Companion loyalty quest
    result3 = quest_workflow.invoke({
        "quest_prompt": "Companion's betrayer from past returns seeking reconciliation, player decides if they forgive",
        "quest_type": "companion quest",
        "game_context": "Space opera RPG, companion approval system, branching dialogue, character growth themes"
    })
    print(result3["quest_md"])
    print("\n" + "="*80 + "\n")
    
    # Example 4: Investigation mystery quest
    result4 = quest_workflow.invoke({
        "quest_prompt": "Series of murders with supernatural elements, player gathers clues to identify killer from suspects",
        "quest_type": "side quest",
        "game_context": "Gothic horror RPG, detective mechanics, environmental storytelling, multiple suspects"
    })
    print(result4["quest_md"])
