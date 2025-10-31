"""
RenderPrepAgent: Main agent module with LangGraph integration.

Transforms Saga/Orchestrator narrative outputs into optimized image generation prompts
using professional prompt engineering techniques.
"""
import os
import sys
import json
import warnings
from typing import Dict, Any, Optional

# Suppress Pydantic warnings
warnings.filterwarnings("ignore", message=".*additionalProperties.*")

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from RenderPrepAgent.state import RenderPrepState
from RenderPrepAgent.config import AgentConfig, RenderConfig
from RenderPrepAgent.services.export_service import RenderExportService
from RenderPrepAgent.nodes import (
    generate_character_prompts_node,
    generate_environment_prompts_node,
    generate_item_prompts_node,
    generate_storyboard_prompts_node,
    generate_images_node,
)

load_dotenv()

# === CHECKPOINT & MEMORY CONFIGURATION ===
memory = MemorySaver()

# === GRAPH CONSTRUCTION ===
workflow = StateGraph(RenderPrepState)

# Add all prompt generation nodes
workflow.add_node("character_prompts", generate_character_prompts_node)
workflow.add_node("environment_prompts", generate_environment_prompts_node)
workflow.add_node("item_prompts", generate_item_prompts_node)
workflow.add_node("storyboard_prompts", generate_storyboard_prompts_node)
workflow.add_node("generate_images", generate_images_node)

# Build edge chain
workflow.add_edge(START, "character_prompts")
workflow.add_edge("character_prompts", "environment_prompts")
workflow.add_edge("environment_prompts", "item_prompts")
workflow.add_edge("item_prompts", "storyboard_prompts")
workflow.add_edge("storyboard_prompts", "generate_images")
workflow.add_edge("generate_images", END)

# Compile workflow
render_prep_agent = workflow.compile(checkpointer=memory)


def load_saga_data(input_path: str) -> Dict[str, Any]:
    """
    Load saga data from JSON file or directory.
    
    Args:
        input_path: Path to JSON file or directory with saga exports
    
    Returns:
        Dict with consolidated saga data
    """
    if os.path.isfile(input_path):
        # Single file
        with open(input_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    elif os.path.isdir(input_path):
        # Directory with multiple JSON files
        saga_data = {}
        
        for filename in os.listdir(input_path):
            if not filename.endswith(".json"):
                continue
            
            filepath = os.path.join(input_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # Merge data based on filename
                if "concept" in filename:
                    saga_data["concept"] = data.get("concept", data)
                elif "world_lore" in filename:
                    saga_data["world_lore"] = data.get("world_lore", data)
                elif "factions" in filename:
                    saga_data["factions"] = data.get("factions", data)
                elif "characters" in filename:
                    saga_data["characters"] = data.get("characters", data)
                elif "plot_arcs" in filename:
                    saga_data["plot_arcs"] = data.get("plot_arcs", data)
                elif "questlines" in filename:
                    saga_data["questlines"] = data.get("questlines", data)
        
        return saga_data
    
    else:
        raise FileNotFoundError(f"Input path not found: {input_path}")


def run_render_prep(
    saga_data: Dict[str, Any],
    agent_config: AgentConfig,
    input_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run complete render prep workflow.
    
    Args:
        saga_data: Saga/Orchestrator output data
        agent_config: Agent configuration
        input_path: Optional path to input file
    
    Returns:
        Final state with all prompts and exports
    """
    print("="*70)
    print("RENDER PREP AGENT: IMAGE PROMPT GENERATION")
    print("="*70)
    
    # Prepare initial state
    inputs = {
        "saga_data": saga_data,
        "messages": [],
        **agent_config.to_state_dict()
    }
    
    if input_path:
        inputs["input_path"] = input_path
    
    config = {"configurable": {"thread_id": agent_config.thread_id}}
    
    # Run workflow
    print("\n[START] Generating image prompts...\n")
    
    try:
        final_state = render_prep_agent.invoke(inputs, config=config)
        
        # Export all prompts
        print("\n--- EXPORTING PROMPTS ---")
        export_result = RenderExportService.export_all(final_state)
        final_state.update(export_result)
        
        # Print summary
        print("\n" + "="*70)
        print("[COMPLETE] RENDER PREP FINISHED")
        print("="*70)
        
        concept = saga_data.get("concept", {})
        title = concept.get("title", "Untitled") if isinstance(concept, dict) else "Untitled"
        
        print(f"\nProject: {title}")
        print(f"Quality Preset: {agent_config.quality_preset}")
        print(f"\nGenerated Prompts:")
        print(f"  - Characters: {len(final_state.get('character_prompts', []))}")
        print(f"  - Environments: {len(final_state.get('environment_prompts', []))}")
        print(f"  - Items: {len(final_state.get('item_prompts', []))}")
        print(f"  - Storyboards: {len(final_state.get('storyboard_prompts', []))}")
        print(f"  - Total: {len(final_state.get('character_prompts', [])) + len(final_state.get('environment_prompts', [])) + len(final_state.get('item_prompts', [])) + len(final_state.get('storyboard_prompts', []))}")
        
        if final_state.get("generate_images"):
            print(f"\nGenerated Images: {len(final_state.get('generated_images', []))}")
        
        export_path = final_state.get("export_path", RenderConfig.EXPORT_DIR)
        print(f"\nExported to: {export_path}")
        print("="*70)
        
        return final_state
    
    except Exception as e:
        print(f"\n✗ ERROR: Render prep failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


def main() -> None:
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="RenderPrepAgent: Generate optimized image prompts from Saga output"
    )
    parser.add_argument(
        "input",
        help="Path to saga JSON file or directory with saga exports"
    )
    parser.add_argument(
        "--quality",
        choices=["draft", "standard", "premium"],
        default="standard",
        help="Quality preset for image generation (default: standard)"
    )
    parser.add_argument(
        "--generate-images",
        action="store_true",
        help="Actually generate images via Nano Banana API (requires API key)"
    )
    parser.add_argument(
        "--thread-id",
        default="render_prep_default",
        help="Thread ID for checkpoint persistence"
    )
    
    args = parser.parse_args()
    
    # Load agent config
    agent_config = AgentConfig(
        thread_id=args.thread_id,
        quality_preset=args.quality,
        generate_images=args.generate_images,
        auto_continue=True
    )
    
    # Load saga data
    print(f"Loading saga data from: {args.input}")
    saga_data = load_saga_data(args.input)
    
    # Validate data
    if not saga_data.get("concept"):
        print("⚠ WARNING: No concept found in saga data")
    if not saga_data.get("characters"):
        print("⚠ WARNING: No characters found in saga data")
    
    # Run render prep
    run_render_prep(saga_data, agent_config, input_path=args.input)


if __name__ == "__main__":
    main()

