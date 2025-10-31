"""
Supervisor State Definition

This module defines the unified state for the Supervisor Architecture that
orchestrates both the Research agent and ArcueAgent workflows.
"""

import operator
from typing import TypedDict, List, Dict, Any, Annotated, Sequence
from typing_extensions import NotRequired
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class SupervisorState(TypedDict):
    """
    Unified state for the Supervisor Architecture.
    
    This state combines elements from both the Research agent and ArcueAgent,
    allowing the supervisor to orchestrate a complete workflow from research
    to creative content generation.
    """
    # === User Input ===
    topic: str  # The main topic/idea provided by user
    log_line: NotRequired[str]  # Story logline (can be generated from topic + research)
    
    # === Workflow Control ===
    workflow_stage: str  # Current stage: "initial", "research", "writing", "complete"
    needs_research: bool  # Whether research is needed before writing
    research_complete: bool  # Whether research has been completed
    writing_complete: bool  # Whether writing has been completed
    
    # === Research Results ===
    research_topic: NotRequired[str]  # Specific research question
    compressed_research: NotRequired[str]  # Compressed research findings
    raw_notes: Annotated[List[str], operator.add]  # Raw research notes
    researcher_messages: Annotated[Sequence[BaseMessage], add_messages]  # Research conversation
    
    # === Messages ===
    messages: Annotated[List[BaseMessage], add_messages]  # Main conversation thread
    llm_calls: NotRequired[int]  # Track LLM usage
    
    # === Story Elements (from ArcueAgent) ===
    draft: NotRequired[str]
    title: NotRequired[str]
    genre: NotRequired[str]
    themes: NotRequired[List[str]]
    tone: NotRequired[str]
    target_audience: NotRequired[str]
    unique_selling_point: NotRequired[str]
    
    # === Story Components ===
    characters: NotRequired[List[Dict[str, Any]]]
    plot_points: NotRequired[List[Dict[str, Any]]]
    logline: NotRequired[str]
    subplot_threads: NotRequired[List[str]]
    dramatic_irony: NotRequired[str]
    dialogue_scenes: NotRequired[List[Dict[str, Any]]]
    locations: NotRequired[List[Dict[str, Any]]]
    scenes: NotRequired[List[Dict[str, Any]]]
    
    # === Final Outputs ===
    final_script: NotRequired[Dict[str, Any]]
    export_path: NotRequired[str]
    export_timestamp: NotRequired[str]
    json_files: NotRequired[List[str]]
    
    # === Feedback Fields ===
    draft_feedback: NotRequired[str]
    characters_feedback: NotRequired[str]
    plot_feedback: NotRequired[str]
    dialogue_feedback: NotRequired[str]
    locations_feedback: NotRequired[str]
    scenes_feedback: NotRequired[str]
    
    # === Model Controls ===
    model: NotRequired[str]
    model_temperature: NotRequired[float]
    random_seed: NotRequired[int]
    
    # === Film Configuration ===
    film_length_seconds: NotRequired[int]
    number_of_scenes: NotRequired[int]

    # === Ad Mode Configuration ===
    ad_mode: NotRequired[bool]
    ad_total_seconds: NotRequired[int]
    ad_scene_seconds: NotRequired[int]
    ad_brand: NotRequired[str]
    ad_product: NotRequired[str]
    ad_goal: NotRequired[str]
    ad_audience: NotRequired[str]
    ad_tone: NotRequired[str]
    ad_offer: NotRequired[str]
    ad_constraints: NotRequired[str]
    ad_brief: NotRequired[Dict[str, Any]]
    ad_scenes: NotRequired[List[Dict[str, Any]]]
    ad_brief_feedback: NotRequired[str]
    ad_scenes_feedback: NotRequired[str]

