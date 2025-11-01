"""Concept generation node for SagaAgent."""
import json
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from SagaAgent.models.concept import ConceptDoc
from SagaAgent.utils.llm_service import LLMService
from SagaAgent.utils.state import SagaState


def generate_concept_node(state: SagaState) -> Dict[str, Any]:
    """
    Generate a structured game concept based on topic and research.
    
    Args:
        state: Current SagaState
        
    Returns:
        Updated state dict with concept output
    """
    topic = state.get("topic", "")
    research_summary = state.get("research_summary", "")
    
    # Build the prompt
    system_prompt = """You are a veteran game designer creating a compelling video game concept.
Your task is to generate a complete, structured game concept document that captures
the essential DNA of the game and sets up all downstream narrative elements."""

    if research_summary:
        human_prompt = f"""Based on the following research and topic, create a structured game concept:

**Topic/Idea:** {topic}

**Research Context:**
{research_summary}

Create a complete concept document that incorporates research insights while establishing
the core gameplay loop, mechanics, art style, and unique selling proposition."""
    else:
        human_prompt = f"""Create a structured game concept based on this idea:

**Topic/Idea:** {topic}

Generate a complete concept document that establishes the core gameplay loop, mechanics,
art style, and unique selling proposition."""
    
    # Get LLM with structured output
    llm = LLMService.create_structured_llm(
        state,
        ConceptDoc,
        creative=True
    )
    
    # Generate concept
    concept_doc = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])
    
    # Convert to dict
    concept_dict = concept_doc.model_dump()
    
    # Create markdown version
    concept_md = f"""# Game Concept: {concept_dict['title']}

## Core Information
- **Genre:** {concept_dict['genre']}
- **Target Audience:** {concept_dict['target_audience']}

## Pitch
{concept_dict['elevator_pitch']}

## Core Loop
{concept_dict['core_loop']}

## Key Mechanics
{concept_dict['key_mechanics']}

## Progression
{concept_dict['progression']}

## World Setting
{concept_dict['world_setting']}

## Art Style
{concept_dict['art_style']}

## Monetization
{concept_dict['monetization']}

## Unique Selling Proposition (USP)
{concept_dict['usp']}
"""
    
    return {
        "concept": concept_dict,
        "concept_md": concept_md,
        "workflow_stage": "concept_complete"
    }
