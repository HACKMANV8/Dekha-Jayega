# Video Game Plot Arcs Agent - LangGraph Workflow
from typing import TypedDict, Literal
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

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
    
    # Player Agency & Interactivity
    moral_dilemmas: str = Field(description="Ethical choices without clear right/wrong answers, test player values.")
    fail_states: str = Field(description="Can player fail quests? Permadeath? What happens if they lose key battles?")
    exploration_rewards: str = Field(description="Optional lore, side content discovered through exploration, not mandatory.")
    player_pacing_control: str = Field(description="Can player tackle objectives in any order? Fast travel? Skip content?")
    
    # Side Content Integration
    parallel_questlines: str = Field(description="Companion quests, faction missions that intersect with main arc.")
    optional_objectives: str = Field(description="Bonus goals, secret bosses, hidden endings for completionists.")
    environmental_storytelling: str = Field(description="Lore told through world design, item descriptions, environmental clues.")
    
    # Pacing & Structure
    intensity_curve: str = Field(description="Map of emotional/action intensity: quiet moments → tension → release → climax.")
    checkpoint_structure: str = Field(description="Where save points/checkpoints occur, how death/failure is handled.")
    act_transitions: str = Field(description="How player moves between acts: cutscenes, open-world transition, choice-driven?")
    
    # Character Integration
    protagonist_arc: str = Field(description="How player character changes/grows throughout the arc.")
    antagonist_presence: str = Field(description="How villain appears throughout: direct confrontations, proxy battles, looming threat?")
    companion_roles: str = Field(description="Which companions are essential to this arc, how they contribute to narrative.")
    
    # Gameplay-Narrative Integration
    mechanics_as_metaphor: str = Field(description="How gameplay mechanics reinforce narrative themes (losing powers = narrative loss).")
    ludonarrative_harmony: str = Field(description="Ensure gameplay and story don't contradict: violent gameplay vs pacifist story?")
    player_expression: str = Field(description="How players express themselves through choices, builds, dialogue options, playstyle.")
    
    # Technical Considerations
    cutscene_balance: str = Field(description="Ratio of cutscenes to gameplay, are they skippable? Length limits?")
    voice_acting_scope: str = Field(description="Dialogue volume, branching conversations, budget considerations.")
    localization_complexity: str = Field(description="How choice branches affect translation work, subtitle timing.")
    
    # Replayability
    ng_plus_features: str = Field(description="New Game Plus additions: harder enemies, alternate perspectives, bonus content.")
    speedrun_potential: str = Field(description="Can arc be sequence-broken? Intended skip mechanics? Glitches to embrace?")
    completionist_content: str = Field(description="100% completion rewards, collectibles, achievement design.")

class PlotReview(BaseModel):
    """Evaluator review for plot arc."""
    decision: Literal["accept", "revise"] = Field(
        description="Accept if arc has clear three-act structure, meaningful choices, proper pacing; otherwise revise."
    )
    feedback: str = Field(description="Specific improvements: weak Act 2, unclear stakes, no player agency, pacing issues.")

class PlotState(TypedDict):
    plot_prompt: str
    game_context: str  # Genre, setting, themes
    arc_length: str  # short/medium/long
    plot_md: str
    feedback: str
    decision: str

# Prepare evaluator
evaluator = llm.with_structured_output(PlotReview, method="json_schema")

def generate_plot(state: PlotState):
    """Generate branching plot arc with interactive narrative design."""
    plot_prompt = state["plot_prompt"]
    game_context = state.get("game_context", "")
    arc_length = state.get("arc_length", "medium")
    
    guidance = (
        f"You are a master narrative designer specializing in interactive storytelling. "
        f"Create a {arc_length} plot arc based on: '{plot_prompt}'. "
        "CRITICAL REQUIREMENTS:\n\n"
        "1. START WITH ACTION: Hook player in first 5 minutes with interactive sequence\n"
        "2. TUTORIAL THROUGH NARRATIVE: Teach mechanics through story context, not lectures\n"
        "3. CLEAR THREE-ACT STRUCTURE: Setup → Confrontation → Resolution with proper pacing\n"
        "4. MIDPOINT TWIST: Major revelation at 50% mark that recontextualizes everything\n"
        "5. BRANCHING CHOICES: 3-5 major decisions that genuinely affect outcomes\n"
        "6. PLAYER AGENCY: Players must feel their choices matter, not just cosmetic differences\n"
        "7. MULTIPLE ENDINGS: 3-5 distinct conclusions based on choices, not just A/B/C variations\n"
        "8. LUDONARRATIVE HARMONY: Ensure gameplay mechanics support story themes\n"
        "9. PACING VARIETY: Mix action, exploration, dialogue, quiet moments, crescendo to climax\n"
        "10. REPLAYABILITY: Design for multiple playthroughs with different experiences\n\n"
        "AVOID:\n"
        "- Long unskippable cutscenes at start\n"
        "- Linear railroading with fake choices\n"
        "- Protagonist who talks for player (unless voiced protagonist established)\n"
        "- Plot twists that contradict established rules\n"
        "- Punishing players for exploration or experimentation"
    )
    
    if game_context:
        guidance += f"\n\nGame Context: {game_context}"
    
    if state.get("feedback"):
        guidance += f"\n\nIMPORTANT - Address this feedback: {state['feedback']}"
    
    schema = llm.with_structured_output(PlotArc, method="json_schema")
    arc = schema.invoke(guidance)
    
    md = (
        f"# {arc.arc_title}\n\n"
        f"**Type**: {arc.arc_type} | **Playtime**: {arc.estimated_playtime}\n\n"
        f"**Central Question**: *{arc.central_question}*\n\n"
        f"**Theme**: {arc.theme}\n\n"
        f"---\n\n"
        f"## Act 1: Setup & Introduction\n\n"
        f"### Opening Hook\n{arc.act1_hook}\n\n"
        f"### Worldbuilding & Context\n{arc.act1_worldbuilding}\n\n"
        f"### Tutorial Integration\n{arc.act1_tutorial}\n\n"
        f"### Inciting Incident\n{arc.inciting_incident}\n\n"
        f"### Act 1 Player Goal\n{arc.act1_player_goal}\n\n"
        f"### Plot Point 1 (Point of No Return)\n{arc.plot_point_1}\n\n"
        f"---\n\n"
        f"## Act 2: Confrontation & Rising Action\n\n"
        f"### Progression & Escalation\n{arc.act2_progression}\n\n"
        f"### Complications\n{arc.act2_complications}\n\n"
        f"### Midpoint Twist\n{arc.midpoint_twist}\n\n"
        f"### Setbacks & Dark Night\n{arc.act2_setbacks}\n\n"
        f"### Companion Development\n{arc.companion_development}\n\n"
        f"### Plot Point 2 (Final Crisis)\n{arc.plot_point_2}\n\n"
        f"---\n\n"
        f"## Act 3: Climax & Resolution\n\n"
        f"### Final Preparations\n{arc.act3_final_prep}\n\n"
        f"### Climax Sequence\n{arc.climax_sequence}\n\n"
        f"### Boss Mechanics\n{arc.boss_mechanics}\n\n"
        f"### Resolution\n{arc.resolution}\n\n"
        f"### Epilogue\n{arc.epilogue}\n\n"
        f"---\n\n"
        f"## Branching Narrative System\n\n"
        f"### Major Choice Points\n{arc.major_choice_points}\n\n"
        f"### Choice Consequences\n{arc.choice_consequences}\n\n"
        f"### Conditional Content\n{arc.conditional_content}\n\n"
        f"### Multiple Endings\n{arc.multiple_endings}\n\n"
        f"---\n\n"
        f"## Player Agency & Interactivity\n\n"
        f"### Moral Dilemmas\n{arc.moral_dilemmas}\n\n"
        f"### Fail States\n{arc.fail_states}\n\n"
        f"### Exploration Rewards\n{arc.exploration_rewards}\n\n"
        f"### Player Pacing Control\n{arc.player_pacing_control}\n\n"
        f"---\n\n"
        f"## Side Content Integration\n\n"
        f"### Parallel Questlines\n{arc.parallel_questlines}\n\n"
        f"### Optional Objectives\n{arc.optional_objectives}\n\n"
        f"### Environmental Storytelling\n{arc.environmental_storytelling}\n\n"
        f"---\n\n"
        f"## Pacing & Structure\n\n"
        f"### Intensity Curve\n{arc.intensity_curve}\n\n"
        f"### Checkpoint Structure\n{arc.checkpoint_structure}\n\n"
        f"### Act Transitions\n{arc.act_transitions}\n\n"
        f"---\n\n"
        f"## Character Integration\n\n"
        f"### Protagonist Arc\n{arc.protagonist_arc}\n\n"
        f"### Antagonist Presence\n{arc.antagonist_presence}\n\n"
        f"### Companion Roles\n{arc.companion_roles}\n\n"
        f"---\n\n"
        f"## Gameplay-Narrative Harmony\n\n"
        f"### Mechanics as Metaphor\n{arc.mechanics_as_metaphor}\n\n"
        f"### Ludonarrative Harmony\n{arc.ludonarrative_harmony}\n\n"
        f"### Player Expression\n{arc.player_expression}\n\n"
        f"---\n\n"
        f"## Technical Considerations\n\n"
        f"### Cutscene Balance\n{arc.cutscene_balance}\n\n"
        f"### Voice Acting Scope\n{arc.voice_acting_scope}\n\n"
        f"### Localization Complexity\n{arc.localization_complexity}\n\n"
        f"---\n\n"
        f"## Replayability\n\n"
        f"### New Game Plus\n{arc.ng_plus_features}\n\n"
        f"### Speedrun Potential\n{arc.speedrun_potential}\n\n"
        f"### Completionist Content\n{arc.completionist_content}\n"
    )
    
    return {"plot_md": md}

def evaluate_plot(state: PlotState):
    """Evaluate plot arc for structure, pacing, player agency, and interactivity."""
    plot_md = state["plot_md"]
    
    rubric = (
        "Evaluate this plot arc for:\n\n"
        "**STRUCTURE (Critical):**\n"
        "1. Clear three-act structure with proper act breaks?\n"
        "2. Strong opening hook that starts with action/gameplay?\n"
        "3. Midpoint twist that genuinely changes player understanding?\n"
        "4. Escalating intensity curve leading to satisfying climax?\n\n"
        "**PLAYER AGENCY (Critical):**\n"
        "5. Do choices have meaningful consequences beyond dialogue changes?\n"
        "6. Are there 3+ genuinely distinct endings based on player decisions?\n"
        "7. Can player express themselves through gameplay/builds/dialogue?\n"
        "8. Are moral dilemmas complex with no obvious right answer?\n\n"
        "**PACING & FLOW:**\n"
        "9. Variety between action, exploration, story, quiet moments?\n"
        "10. Tutorial integrated naturally without breaking immersion?\n"
        "11. Proper checkpointing so death doesn't frustrate?\n"
        "12. Player has pacing control (skip cutscenes, tackle objectives flexibly)?\n\n"
        "**LUDONARRATIVE HARMONY:**\n"
        "13. Do gameplay mechanics reinforce narrative themes?\n"
        "14. No contradictions between story and gameplay?\n"
        "15. Mechanics introduced serve narrative purpose?\n\n"
        "**REPLAYABILITY:**\n"
        "16. Reason to play multiple times beyond seeing all endings?\n"
        "17. Conditional content that reveals new perspectives?\n"
        "18. New Game Plus or alternate playthrough incentives?\n\n"
        "**RED FLAGS (Auto-reject if present):**\n"
        "- Long unskippable intro before gameplay\n"
        "- Fake choices that don't affect anything\n"
        "- Linear path disguised as branching narrative\n"
        "- Plot requires player to be stupid/ignore obvious solutions\n"
        "- Punishes exploration or experimentation\n\n"
        "Accept only if arc demonstrates strong interactive storytelling principles."
    )
    
    review = evaluator.invoke(f"{rubric}\n\nPLOT ARC:\n{plot_md}")
    return {"decision": review.decision, "feedback": review.feedback}

def route_plot(state: PlotState):
    """Route to finish on accept; loop back with feedback to revise."""
    if state["decision"] == "accept":
        return "Accepted"
    else:
        return "Revise"

# Build workflow
builder = StateGraph(PlotState)
builder.add_node("generate_plot", generate_plot)
builder.add_node("evaluate_plot", evaluate_plot)
builder.add_edge(START, "generate_plot")
builder.add_edge("generate_plot", "evaluate_plot")
builder.add_conditional_edges(
    "evaluate_plot",
    route_plot,
    {
        "Accepted": END,
        "Revise": "generate_plot",
    },
)

plot_workflow = builder.compile()

# Example invocations
if __name__ == "__main__":
    # Example 1: Dark fantasy main quest
    result1 = plot_workflow.invoke({
        "plot_prompt": "Player must choose between saving their dying kingdom or ascending to godhood",
        "game_context": "Dark fantasy RPG, themes of sacrifice vs ambition, morally grey choices",
        "arc_length": "long"
    })
    print(result1["plot_md"])
    print("\n" + "="*80 + "\n")
    
    # Example 2: Sci-fi faction questline
    result2 = plot_workflow.invoke({
        "plot_prompt": "Corporate espionage mission that reveals player's memories are fabricated",
        "game_context": "Cyberpunk RPG, themes of identity and free will, stealth gameplay",
        "arc_length": "medium"
    })
    print(result2["plot_md"])
    print("\n" + "="*80 + "\n")
    
    # Example 3: Companion character arc
    result3 = plot_workflow.invoke({
        "plot_prompt": "Companion seeking revenge discovers their target is their long-lost sibling",
        "game_context": "Action RPG, themes of family vs justice, player can influence outcome",
        "arc_length": "short"
    })
    print(result3["plot_md"])
