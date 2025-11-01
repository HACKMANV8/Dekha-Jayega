"""Faction generation node for SagaAgent."""
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from SagaAgent.models.faction import GameFaction
from SagaAgent.utils.llm_service import LLMService
from SagaAgent.utils.state import SagaState


def generate_factions_node(state: SagaState) -> Dict[str, Any]:
    """Generate game factions based on world lore and concept."""
    concept = state.get("concept", {})
    world_lore = state.get("world_lore", {})
    feedback = state.get("factions_feedback", "")
    
    system_prompt = """You are a game designer creating compelling faction systems.
Generate factions that have clear identities, gameplay mechanics, and conflict potential."""

    human_prompt = f"""Create 2-3 major factions for this game:

**Concept:** {concept.get('title', 'Unknown')}
**World:** {world_lore.get('world_name', 'Unknown')}
**Conflicts:** {world_lore.get('conflicts_tensions', 'Unknown')}

{f"**Feedback:**\\n{feedback}\\n\\n" if feedback else ""}

Generate detailed faction profiles with identity, leadership, gameplay integration, and conflict systems."""
    
    llm = LLMService.create_structured_llm(state, GameFaction, creative=True)
    
    # Generate multiple factions (simplified: generate 2)
    factions = []
    for i in range(2):
        faction_doc = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt + f"\n\nFaction #{i+1}:")
        ])
        factions.append(faction_doc.model_dump())
    
    return {
        "factions": factions,
    }
