"""Plot arc generation node for SagaAgent."""
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from SagaAgent.models.plot import PlotArc
from SagaAgent.utils.llm_service import LLMService
from SagaAgent.utils.state import SagaState


def generate_plot_arcs_node(state: SagaState) -> Dict[str, Any]:
    """Generate plot arcs based on concept, characters, and world."""
    concept = state.get("concept", {})
    world_lore = state.get("world_lore", {})
    characters = state.get("characters", [])
    feedback = state.get("plot_arcs_feedback", "")
    
    system_prompt = """You are a narrative designer creating compelling branching story arcs.
Generate plot arcs with clear dramatic structure, branching choices, and multiple endings."""

    char_summary = ", ".join([c.get('character_name', 'Unknown') for c in characters[:3]]) if characters else "TBD"
    
    human_prompt = f"""Create 1-2 major plot arcs for this game:

**Concept:** {concept.get('title', 'Unknown')}
**World:** {world_lore.get('world_name', 'Unknown')}
**Key Characters:** {char_summary}

{f"**Feedback:**\\n{feedback}\\n\\n" if feedback else ""}

Generate detailed plot arcs with three-act structure, branching narrative, and multiple endings."""
    
    llm = LLMService.create_structured_llm(state, PlotArc, creative=True)
    
    # Generate plot arcs (simplified: generate 1)
    plot_arcs = []
    arc_doc = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])
    plot_arcs.append(arc_doc.model_dump())
    
    return {
        "plot_arcs": plot_arcs,
    }
