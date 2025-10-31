"""Questline generation node for SagaAgent."""
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from SagaAgent.models.quest import Questline
from SagaAgent.utils.llm_service import LLMService
from SagaAgent.utils.state import SagaState


def generate_questlines_node(state: SagaState) -> Dict[str, Any]:
    """Generate questlines based on plot arcs, characters, and factions."""
    concept = state.get("concept", {})
    plot_arcs = state.get("plot_arcs", [])
    characters = state.get("characters", [])
    factions = state.get("factions", [])
    feedback = state.get("questlines_feedback", "")
    
    system_prompt = """You are a quest designer creating engaging game quests.
Generate questlines with clear objectives, branching paths, and meaningful player choices."""

    plot_summary = plot_arcs[0].get('arc_title', 'Unknown') if plot_arcs else 'Unknown'
    char_summary = ", ".join([c.get('character_name', 'Unknown') for c in characters[:2]]) if characters else "TBD"
    
    human_prompt = f"""Create 3-5 questlines for this game:

**Concept:** {concept.get('title', 'Unknown')}
**Main Plot:** {plot_summary}
**Key NPCs:** {char_summary}

{f"**Feedback:**\\n{feedback}\\n\\n" if feedback else ""}

Generate detailed questlines with discovery hooks, branching objectives, and varied rewards."""
    
    llm = LLMService.create_structured_llm(state, Questline, creative=True)
    
    # Generate questlines (simplified: generate 2)
    questlines = []
    for i in range(2):
        quest_doc = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt + f"\n\nQuestline #{i+1}:")
        ])
        questlines.append(quest_doc.model_dump())
    
    return {
        "questlines": questlines,
    }
