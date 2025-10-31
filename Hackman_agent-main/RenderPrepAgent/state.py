"""State definition for RenderPrepAgent workflow."""
import operator
from typing import TypedDict, List, Dict, Any, Annotated, Optional
from typing_extensions import NotRequired
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class RenderPrepState(TypedDict):
    """
    State for RenderPrepAgent workflow.
    
    Takes Saga/Orchestrator output and transforms it into optimized image prompts.
    """
    # === Input from Saga/Orchestrator ===
    saga_data: Dict[str, Any]  # Complete saga output (concept, world_lore, characters, etc.)
    input_path: NotRequired[str]  # Path to input JSON file
    
    # === Workflow Control ===
    workflow_stage: NotRequired[str]  # Current stage tracking
    quality_preset: NotRequired[str]  # Quality preset: draft, standard, premium
    generate_images: NotRequired[bool]  # Whether to actually generate images via API
    
    # === Configuration ===
    model_name: NotRequired[str]  # LLM model for prompt engineering
    model_temperature: NotRequired[float]  # Temperature for generation
    
    # === Messages ===
    messages: Annotated[List[BaseMessage], add_messages]  # Conversation thread
    
    # === Character Visual Prompts ===
    character_prompts: Annotated[List[Dict[str, Any]], operator.add]
    character_prompts_feedback: NotRequired[str]
    
    # === Environment Visual Prompts ===
    environment_prompts: Annotated[List[Dict[str, Any]], operator.add]
    environment_prompts_feedback: NotRequired[str]
    
    # === Item Visual Prompts ===
    item_prompts: Annotated[List[Dict[str, Any]], operator.add]
    item_prompts_feedback: NotRequired[str]
    
    # === Storyboard Frame Prompts ===
    storyboard_prompts: Annotated[List[Dict[str, Any]], operator.add]
    storyboard_prompts_feedback: NotRequired[str]
    
    # === Generated Images (if generate_images=True) ===
    generated_images: NotRequired[List[Dict[str, Any]]]  # Image URLs/metadata from API
    
    # === Export Results ===
    export_path: NotRequired[str]  # Directory where prompts are exported
    export_timestamp: NotRequired[str]  # Export timestamp
    json_files: NotRequired[List[str]]  # List of exported JSON files
    markdown_files: NotRequired[List[str]]  # List of exported Markdown files
    
    # === Error Tracking ===
    errors: NotRequired[List[str]]  # Any errors encountered during generation

