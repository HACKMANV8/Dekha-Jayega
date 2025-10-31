"""
Supervisor Agent Implementation

This module implements the Supervisor Architecture that orchestrates
the Research agent and ArcueAgent workflows into a cohesive end-to-end system.
"""

import os
from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model

from supervisor_state import SupervisorState
from Research.research_agent import researcher_agent
from Research.state_research import ResearcherState
from ArcueAgent.agent import story_agent
from ArcueAgent.utils.state import UnifiedState
from ArcueAgent.models.draft import InitialDraft
from ArcueAgent.config import ModelConfig
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()


# === STRUCTURED OUTPUT SCHEMAS ===

class SupervisorDecision(BaseModel):
    """Schema for supervisor routing decisions."""
    needs_research: bool = Field(
        description="Whether research is needed before proceeding to creative writing. "
        "Set to True if the topic would benefit from background information, context, "
        "references, or examples. Set to False if the topic is straightforward and "
        "self-contained."
    )
    research_question: str = Field(
        description="If research is needed, formulate a specific research question "
        "that will help gather relevant context for the creative writing task."
    )
    reasoning: str = Field(
        description="Brief explanation of why research is or isn't needed."
    )


# === INITIALIZE MODELS ===

def get_supervisor_model():
    """
    Get supervisor model based on environment variables.
    Priority: SUPERVISOR_MODEL env var > OPENAI_API_KEY > GOOGLE_API_KEY
    Uses ModelConfig for default model selection.
    """
    supervisor_model_name = os.environ.get("SUPERVISOR_MODEL")
    
    if supervisor_model_name:
        # Explicit model specified
        if "gpt" in supervisor_model_name.lower() or "openai" in supervisor_model_name.lower():
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=supervisor_model_name,
                api_key=os.environ.get("OPENAI_API_KEY")
            )
        else:
            # Assume Google model
            return ChatGoogleGenerativeAI(
                model=supervisor_model_name,
                google_api_key=os.environ.get("GOOGLE_API_KEY")
            )
    
    # Auto-select based on available API keys using ModelConfig
    if os.environ.get("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=ModelConfig.get_default_openai_model(),
            api_key=os.environ.get("OPENAI_API_KEY")
        )
    elif os.environ.get("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(
            model=ModelConfig.get_default_google_model(),
            google_api_key=os.environ.get("GOOGLE_API_KEY")
        )
    else:
        raise ValueError("No API keys found. Please set OPENAI_API_KEY or GOOGLE_API_KEY")

supervisor_model = get_supervisor_model()
supervisor_with_structure = supervisor_model.with_structured_output(SupervisorDecision)


# === SUPERVISOR NODES ===

def supervisor_node(state: SupervisorState) -> dict:
    """
    Supervisor agent that decides whether research is needed before writing.
    
    Analyzes the user's topic and determines if research would enhance
    the creative writing process.
    """
    topic = state.get("topic", "")
    
    # If we're already past initial stage, skip decision-making
    if state.get("workflow_stage") != "initial":
        return {}
    
    system_prompt = """You are a Supervisor Agent orchestrating a creative writing workflow.

Your job is to decide whether the user's topic would benefit from research before 
starting the creative writing process.

Consider these factors:
1. **Needs Research**: Topics that reference:
   - Historical events, figures, or periods
   - Real products, brands, or companies
   - Specific cultural contexts or movements
   - Technical domains requiring accuracy
   - Existing creative works (films, ads, art styles)
   - Real-world professions or industries

2. **No Research Needed**: Topics that are:
   - Purely fictional and original
   - Self-contained creative concepts
   - Abstract or fantastical with no real-world grounding
   - Personal stories without factual requirements

When in doubt, err on the side of doing research - it enriches the creative output."""

    human_prompt = f"""Topic: {topic}

Analyze this topic and decide if research would enhance the creative writing process.
If research is needed, formulate a specific research question that will gather the most 
relevant context and inspiration for the writing task."""

    decision = supervisor_with_structure.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])
    
    print(f"\n SUPERVISOR DECISION:")
    print(f"   Research needed: {decision.needs_research}")
    print(f"   Reasoning: {decision.reasoning}")
    if decision.needs_research:
        print(f"   Research question: {decision.research_question}")
    
    return {
        "needs_research": decision.needs_research,
        "research_topic": decision.research_question if decision.needs_research else "",
        "workflow_stage": "research" if decision.needs_research else "writing"
    }


def research_subgraph_node(state: SupervisorState) -> dict:
    """
    Invokes the Research agent as a subgraph.
    
    Transforms SupervisorState to ResearcherState, runs research,
    and transforms results back to SupervisorState.
    """
    print("\n[SEARCH] RESEARCH PHASE: Starting research...")
    
    # Transform to ResearcherState
    research_state: ResearcherState = {
        "researcher_messages": [
            HumanMessage(content=state.get("research_topic", state.get("topic", "")))
        ],
        "tool_call_iterations": 0,
        "research_topic": state.get("research_topic", state.get("topic", "")),
        "compressed_research": "",
        "raw_notes": []
    }
    
    # Invoke research agent
    research_result = researcher_agent.invoke(research_state)
    
    print(f"\n[OK] RESEARCH COMPLETE:")
    print(f"   Compressed findings: {len(research_result.get('compressed_research', ''))} chars")
    print(f"   Raw notes: {len(research_result.get('raw_notes', []))} notes")
    
    # Transform back to SupervisorState
    return {
        "compressed_research": research_result.get("compressed_research", ""),
        "raw_notes": research_result.get("raw_notes", []),
        "researcher_messages": research_result.get("researcher_messages", []),
        "research_complete": True,
        "workflow_stage": "writing"
    }


def prepare_writing_node(state: SupervisorState) -> dict:
    """
    Generates the InitialDraft using research findings.
    
    This node creates a complete initial draft enriched with research context,
    which will be passed to ArcueAgent to skip the draft generation step.
    """
    print("\n[WRITE] PREPARATION PHASE: Generating initial draft from research...")
    
    topic = state.get("topic", "")
    compressed_research = state.get("compressed_research", "")
    
    # If no research was done, create a simple draft from topic
    if not compressed_research:
        print("   No research available, creating basic draft from topic...")
        system_prompt = """You are a creative screenwriting assistant. Generate an initial draft for the given topic."""
        human_prompt = f"Topic: {topic}\n\nCreate an initial draft that captures this story idea."
    else:
        # Create enriched draft with research context
        system_prompt = """You are a creative screenwriting assistant with access to research findings.

Your task is to create a compelling initial draft that:
- Incorporates insights and inspiration from the research
- Establishes clear dramatic stakes and conflict
- Sets up authentic characters and world-building informed by research
- Creates a vivid, engaging narrative foundation
- Shows understanding of genre conventions and audience expectations

Use the research to enrich your creative choices without being overly literal."""

        human_prompt = f"""Original Topic: {topic}

Research Findings:
{compressed_research}

Create a detailed initial draft that serves as the foundation for this screenplay, 
enriched by the research insights."""

    # Use structured output to generate InitialDraft
    draft_generator = supervisor_model.with_structured_output(InitialDraft)
    
    initial_draft = draft_generator.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])
    
    print(f"\n INITIAL DRAFT GENERATED:")
    print(f"   Title: {initial_draft.title}")
    print(f"   Genre: {initial_draft.genre}")
    print(f"   Themes: {', '.join(initial_draft.themes)}")
    print(f"   Draft length: {len(initial_draft.draft)} characters")
    
    return {
        "draft": initial_draft.draft,
        "title": initial_draft.title,
        "genre": initial_draft.genre,
        "themes": initial_draft.themes,
        "tone": initial_draft.tone,
        "target_audience": initial_draft.target_audience,
        "unique_selling_point": initial_draft.unique_selling_point,
        "log_line": topic  # Keep original topic as log_line for reference
    }


def writing_subgraph_node(state: SupervisorState) -> dict:
    """
    Invokes the ArcueAgent as a subgraph for creative writing.
    
    The initial draft has already been generated by the prepare_writing_node,
    so we pass it directly to ArcueAgent to continue with characters, plot, and scenes.
    """
    print("\n[WRITING] WRITING PHASE: Continuing with ArcueAgent workflow...")
    print(f"   Using pre-generated draft: {state.get('title', 'N/A')}")
    
    # Transform to UnifiedState for ArcueAgent
    # Include the already-generated draft so ArcueAgent skips draft generation
    writing_input = {
        "log_line": state.get("log_line", ""),
        "draft": state.get("draft", ""),
        "title": state.get("title", ""),
        "genre": state.get("genre", ""),
        "themes": state.get("themes", []),
        "tone": state.get("tone", ""),
        "target_audience": state.get("target_audience", ""),
        "unique_selling_point": state.get("unique_selling_point", ""),
        "film_length_seconds": state.get("film_length_seconds", 90),
        "number_of_scenes": state.get("number_of_scenes", 12),
        "ad_mode": state.get("ad_mode", False),
    }
    
    # Add optional fields only if they have values
    if state.get("model"):
        writing_input["model"] = state["model"]
    if state.get("model_temperature") is not None:
        writing_input["model_temperature"] = state["model_temperature"]
    if state.get("random_seed") is not None:
        writing_input["random_seed"] = state["random_seed"]
    
    # Add ad-specific fields if in ad mode
    if state.get("ad_mode"):
        ad_fields = {
            "ad_total_seconds": state.get("ad_total_seconds"),
            "ad_scene_seconds": state.get("ad_scene_seconds"),
            "ad_brand": state.get("ad_brand"),
            "ad_product": state.get("ad_product"),
            "ad_goal": state.get("ad_goal"),
            "ad_audience": state.get("ad_audience"),
            "ad_tone": state.get("ad_tone"),
            "ad_offer": state.get("ad_offer"),
            "ad_constraints": state.get("ad_constraints"),
        }
        # Only add non-None ad fields
        writing_input.update({k: v for k, v in ad_fields.items() if v is not None})
    
    # Configure thread for story agent
    config = {
        "configurable": {
            "thread_id": f"supervisor_{state.get('topic', 'default')[:50]}"
        }
    }
    
    try:
        # The ArcueAgent has interrupts after each stage
        # We need to invoke it multiple times to progress through all stages
        
        # First invoke - will regenerate draft (or use existing) and stop at interrupt
        print("   Invoking ArcueAgent stage 1: Initial draft...")
        writing_result = story_agent.invoke(writing_input, config=config)
        
        # Continue through remaining stages
        stages = [
            ("characters", "create_characters"),
            ("plot", "create_plot"),
            ("dialogue", "create_dialogue"),
            ("locations", "create_locations"),
            ("visual lookbook", "define_visual_language"),
            ("scenes", "create_scenes"),
        ]
        
        for stage_name, _ in stages:
            print(f"   Continuing to {stage_name}...")
            writing_result = story_agent.invoke(None, config=config)
        
        # Continue through compilation and export stages (no interrupts)
        print(f"   Finalizing: compiling and exporting...")
        writing_result = story_agent.invoke(None, config=config)  # compile_script
        writing_result = story_agent.invoke(None, config=config)  # export_to_json
        writing_result = story_agent.invoke(None, config=config)  # export_to_markdown
        writing_result = story_agent.invoke(None, config=config)  # export_user_view
        
        print(f"\n[OK] ArcueAgent workflow complete!")
        print(f"   Characters: {len(writing_result.get('characters', []))} generated")
        print(f"   Plot Points: {len(writing_result.get('plot_points', []))} generated")
        print(f"   Scenes: {len(writing_result.get('scenes', []))} generated")
        
        # Transform results back to SupervisorState format
        # Keep all existing draft fields and add new generated content
        return {
            "characters": writing_result.get("characters", []),
            "plot_points": writing_result.get("plot_points", []),
            "dialogue_scenes": writing_result.get("dialogue_scenes", []),
            "locations": writing_result.get("locations", []),
            "scenes": writing_result.get("scenes", []),
            "final_script": writing_result.get("final_script"),
            "export_path": writing_result.get("export_path"),
            "json_files": writing_result.get("json_files", []),
            "workflow_stage": "complete",
            "writing_complete": True
        }
        
    except Exception as e:
        print(f"\nWARNING: Error invoking ArcueAgent: {e}")
        print(f"   The initial draft was generated successfully.")
        print(f"   You can continue with ArcueAgent manually from the character step.")
        import traceback
        traceback.print_exc()
        return {
            "workflow_stage": "complete",
            "writing_complete": False
        }


# === ROUTING LOGIC ===

def route_after_supervisor(state: SupervisorState) -> Literal["research_subgraph", "prepare_writing"]:
    """Route to research or directly to writing based on supervisor decision."""
    if state.get("needs_research", False):
        return "research_subgraph"
    return "prepare_writing"


def route_after_preparation(state: SupervisorState) -> Literal["writing_subgraph"]:
    """Always proceed to writing after preparation."""
    return "writing_subgraph"


# === GRAPH CONSTRUCTION ===

def build_supervisor_graph() -> StateGraph:
    """
    Build and compile the Supervisor graph.
    
    Workflow:
    1. START -> supervisor_node: Decide if research is needed
    2. supervisor_node -> research_subgraph OR prepare_writing
    3. research_subgraph -> prepare_writing
    4. prepare_writing -> writing_subgraph
    5. writing_subgraph -> END
    """
    builder = StateGraph(SupervisorState)
    
    # Add nodes
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("research_subgraph", research_subgraph_node)
    builder.add_node("prepare_writing", prepare_writing_node)
    builder.add_node("writing_subgraph", writing_subgraph_node)
    
    # Add edges
    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "research_subgraph": "research_subgraph",
            "prepare_writing": "prepare_writing"
        }
    )
    builder.add_edge("research_subgraph", "prepare_writing")
    builder.add_edge("prepare_writing", "writing_subgraph")
    builder.add_edge("writing_subgraph", END)
    
    return builder.compile()


# Compile the supervisor graph
supervisor_graph = build_supervisor_graph()


# === MAIN EXECUTION ===

def main():
    """
    Main execution function demonstrating the Supervisor Architecture.
    """
    print("[START] SUPERVISOR ARCHITECTURE - Unified Research + Writing Workflow")
    print("=" * 80)
    
    # Example: User provides a topic
    topic = input("\nEnter your story topic/idea: ").strip()
    if not topic:
        topic = "a story about a robot who wants to be a screenwriter"
        print(f"Using example topic: {topic}")
    
    # Initialize state
    initial_state: SupervisorState = {
        "topic": topic,
        "workflow_stage": "initial",
        "needs_research": False,
        "research_complete": False,
        "writing_complete": False,
        "raw_notes": [],
        "researcher_messages": [],
        "messages": []
    }
    
    print(f"\n Topic: {topic}")
    print("\n" + "=" * 80)
    
    # Invoke the supervisor graph
    try:
        result = supervisor_graph.invoke(initial_state)
        
        print("\n" + "=" * 80)
        print("[OK] SUPERVISOR WORKFLOW COMPLETE")
        print("=" * 80)
        
        print(f"\n[STATS] Workflow Summary:")
        print(f"   Research performed: {result.get('research_complete', False)}")
        print(f"   Writing completed: {result.get('writing_complete', False)}")
        
        if result.get("compressed_research"):
            print(f"\n[SEARCH] Research Summary:")
            print(f"   {result['compressed_research'][:200]}...")
        
        if result.get("draft"):
            print(f"\n Generated Initial Draft:")
            print(f"   Title: {result.get('title', 'N/A')}")
            print(f"   Genre: {result.get('genre', 'N/A')}")
            print(f"   Themes: {', '.join(result.get('themes', []))}")
            print(f"   Draft length: {len(result['draft'])} characters")
            print(f"\n   Draft preview:")
            print(f"   {result['draft'][:300]}...")
        
        if result.get("characters"):
            print(f"\n Characters: {len(result['characters'])} generated")
        if result.get("plot_points"):
            print(f"[RESEARCH] Plot Points: {len(result['plot_points'])} generated")
        if result.get("locations"):
            print(f"[LOCATION] Locations: {len(result['locations'])} generated")
        if result.get("scenes"):
            print(f"[SCENE] Scenes: {len(result['scenes'])} generated")
        
        if result.get("export_path"):
            print(f"\n[FOLDER] Export Location: {result['export_path']}")
            if result.get("json_files"):
                print(f"   JSON files: {len(result['json_files'])} exported")
        
        print("\n[IDEA] Next Steps:")
        if result.get("writing_complete") and result.get("characters"):
            print(f"   [OK] Full end-to-end workflow complete!")
            print(f"   Generated: Draft (research-enriched)  Characters  Plot  Dialogue  Locations  Visual Lookbook  Scenes")
            print(f"   All content exported to: {result.get('export_path', 'ArcueAgent/exports/')}")
            print(f"\n   For interactive refinement with human-in-the-loop:")
            print(f'   python -m ArcueAgent.agent')
            print(f'   Use CHECKPOINT_ID to resume from any stage.')
        elif result.get("draft"):
            print(f"   [OK] Initial draft created with research insights!")
            print(f"   Continue with ArcueAgent to generate characters, plot, and scenes:")
            print(f'   python -m ArcueAgent.agent')
            
    except Exception as e:
        print(f"\n[ERROR] Error during supervisor workflow: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

