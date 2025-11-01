"""SagaAgent: Multi-stage narrative generation with human-in-the-loop interrupts."""
import os
import sys
import sqlite3
import pprint
import warnings
from langgraph.checkpoint.memory import MemorySaver

# Suppress Pydantic warnings about additionalProperties (common with Gemini models)
warnings.filterwarnings("ignore", message=".*additionalProperties.*")

# Force UTF-8 encoding for console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
try:
    from langgraph.checkpoint.sqlite import SqliteSaver
except Exception:
    SqliteSaver = None

from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph
from SagaAgent.utils.state import SagaState
from SagaAgent.config import AgentConfig, ExportConfig
from SagaAgent.services.export_service import ExportService
from SagaAgent.nodes import (
    generate_concept_node,
    generate_world_lore_node,
    generate_factions_node,
    generate_characters_node,
    generate_plot_arcs_node,
    generate_questlines_node,
)

load_dotenv()

# === CHECKPOINT & MEMORY CONFIGURATION ===
checkpoint_db_path = os.environ.get("CHECKPOINT_DB_PATH", ExportConfig.CHECKPOINT_DB_PATH)
if SqliteSaver is not None:
    try:
        memory = SqliteSaver(sqlite3.connect(checkpoint_db_path))
    except Exception:
        memory = MemorySaver()
else:
    memory = MemorySaver()

# === GRAPH CONSTRUCTION ===
workflow = StateGraph(SagaState)

# Add all narrative generation nodes
workflow.add_node("concept", generate_concept_node)
workflow.add_node("world_lore", generate_world_lore_node)
workflow.add_node("factions", generate_factions_node)
workflow.add_node("characters", generate_characters_node)
workflow.add_node("plot_arcs", generate_plot_arcs_node)
workflow.add_node("questlines", generate_questlines_node)

# Build edge chain: concept → lore → factions → characters → plot → quests → END
workflow.add_edge(START, "concept")
workflow.add_edge("concept", "world_lore")
workflow.add_edge("world_lore", "factions")
workflow.add_edge("factions", "characters")
workflow.add_edge("characters", "plot_arcs")
workflow.add_edge("plot_arcs", "questlines")
workflow.add_edge("questlines", END)

# Compile with interrupts after each major stage for HITL feedback
saga_agent = workflow.compile(
    checkpointer=memory,
    interrupt_after=['concept', 'world_lore', 'factions', 'characters', 'plot_arcs', 'questlines']
)

# === HELPER FUNCTIONS ===
def _write_markdown(file_name: str, content) -> None:
    """Write content to markdown file."""
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(pprint.pformat(content))


def _handle_interrupt(
    stage_header: str,
    state_key: str,
    output_file: str,
    feedback_prompt: str,
    feedback_key: str,
    node_func,
    current_state: dict,
    config: dict,
    auto_continue: bool
) -> dict:
    """Handle HITL interrupt with optional feedback."""
    print(f"\n--- {stage_header} ---")
    value = current_state.get(state_key, [] if state_key.endswith('s') else None)
    pprint.pprint(value)
    _write_markdown(output_file, value)

    user_feedback = ""
    if not auto_continue:
        try:
            user_feedback = input(f"\n{feedback_prompt}").strip()
        except EOFError:
            user_feedback = ""

    if user_feedback:
        revision = node_func({**current_state, feedback_key: user_feedback})
        saga_agent.update_state(config, revision)
        current_state.update(revision)
        value = current_state.get(state_key, value)
        pprint.pprint(value)
        _write_markdown(output_file, value)

    return current_state


# === PARALLEL EXECUTION FUNCTIONS ===
def run_parallel_workflow(agent_config: AgentConfig, config: dict, inputs: dict) -> dict:
    """
    Run saga generation with parallel execution for independent nodes.
    This provides significant speedup (40-50%) by running world_lore, factions,
    and characters in parallel after the concept is complete.
    """
    from SagaAgent.utils.parallel_execution import run_parallel_generation
    
    print("\n" + "="*70)
    print("[START] PARALLEL WORKFLOW ENABLED")
    print(f"   Max workers: {agent_config.parallel_max_workers}")
    print(f"   Batch size: {agent_config.parallel_batch_size}")
    print("="*70)
    
    # Prepare state with config
    state = {**inputs, **agent_config.to_state_dict()}
    
    # Define the parallel nodes (world_lore, factions, characters can run in parallel)
    parallel_nodes = {
        "world_lore": generate_world_lore_node,
        "factions": generate_factions_node,
        "characters": generate_characters_node
    }
    
    # Run parallel generation
    try:
        final_state = run_parallel_generation(
            state=state,
            concept_func=generate_concept_node,
            parallel_nodes=parallel_nodes,
            plot_func=generate_plot_arcs_node,
            quest_func=generate_questlines_node,
            max_workers=agent_config.parallel_max_workers,
            retry_sequential=agent_config.parallel_retry_sequential
        )
        
        # Debug: Show state contents before export
        print("\n" + "="*70)
        print("[STATS] FINAL STATE BEFORE EXPORT")
        print("="*70)
        concept = final_state.get('concept', {})
        title = concept.get('title', 'MISSING') if isinstance(concept, dict) else 'MISSING'
        print(f"   Title: {title}")
        print(f"   Topic: {final_state.get('topic', 'MISSING')}")
        print(f"   World Lore: {'present' if final_state.get('world_lore') else 'MISSING'}")
        print(f"   Factions: {len(final_state.get('factions', []))} items")
        print(f"   Characters: {len(final_state.get('characters', []))} items")
        print(f"   Plot Arcs: {len(final_state.get('plot_arcs', []))} items")
        print(f"   Questlines: {len(final_state.get('questlines', []))} items")
        print("="*70)
        
        # Run export (JSON and Markdown)
        print("\n--- EXPORTING SAGA ---")
        export_result = ExportService.export_all_json(final_state)
        final_state.update(export_result)
        
        md_result = ExportService.export_all_markdown(final_state)
        final_state.update(md_result)
        
        return final_state
        
    except Exception as e:
        print(f"\n[ERROR] Parallel workflow failed: {e}")
        if agent_config.parallel_retry_sequential:
            print("WARNING: Falling back to sequential workflow...")
            return None  # Return None to trigger sequential fallback
        raise


# === MAIN EXECUTION ===
def main() -> None:
    """Main execution for SagaAgent."""
    agent_config = AgentConfig.from_env()
    config = {"configurable": {"thread_id": agent_config.thread_id}}

    print("="*70)
    print("SAGAAGENT: NARRATIVE GENERATION PIPELINE")
    print("="*70)
    print(f"Topic: {agent_config.topic}")
    print(f"Auto-Continue: {agent_config.auto_continue}")
    print(f"Parallel Execution: {agent_config.parallel_execution}")
    print("="*70)

    # Handle checkpoint history listing
    if agent_config.list_history:
        try:
            history = list(saga_agent.get_state_history(config))
            if history:
                print("\nCheckpoint history (most recent first):")
                for idx, snap in enumerate(history, start=1):
                    ck_cfg = snap.config.get("configurable", {}) if isinstance(snap.config, dict) else {}
                    ck_id = ck_cfg.get("checkpoint_id", "")
                    next_nodes = getattr(snap, "next", ())
                    keys = sorted(list(snap.values.keys())) if hasattr(snap, "values") else []
                    created_at = getattr(snap, "created_at", None)
                    print(f"{idx:02d}. checkpoint_id={ck_id} created_at={created_at} next={next_nodes} keys={keys}")
            else:
                print("\nNo checkpoints found for this thread.")
        except Exception as e:
            print(f"Failed to list checkpoint history: {e}")

    # Resume from checkpoint or start fresh
    if agent_config.checkpoint_id:
        config["configurable"]["checkpoint_id"] = agent_config.checkpoint_id
        inputs = None
        # Update state with config if resuming from checkpoint
        if agent_config.model_temperature is not None or agent_config.random_seed is not None:
            update_values = agent_config.to_state_dict()
            try:
                saga_agent.update_state(config, update_values)
            except Exception as e:
                print(f"Warning: could not update state with config: {e}")
    else:
        topic = agent_config.topic or input("Enter the topic for your saga: ")
        inputs = {
            "topic": topic,
            "messages": []
        }
        # Add optional research summary if provided
        if agent_config.research_summary:
            inputs["research_summary"] = agent_config.research_summary
        # Add config options
        inputs.update(agent_config.to_state_dict())

    # Check if parallel execution is enabled and AUTO_CONTINUE is true
    # Parallel execution only works with AUTO_CONTINUE=true (no interrupts)
    use_parallel = (
        agent_config.parallel_execution and 
        agent_config.auto_continue and 
        inputs is not None  # Must have inputs (not checkpoint resume)
    )
    
    if use_parallel:
        try:
            final_state = run_parallel_workflow(agent_config, config, inputs)
            
            # If parallel workflow succeeded, we're done
            if final_state:
                export_path = final_state.get("export_path", ExportConfig.EXPORT_DIR)
                json_files = final_state.get("json_files", [])
                markdown_files = final_state.get("markdown_files", [])
                
                print(f"\n--- SAGA GENERATION COMPLETE ---")
                print(f"All saga components have been compiled and exported to: {export_path}")
                if json_files:
                    print(f"\nJSON exports ({len(json_files)} files):")
                    for json_file in json_files:
                        print(f"  - {json_file}")
                if markdown_files:
                    print(f"\nMarkdown exports ({len(markdown_files)} files):")
                    for md_file in markdown_files:
                        print(f"  - {md_file}")
                
                return
        except Exception as e:
            print(f"WARNING: Parallel execution failed: {e}")
            if agent_config.parallel_retry_sequential:
                print("WARNING: Falling back to sequential workflow...")
            else:
                raise

    # Run workflow with HITL interrupts (sequential)
    print("\n[START] SAGA GENERATION (Sequential with interrupts)")
    print("="*70)

    # Concept stage
    current_state = saga_agent.invoke(inputs, config=config)
    current_state = _handle_interrupt(
        "CONCEPT REVIEW",
        "concept",
        "saga_concept.json",
        "Provide feedback on concept (or press Enter to continue): ",
        "concept_feedback",
        generate_concept_node,
        current_state,
        config,
        agent_config.auto_continue
    )

    # World Lore stage
    current_state = saga_agent.invoke(None, config=config)
    current_state = _handle_interrupt(
        "WORLD LORE REVIEW",
        "world_lore",
        "saga_world_lore.json",
        "Provide feedback on world lore (or press Enter to continue): ",
        "world_lore_feedback",
        generate_world_lore_node,
        current_state,
        config,
        agent_config.auto_continue
    )

    # Factions stage
    current_state = saga_agent.invoke(None, config=config)
    current_state = _handle_interrupt(
        "FACTIONS REVIEW",
        "factions",
        "saga_factions.json",
        "Provide feedback on factions (or press Enter to continue): ",
        "factions_feedback",
        generate_factions_node,
        current_state,
        config,
        agent_config.auto_continue
    )

    # Characters stage
    current_state = saga_agent.invoke(None, config=config)
    current_state = _handle_interrupt(
        "CHARACTERS REVIEW",
        "characters",
        "saga_characters.json",
        "Provide feedback on characters (or press Enter to continue): ",
        "characters_feedback",
        generate_characters_node,
        current_state,
        config,
        agent_config.auto_continue
    )

    # Plot Arcs stage
    current_state = saga_agent.invoke(None, config=config)
    current_state = _handle_interrupt(
        "PLOT ARCS REVIEW",
        "plot_arcs",
        "saga_plot_arcs.json",
        "Provide feedback on plot arcs (or press Enter to continue): ",
        "plot_arcs_feedback",
        generate_plot_arcs_node,
        current_state,
        config,
        agent_config.auto_continue
    )

    # Questlines stage
    current_state = saga_agent.invoke(None, config=config)
    current_state = _handle_interrupt(
        "QUESTLINES REVIEW",
        "questlines",
        "saga_questlines.json",
        "Provide feedback on questlines (or press Enter to complete): ",
        "questlines_feedback",
        generate_questlines_node,
        current_state,
        config,
        agent_config.auto_continue
    )

    # Export all stages
    print("\n--- EXPORTING SAGA ---")
    export_result = ExportService.export_all_json(current_state)
    current_state.update(export_result)
    
    md_result = ExportService.export_all_markdown(current_state)
    current_state.update(md_result)

    # Final completion
    print("\n" + "="*70)
    print("[OK] SAGA GENERATION COMPLETE")
    print("="*70)
    concept = current_state.get('concept', {})
    title = concept.get('title', 'N/A') if isinstance(concept, dict) else 'N/A'
    world_lore = current_state.get('world_lore', {})
    world_name = world_lore.get('world_name', 'N/A') if isinstance(world_lore, dict) else 'N/A'
    
    print(f"\nGenerated Content:")
    print(f"  - Concept: {title}")
    print(f"  - World Lore: {world_name}")
    print(f"  - Factions: {len(current_state.get('factions', []))} created")
    print(f"  - Characters: {len(current_state.get('characters', []))} created")
    print(f"  - Plot Arcs: {len(current_state.get('plot_arcs', []))} created")
    print(f"  - Questlines: {len(current_state.get('questlines', []))} created")
    
    export_path = current_state.get("export_path", ExportConfig.EXPORT_DIR)
    print(f"\nExported to: {export_path}")
    print("="*70)


if __name__ == "__main__":
    main()
