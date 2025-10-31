"""State definition for SagaAgent workflow."""
import operator
from typing import TypedDict, List, Dict, Any, Annotated, Optional
from typing_extensions import NotRequired
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class SagaState(TypedDict):
    """
    Unified state for SagaAgent workflow.
    
    Covers narrative generation pipeline:
    Concept → World Lore → Factions → Characters → Plot Arcs → Questlines → RenderPrep
    """
    # === User Input ===
    topic: str  # Main topic/idea for the saga
    research_summary: NotRequired[str]  # Optional research context from supervisor
    
    # === Workflow Control ===
    workflow_stage: NotRequired[str]  # Current stage tracking
    renders_ready: NotRequired[bool]  # Whether render prep can proceed
    
    # === Messages ===
    messages: Annotated[List[BaseMessage], add_messages]  # Conversation thread
    
    # === Concept Stage ===
    concept: NotRequired[Dict[str, Any]]  # GameConcept output
    concept_feedback: NotRequired[str]  # User feedback on concept
    concept_md: NotRequired[str]  # Markdown version of concept
    
    # === World Lore Stage ===
    world_lore: NotRequired[Dict[str, Any]]  # WorldLore output
    world_lore_feedback: NotRequired[str]  # User feedback on lore
    world_lore_md: NotRequired[str]  # Markdown version of lore
    
    # === Factions Stage ===
    factions: Annotated[List[Dict[str, Any]], operator.add]  # List of GameFaction outputs
    factions_feedback: NotRequired[str]  # User feedback on factions
    
    # === Characters Stage ===
    characters: Annotated[List[Dict[str, Any]], operator.add]  # List of GameCharacter outputs
    characters_feedback: NotRequired[str]  # User feedback on characters
    
    # === Plot Arcs Stage ===
    plot_arcs: Annotated[List[Dict[str, Any]], operator.add]  # List of PlotArc outputs
    plot_arcs_feedback: NotRequired[str]  # User feedback on plot arcs
    
    # === Questlines Stage ===
    questlines: Annotated[List[Dict[str, Any]], operator.add]  # List of Questline outputs
    questlines_feedback: NotRequired[str]  # User feedback on questlines
    
    # === General Feedback ===
    feedback: NotRequired[Dict[str, str]]  # Aggregated feedback dictionary
    
    # === Model Controls ===
    model: NotRequired[str]
    model_temperature: NotRequired[float]
    random_seed: NotRequired[int]
    
    # === Render Prep Output ===
    render_prompts: NotRequired[Dict[str, Any]]  # RenderPrepOutput data
    render_ready: NotRequired[bool]
    
    # === Metadata ===
    metadata: NotRequired[Dict[str, Any]]  # Additional tracking info
    export_path: NotRequired[str]  # Export directory path
    export_timestamp: NotRequired[str]  # Export timestamp
    json_files: NotRequired[List[str]]  # List of exported JSON files
    markdown_files: NotRequired[List[str]]  # List of exported Markdown files
    
    # === Parallel Execution Settings ===
    parallel_execution: NotRequired[bool]
    parallel_max_workers: NotRequired[int]
    parallel_batch_size: NotRequired[int]
    parallel_retry_sequential: NotRequired[bool]
