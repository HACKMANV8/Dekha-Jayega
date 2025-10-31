"""
Prompts for orchestrator agent to analyze and provide feedback on SagaAgent narrative files.
"""


def get_user_view_analysis_prompt(saga_data: dict, user_feedback: str = "") -> str:
    """
    Generate prompt for analyzing a saga narrative file and providing structured feedback.
    
    Args:
        saga_data: The complete saga JSON data (concept, world_lore, factions, characters, plot_arcs, questlines)
        user_feedback: Optional additional feedback from the user
        
    Returns:
        Formatted prompt string
    """
    
    user_feedback_section = ""
    if user_feedback:
        user_feedback_section = f"""
## User Feedback

The user has provided the following feedback:
{user_feedback}

Please incorporate this feedback into your analysis and recommendations.
"""
    
    concept = saga_data.get('concept', {})
    world_lore = saga_data.get('world_lore', {})
    
    prompt = f"""You are an expert game narrative analyst and world-building consultant. Your task is to analyze a game's narrative structure and provide structured, actionable feedback.

{user_feedback_section}

## Game Narrative Content to Analyze

**Title:** {concept.get('title', 'Untitled')}
**Genre:** {concept.get('genre', 'N/A')}
**Setting:** {concept.get('world_setting', 'N/A')}

**Concept (Elevator Pitch):**
{concept.get('elevator_pitch', 'N/A')}

**Core Loop:**
{concept.get('core_loop', 'N/A')}

**World Lore:**
**World Name:** {world_lore.get('world_name', 'N/A')}
**History:** {world_lore.get('history', 'N/A')[:300]}...
**Culture:** {world_lore.get('culture', 'N/A')[:300]}...
**Themes:** {', '.join(world_lore.get('key_themes', []))}

**Factions ({len(saga_data.get('factions', []))}):**
{format_factions(saga_data.get('factions', []))}

**Characters ({len(saga_data.get('characters', []))}):**
{format_characters(saga_data.get('characters', []))}

**Plot Arcs ({len(saga_data.get('plot_arcs', []))}):**
{format_plot_arcs(saga_data.get('plot_arcs', []))}

**Questlines ({len(saga_data.get('questlines', []))}):**
{format_questlines(saga_data.get('questlines', []))}

## Analysis Instructions

Analyze the game narrative comprehensively and provide feedback on:

1. **Overall Assessment**: Evaluate the narrative's strengths and weaknesses
2. **Narrative Coherence Score**: Rate 1-10 based on:
   - World-building consistency and depth
   - Character depth and faction dynamics
   - Plot arc coherence and pacing
   - Questline variety and engagement
   - Thematic consistency
   - Alignment with game concept and genre

3. **Component Feedback**: For each component (concept, world_lore, factions, characters, plot_arcs, questlines):
   - Determine if it needs updating
   - Provide specific, actionable feedback
   - Assign priority (1=critical, 2=important, 3=nice-to-have)

4. **Suggested Improvements**: List 3-5 high-level improvements

## Guidelines

- Be specific and actionable in feedback
- Consider how components interact (e.g., characters should align with factions)
- Identify inconsistencies, gaps, or missed opportunities
- Suggest concrete improvements, not just criticisms
- Respect the game's genre, setting, and core loop
- Focus on what will most improve player engagement

Please provide your analysis in the structured format requested.
"""
    
    return prompt


def format_factions(factions: list) -> str:
    """Format factions for display"""
    if not factions:
        return "No factions defined"
    
    parts = []
    for i, faction in enumerate(factions, 1):
        name = faction.get('name', 'Unknown')
        ideology = faction.get('ideology', 'N/A')
        influence = faction.get('influence_level', 'N/A')
        parts.append(f"{i}. **{name}** (Influence: {influence})\n   Ideology: {ideology[:200]}...")
    
    return "\n".join(parts)


def format_characters(characters: list) -> str:
    """Format characters for display"""
    if not characters:
        return "No characters defined"
    
    parts = []
    for i, char in enumerate(characters, 1):
        name = char.get('name', 'Unknown')
        role = char.get('role', 'N/A')
        faction = char.get('faction_affiliation', 'None')
        backstory = char.get('backstory', 'N/A')
        parts.append(f"{i}. **{name}** ({role})\n   Faction: {faction}\n   Backstory: {backstory[:150]}...")
    
    return "\n".join(parts)


def format_plot_arcs(plot_arcs: list) -> str:
    """Format plot arcs for display"""
    if not plot_arcs:
        return "No plot arcs defined"
    
    parts = []
    for i, arc in enumerate(plot_arcs, 1):
        arc_name = arc.get('arc_name', 'Unknown')
        arc_type = arc.get('arc_type', 'N/A')
        stakes = arc.get('stakes', 'N/A')
        parts.append(f"{i}. **{arc_name}** ({arc_type})\n   Stakes: {stakes[:200]}...")
    
    return "\n".join(parts)


def format_questlines(questlines: list) -> str:
    """Format questlines for display"""
    if not questlines:
        return "No questlines defined"
    
    parts = []
    for i, quest in enumerate(questlines, 1):
        quest_name = quest.get('quest_name', 'Unknown')
        quest_type = quest.get('quest_type', 'N/A')
        objective = quest.get('objective', 'N/A')
        parts.append(f"{i}. **{quest_name}** ({quest_type})\n   Objective: {objective[:150]}...")
    
    return "\n".join(parts)


def get_revision_plan_prompt(analysis: dict, user_preferences: str = "") -> str:
    """
    Generate prompt for creating a revision plan based on analysis.
    
    Args:
        analysis: The UserViewAnalysis data
        user_preferences: Optional user preferences for the revision
        
    Returns:
        Formatted prompt string
    """
    
    preferences_section = ""
    if user_preferences:
        preferences_section = f"""
## User Preferences

{user_preferences}
"""
    
    prompt = f"""Based on the following analysis of a game narrative, create a detailed revision plan.

## Narrative Analysis

**Overall Assessment:**
{analysis.get('overall_assessment', 'N/A')}

**Narrative Coherence Score:** {analysis.get('narrative_coherence_score', 0)}/10

**Component Feedback:**
{format_component_feedback(analysis.get('component_feedback', []))}

**Suggested Improvements:**
{format_improvements(analysis.get('suggested_improvements', []))}

{preferences_section}

## Task

Create a comprehensive revision plan that:
1. Summarizes the key revisions needed
2. Lists components to update in optimal order
3. Defines the update strategy (which components depend on others)
4. Estimates the impact of these revisions

Consider:
- Concept should be updated first if it needs major changes
- World lore establishes the foundation for everything else
- Factions and characters can be updated in parallel
- Plot arcs depend on characters and factions
- Questlines depend on plot arcs and characters
- Updates should maintain narrative coherence

Provide your plan in the structured format requested.
"""
    
    return prompt


def format_component_feedback(component_feedback: list) -> str:
    """Format component feedback for display"""
    if not component_feedback:
        return "No component feedback"
    
    parts = []
    for cf in component_feedback:
        component = cf.get('component_name', 'Unknown')
        needs_update = cf.get('needs_update', False)
        priority = cf.get('priority', 3)
        feedback = cf.get('feedback', 'N/A')
        
        status = "[NEEDS UPDATE]" if needs_update else "[OK]"
        priority_label = {1: "HIGH", 2: "MEDIUM", 3: "LOW"}.get(priority, "MEDIUM")
        
        parts.append(f"**{component}** [{status}] Priority: {priority_label}\n   {feedback}")
    
    return "\n\n".join(parts)


def format_improvements(improvements: list) -> str:
    """Format suggested improvements for display"""
    if not improvements:
        return "No improvements suggested"
    
    return "\n".join(f"{i}. {imp}" for i, imp in enumerate(improvements, 1))


def get_component_identification_prompt(user_feedback: str, saga_data: dict) -> str:
    """
    Generate prompt for LLM to identify which components need updating based on user feedback.
    
    Args:
        user_feedback: The user's request or feedback
        saga_data: The current saga state
        
    Returns:
        Formatted prompt string
    """
    
    concept = saga_data.get('concept', {})
    
    prompt = f"""You are an expert game narrative orchestrator. Your task is to analyze user feedback and determine which narrative components need to be updated.

## User Feedback

"{user_feedback}"

## Current Saga State

**Title:** {concept.get('title', 'Untitled')}
**Genre:** {concept.get('genre', 'N/A')}
**Setting:** {concept.get('world_setting', 'N/A')}

**World Name:** {saga_data.get('world_lore', {}).get('world_name', 'N/A')}

**Factions:** {len(saga_data.get('factions', []))} faction(s) defined
{_format_faction_summary(saga_data.get('factions', []))}

**Characters:** {len(saga_data.get('characters', []))} character(s) defined
{_format_character_summary(saga_data.get('characters', []))}

**Plot Arcs:** {len(saga_data.get('plot_arcs', []))} arc(s) defined

**Questlines:** {len(saga_data.get('questlines', []))} questline(s) defined

## Available Components

You can update the following components:

1. **concept** - Game concept, elevator pitch, core loop, mechanics, USP
2. **world_lore** - World history, culture, geography, key themes
3. **factions** - Faction definitions, ideologies, goals, relationships
4. **characters** - Character profiles, backstories, motivations, relationships
5. **plot_arcs** - Major narrative arcs, stakes, resolutions
6. **questlines** - Individual quests, objectives, rewards, branches

## Your Task

Analyze the user's feedback and determine:

1. **User Intent**: What does the user want to achieve?

2. **Primary Component**: Which ONE component is the main target of the user's request?
   - If user mentions "game concept", "core loop", "mechanics", "USP" → likely **concept**
   - If user mentions "world", "history", "culture", "lore", "setting" → likely **world_lore**
   - If user mentions "faction", "group", "organization", "power" → likely **factions**
   - If user mentions "character", "protagonist", "NPC", "person" → likely **characters**
   - If user mentions "story", "narrative", "arc", "plot" → likely **plot_arcs**
   - If user mentions "quest", "mission", "objective", "task" → likely **questlines**

3. **Dependent Components**: Which other components might need updating (if any)?
   
   **IMPORTANT PRINCIPLE: BE EXTREMELY CONSERVATIVE**
   - Default to NO dependent components unless absolutely necessary
   - User can always make additional requests if needed
   - Avoid cascading updates that change parts the user didn't mention
   
   **Dependency Guidelines (use sparingly):**
   - If updating **concept**:
     * Generally NO dependencies (concept changes don't automatically require regenerating everything)
     * Only suggest if user asks for complete narrative overhaul
   
   - If updating **world_lore**:
     * Generally NO dependencies (lore is foundational but standalone)
     * Only suggest if user explicitly asks to integrate lore changes everywhere
   
   - If updating **factions**:
     * Generally NO dependencies (faction definition is standalone)
     * Only if user explicitly asks to update character affiliations
   
   - If updating **characters**:
     * Generally NO dependencies (character definition is standalone)
     * Only if user explicitly asks to integrate character into quests/arcs
   
   - If updating **plot_arcs**:
     * Generally NO dependencies (arc definition is standalone)
     * Only if user explicitly asks to create quests for the arc
   
   - If updating **questlines**:
     * NO dependencies (quests are standalone)

4. **Reasoning**: Explain your decision clearly

5. **Primary Feedback**: Provide specific, actionable feedback for the primary component being updated

## Guidelines

- **Be EXTREMELY conservative**: Only update what the user explicitly asked for
- **Default to NO dependencies**: Let the user request additional changes if needed
- **User intent first**: Focus ONLY on what the user mentioned
- **Minimize cascading changes**: Avoid changing parts the user didn't mention

## Examples

**Example 1:**
User: "Add a faction called The Shadow Council, a secretive organization"
- Primary: factions (explicitly adding a faction)
- Dependent: [] (NONE - just add the faction definition)
- Reasoning: User only asked to add a faction, not to integrate it everywhere
- Keep unchanged: concept, world_lore, characters, plot_arcs, questlines

**Example 2:**
User: "Make the world more dystopian with oppressive governments"
- Primary: world_lore (world setting change)
- Dependent: [] (NONE - update the lore only)
- Reasoning: User asked to change world tone, not regenerate everything
- Keep unchanged: concept, factions, characters, plot_arcs, questlines

**Example 3:**
User: "Add a character named Marcus, a rebel leader"
- Primary: characters (explicit character addition)
- Dependent: [] (NONE - just add the character)
- Reasoning: User asked to add a character, not create quests for them
- Keep unchanged: concept, world_lore, factions, plot_arcs, questlines

**Example 4 (RARE case with dependencies):**
User: "Completely redesign the game concept as a cyberpunk RPG and regenerate all factions, characters, arcs, and quests to match"
- Primary: concept
- Dependent: [world_lore, factions, characters, plot_arcs, questlines]
- Reasoning: User EXPLICITLY asked for complete overhaul of everything

Please analyze the user feedback and provide your structured response.
"""
    
    return prompt


def _format_faction_summary(factions: list) -> str:
    """Quick faction summary"""
    if not factions:
        return "  No factions defined"
    return "\n".join(f"  - {f.get('name', 'Unknown')} (Influence: {f.get('influence_level', 'N/A')})" for f in factions[:5])


def _format_character_summary(characters: list) -> str:
    """Quick character summary"""
    if not characters:
        return "  No characters defined"
    return "\n".join(f"  - {c.get('name', 'Unknown')} ({c.get('role', 'N/A')})" for c in characters[:5])
