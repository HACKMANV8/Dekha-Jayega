"""Character generation node for SagaAgent."""
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from SagaAgent.models.character import GameCharacter
from SagaAgent.utils.llm_service import LLMService
from SagaAgent.utils.state import SagaState


def generate_characters_node(state: SagaState) -> Dict[str, Any]:
    """Generate game characters based on concept, factions, and world."""
    concept = state.get("concept", {})
    world_lore = state.get("world_lore", {})
    factions = state.get("factions", [])
    feedback = state.get("characters_feedback", "")
    
    system_prompt = """You are a character designer creating memorable game characters.
Generate characters with strong visual identity, clear motivations, and gameplay role."""

    faction_summary = ", ".join([f['faction_name'] for f in factions]) if factions else "TBD"
    
    human_prompt = f"""Create 3-4 major characters for this game:

**Concept:** {concept.get('title', 'Unknown')}
**World:** {world_lore.get('world_name', 'Unknown')}
**Factions:** {faction_summary}

{f"**Feedback:**\\n{feedback}\\n\\n" if feedback else ""}

Generate detailed character profiles with visual design, personality, gameplay role, and recruitment mechanics."""
    
    llm = LLMService.create_structured_llm(state, GameCharacter, creative=True)
    
    # Generate multiple characters (simplified: generate 3)
    characters = []
    for i in range(3):
        char_doc = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt + f"\n\nCharacter #{i+1}:")
        ])
        characters.append(char_doc.model_dump())
    
    return {
        "characters": characters,
    }
