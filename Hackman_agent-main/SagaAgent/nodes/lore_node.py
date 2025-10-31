"""World lore generation node for SagaAgent."""
from typing import Dict, Any, List, Literal
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage
from SagaAgent.models.lore import WorldLore
from SagaAgent.utils.llm_service import LLMService
from SagaAgent.utils.state import SagaState


class _LoreReview(BaseModel):
    decision: Literal["accept", "revise"]
    feedback: List[str]


def _render_lore_markdown(lore_dict: Dict[str, Any]) -> str:
    return f"""# World Lore: {lore_dict['world_name']}

## Overview
{lore_dict['setting_overview']}

## Geography
{lore_dict['geography']}

## Climate & Cosmology
{lore_dict['climate_cosmology']}

## Flora & Fauna
{lore_dict['flora_fauna']}

## Creation Myth
{lore_dict['creation_myth']}

## Historical Eras
{lore_dict['historical_eras']}

## Current Age
{lore_dict['current_age']}

## Civilizations
{lore_dict['civilizations']}

## Social Structures
{lore_dict['social_structures']}

## Religions & Beliefs
{lore_dict['religions_beliefs']}

## Magic/Technology System
{lore_dict['magic_or_technology']}

## Economy & Resources
{lore_dict['economy_resources']}

## Conflicts & Tensions
{lore_dict['conflicts_tensions']}

## Mysteries & Legends
{lore_dict['mysteries_legends']}

## Story Potential
{lore_dict['story_potential']}
"""


def _evaluate_lore(state: SagaState, lore_md: str) -> _LoreReview:
    reviewer = LLMService.create_llm(state, creative=False)
    system_prompt = (
        "You are a strict game design critic. Respond ONLY with JSON containing keys: "
        "decision (accept|revise) and feedback (array of specific bullet strings)."
    )
    human_prompt = f"""Review the following world lore for originality, coherence, specificity, and internal consistency.
Return only JSON.

LORE:
{lore_md}
"""
    try:
        resp = reviewer.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])
        import json as _json
        raw = resp.content if isinstance(resp.content, str) else str(resp.content)
        raw = raw.strip()
        if raw.startswith("```") and raw.endswith("```"):
            raw = raw.strip("`\n ")
            if raw.startswith("json"):
                raw = raw[4:]
        data = _json.loads(raw)
        return _LoreReview(**data)
    except Exception:
        return _LoreReview(decision="accept", feedback=["Auto-accepted due to parsing issue."])



def generate_world_lore_node(state: SagaState) -> Dict[str, Any]:
    """Generate world lore based on concept and research with reviewer loop."""
    concept = state.get("concept", {})
    research_summary = state.get("research_summary", "")
    human_feedback = state.get("world_lore_feedback", "")

    system_prompt = (
        "You are a master worldbuilder creating deep, coherent fantasy/sci-fi universes. "
        "Return content that can be parsed into the WorldLore schema fields."
    )

    max_iterations = 5
    iteration = 0
    accumulated_feedback = human_feedback.strip()
    lore_dict: Dict[str, Any] = {}

    while iteration < max_iterations:
        human_prompt = f"""Create a world lore document for this game concept:

**Concept:** {concept.get('title', 'Unknown')}
**Genre:** {concept.get('genre', 'Unknown')}
**Setting:** {concept.get('world_setting', 'Unknown')}

{f"**Research Context:**\n{research_summary}\n\n" if research_summary else ""}
{f"**Revision Feedback:**\n{accumulated_feedback}\n\n" if accumulated_feedback else ""}

Generate a comprehensive, internally consistent world lore document."""

        llm = LLMService.create_structured_llm(state, WorldLore, creative=True)
        lore_doc = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])
        lore_dict = lore_doc.model_dump()

        lore_md = _render_lore_markdown(lore_dict)
        review = _evaluate_lore(state, lore_md)
        if review.decision == "accept":
            break

        accumulated_feedback = (accumulated_feedback + "\n" if accumulated_feedback else "") + "\n".join(review.feedback)
        iteration += 1

    lore_md = _render_lore_markdown(lore_dict)

    return {
        "world_lore": lore_dict,
        "world_lore_md": lore_md,
    }
