"""
FastAPI Server for SagaAgent Integration

This server provides REST API endpoints to integrate Research Agent and SagaAgent
with a frontend application, supporting human-in-the-loop workflows for game narrative generation.
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Import agents and states
from Research.research_agent import researcher_agent
from Research.state_research import ResearcherState
from SagaAgent.agent import saga_agent
from SagaAgent.utils.state import SagaState
from SagaAgent.models.concept import ConceptDoc
from SagaAgent.config import ModelConfig, AgentConfig, ExportConfig
from SagaAgent.nodes import (
    generate_concept_node,
    generate_world_lore_node,
    generate_factions_node,
    generate_characters_node,
    generate_plot_arcs_node,
    generate_questlines_node,
)
from SagaAgent.services.export_service import ExportService

# Load environment
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="SagaEngine API",
    description="AI-powered game narrative generation platform with research and saga creation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MODELS ===

class ResearchOption(str, Enum):
    """Research requirement options"""
    REQUIRED = "required"
    NOT_REQUIRED = "not_required"


class WorkflowStage(str, Enum):
    """Workflow stages for tracking progress"""
    INITIAL = "initial"
    RESEARCH = "research"
    CONCEPT = "concept"
    WORLD_LORE = "world_lore"
    FACTIONS = "factions"
    CHARACTERS = "characters"
    PLOT_ARCS = "plot_arcs"
    QUESTLINES = "questlines"
    COMPLETE = "complete"


class StartWorkflowRequest(BaseModel):
    """Request to start a new workflow"""
    topic: str = Field(description="The game saga topic or idea")
    research_required: ResearchOption = Field(
        default=ResearchOption.NOT_REQUIRED,
        description="Whether research is required before saga generation"
    )
    research_question: Optional[str] = Field(
        default=None,
        description="Specific research question (required if research_required=True)"
    )
    model: Optional[str] = Field(default=None, description="LLM model to use")
    model_temperature: Optional[float] = Field(default=None, description="Model temperature")
    random_seed: Optional[int] = Field(default=None, description="Random seed for reproducibility")
    parallel_execution: Optional[bool] = Field(default=False, description="Enable parallel execution")
    parallel_max_workers: Optional[int] = Field(default=3, description="Max parallel workers")


class SubmitFeedbackRequest(BaseModel):
    """Request to submit feedback for current stage"""
    session_id: str = Field(description="Session/thread ID")
    feedback: str = Field(description="User feedback for the current stage")


class ContinueWorkflowRequest(BaseModel):
    """Request to continue to next stage"""
    session_id: str = Field(description="Session/thread ID")


class GetStateRequest(BaseModel):
    """Request to get current workflow state"""
    session_id: str = Field(description="Session/thread ID")


class WorkflowResponse(BaseModel):
    """Response for workflow operations"""
    session_id: str
    current_stage: WorkflowStage
    awaiting_feedback: bool
    data: Optional[Dict[str, Any]] = None
    message: str


class ResearchResponse(BaseModel):
    """Response for completed research"""
    session_id: str
    compressed_research: str
    raw_notes: List[str]
    message: str


# === SESSION MANAGEMENT ===

class SessionManager:
    """Manages workflow sessions and states"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.supervisor_model = self._get_supervisor_model()
    
    def _get_supervisor_model(self):
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
    
    def create_session(self, request: StartWorkflowRequest) -> str:
        """Create a new workflow session"""
        session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            "topic": request.topic,
            "research_required": request.research_required,
            "research_question": request.research_question,
            "current_stage": WorkflowStage.INITIAL,
            "awaiting_feedback": False,
            "config": {
                "model": request.model,
                "model_temperature": request.model_temperature,
                "random_seed": request.random_seed,
                "parallel_execution": request.parallel_execution,
                "parallel_max_workers": request.parallel_max_workers,
            },
            "state": {
                "messages": [],
                "factions": [],
                "characters": [],
                "plot_arcs": [],
                "questlines": [],
            },
            "thread_id": f"saga_{session_id}",
        }
        
        return session_id
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get session data"""
        if session_id not in self.sessions:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        return self.sessions[session_id]
    
    def update_session(self, session_id: str, updates: Dict[str, Any]):
        """Update session data"""
        session = self.get_session(session_id)
        session.update(updates)
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]


# Initialize session manager
session_manager = SessionManager()


# === HELPER FUNCTIONS ===

async def perform_research(session_id: str) -> Dict[str, Any]:
    """Perform research using the research agent"""
    session = session_manager.get_session(session_id)
    
    research_question = session.get("research_question") or session.get("topic")
    
    print(f"\n[SEARCH] Starting research for session {session_id}")
    print(f"   Research question: {research_question}")
    
    # Create research state
    research_state: ResearcherState = {
        "researcher_messages": [HumanMessage(content=research_question)],
        "tool_call_iterations": 0,
        "research_topic": research_question,
        "compressed_research": "",
        "raw_notes": []
    }
    
    # Invoke research agent
    research_result = researcher_agent.invoke(research_state)
    
    compressed_research = research_result.get("compressed_research", "")
    raw_notes = research_result.get("raw_notes", [])
    
    print(f"[OK] Research completed: {len(compressed_research)} characters")
    
    return {
        "compressed_research": compressed_research,
        "raw_notes": raw_notes,
        "researcher_messages": research_result.get("researcher_messages", [])
    }


async def generate_concept_from_research(
    session_id: str,
    compressed_research: str
) -> Dict[str, Any]:
    """Generate game concept enriched with research findings"""
    session = session_manager.get_session(session_id)
    topic = session.get("topic", "")
    
    print(f"\n[CONCEPT] Generating game concept from research for session {session_id}")
    
    # Create concept using research context
    system_prompt = """You are a creative game design assistant with access to research findings.

Your task is to create a compelling game concept that:
- Incorporates insights and inspiration from the research
- Establishes clear gameplay loops and mechanics
- Sets up authentic world-building informed by research
- Creates a compelling hook and unique selling proposition
- Shows understanding of game design principles and target audience

Use the research to enrich your creative choices without being overly literal."""

    human_prompt = f"""Original Topic: {topic}

Research Findings:
{compressed_research}

Create a detailed game concept that serves as the foundation for this game saga, 
enriched by the research insights."""

    # Use structured output to generate ConceptDoc
    concept_generator = session_manager.supervisor_model.with_structured_output(ConceptDoc)
    
    concept = concept_generator.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])
    
    print(f"✓ Game concept generated: {concept.title}")
    
    return {
        "title": concept.title,
        "genre": concept.genre,
        "elevator_pitch": concept.elevator_pitch,
        "core_loop": concept.core_loop,
        "key_mechanics": concept.key_mechanics,
        "progression": concept.progression,
        "world_setting": concept.world_setting,
        "art_style": concept.art_style,
        "target_audience": concept.target_audience,
        "monetization": concept.monetization,
        "usp": concept.usp,
    }


async def run_saga_stage(
    session_id: str,
    stage: WorkflowStage,
    node_func,
    state_key: str
) -> Dict[str, Any]:
    """Run a specific SagaAgent stage"""
    session = session_manager.get_session(session_id)
    current_state = session.get("state", {})
    config = session.get("config", {})
    
    print(f"\n[SAGA] Running stage: {stage.value}")
    
    # Create LangGraph config
    langgraph_config = {
        "configurable": {
            "thread_id": session.get("thread_id")
        }
    }
    
    # Prepare state for node execution
    # Filter out None values from config to avoid issues
    filtered_config = {k: v for k, v in config.items() if v is not None}
    node_state = {
        **current_state,
        **filtered_config,
        "topic": session.get("topic", ""),
    }
    
    # Execute the node
    result = node_func(node_state)
    
    # Update session state
    current_state.update(result)
    session_manager.update_session(session_id, {
        "state": current_state,
        "current_stage": stage,
        "awaiting_feedback": True
    })
    
    # Extract the relevant data for this stage
    stage_data = result.get(state_key)
    
    return {
        "stage": stage.value,
        "data": stage_data,
        "full_state": current_state
    }


# === API ENDPOINTS ===

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SagaEngine API",
        "version": "1.0.0",
        "endpoints": {
            "POST /workflow/start": "Start a new saga workflow",
            "POST /workflow/continue": "Continue to next stage",
            "POST /workflow/feedback": "Submit feedback for current stage",
            "GET /workflow/state/{session_id}": "Get current workflow state",
            "GET /workflow/{session_id}/export": "Export completed saga results",
            "DELETE /workflow/{session_id}": "Delete a workflow session",
            "POST /research/execute": "Execute research only",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/workflow/start", response_model=WorkflowResponse)
async def start_workflow(request: StartWorkflowRequest):
    """
    Start a new saga workflow
    
    This endpoint creates a new session and optionally performs research before
    starting the game narrative generation workflow.
    """
    try:
        # Create session
        session_id = session_manager.create_session(request)
        
        print(f"\n[START] Starting new saga workflow: {session_id}")
        print(f"   Topic: {request.topic}")
        print(f"   Research required: {request.research_required.value}")
        
        session = session_manager.get_session(session_id)
        
        # Handle research if required
        if request.research_required == ResearchOption.REQUIRED:
            if not request.research_question:
                raise HTTPException(
                    status_code=400,
                    detail="research_question is required when research_required=True"
                )
            
            # Perform research
            research_results = await perform_research(session_id)
            
            # Update session with research results
            session_manager.update_session(session_id, {
                "research_results": research_results,
                "current_stage": WorkflowStage.RESEARCH
            })
            
            # Generate concept from research
            concept_data = await generate_concept_from_research(
                session_id,
                research_results["compressed_research"]
            )
            
            # Update session state with concept
            session["state"]["concept"] = concept_data
            session["state"]["research_summary"] = research_results["compressed_research"]
            session_manager.update_session(session_id, {
                "state": session["state"],
                "current_stage": WorkflowStage.CONCEPT,
                "awaiting_feedback": True
            })
            
            return WorkflowResponse(
                session_id=session_id,
                current_stage=WorkflowStage.CONCEPT,
                awaiting_feedback=True,
                data={
                    "concept": concept_data,
                    "research": {
                        "compressed_research": research_results["compressed_research"],
                        "raw_notes_count": len(research_results.get("raw_notes", []))
                    }
                },
                message="Research completed and game concept generated. Ready for feedback."
            )
        
        else:
            # No research - create concept from topic
            print(f"   Skipping research, creating concept from topic...")
            
            # Run concept creation node
            result = await run_saga_stage(
                session_id,
                WorkflowStage.CONCEPT,
                generate_concept_node,
                "concept"
            )
            
            return WorkflowResponse(
                session_id=session_id,
                current_stage=WorkflowStage.CONCEPT,
                awaiting_feedback=True,
                data=result["full_state"],
                message="Game concept generated. Ready for feedback."
            )
    
    except Exception as e:
        print(f"[ERROR] Error starting workflow: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workflow/feedback", response_model=WorkflowResponse)
async def submit_feedback(request: SubmitFeedbackRequest):
    """
    Submit feedback for the current stage
    
    This endpoint allows users to provide feedback on the current stage,
    which will be used to regenerate that stage's content.
    """
    try:
        session = session_manager.get_session(request.session_id)
        current_stage = session.get("current_stage")
        
        if not session.get("awaiting_feedback"):
            raise HTTPException(
                status_code=400,
                detail="Session is not awaiting feedback"
            )
        
        print(f"\n📝 Received feedback for session {request.session_id}")
        print(f"   Stage: {current_stage.value}")
        print(f"   Feedback: {request.feedback[:100]}...")
        
        # Map stages to node functions and feedback keys
        stage_config = {
            WorkflowStage.CONCEPT: (generate_concept_node, "concept_feedback", "concept"),
            WorkflowStage.WORLD_LORE: (generate_world_lore_node, "world_lore_feedback", "world_lore"),
            WorkflowStage.FACTIONS: (generate_factions_node, "factions_feedback", "factions"),
            WorkflowStage.CHARACTERS: (generate_characters_node, "characters_feedback", "characters"),
            WorkflowStage.PLOT_ARCS: (generate_plot_arcs_node, "plot_arcs_feedback", "plot_arcs"),
            WorkflowStage.QUESTLINES: (generate_questlines_node, "questlines_feedback", "questlines"),
        }
        
        if current_stage not in stage_config:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot submit feedback for stage: {current_stage.value}"
            )
        
        node_func, feedback_key, state_key = stage_config[current_stage]
        
        # Add feedback to state and regenerate
        current_state = session.get("state", {})
        current_state[feedback_key] = request.feedback
        
        # Prepare state for node execution
        config = session.get("config", {})
        filtered_config = {k: v for k, v in config.items() if v is not None}
        node_state = {
            **current_state,
            **filtered_config,
            "topic": session.get("topic", ""),
        }
        
        # Regenerate with feedback
        result = node_func(node_state)
        
        # Update session state
        current_state.update(result)
        session_manager.update_session(request.session_id, {
            "state": current_state,
            "awaiting_feedback": True
        })
        
        return WorkflowResponse(
            session_id=request.session_id,
            current_stage=current_stage,
            awaiting_feedback=True,
            data=current_state,
            message=f"Stage {current_stage.value} regenerated with feedback"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Error submitting feedback: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workflow/continue", response_model=WorkflowResponse)
async def continue_workflow(request: ContinueWorkflowRequest):
    """
    Continue to the next stage of the workflow
    
    This endpoint moves the workflow to the next stage after the current stage
    has been reviewed and approved (or feedback has been incorporated).
    """
    try:
        session = session_manager.get_session(request.session_id)
        current_stage = session.get("current_stage")
        
        print(f"\n▶ Continuing workflow for session {request.session_id}")
        print(f"   Current stage: {current_stage.value}")
        
        # Define stage progression
        stage_progression = {
            WorkflowStage.CONCEPT: (WorkflowStage.WORLD_LORE, generate_world_lore_node, "world_lore"),
            WorkflowStage.WORLD_LORE: (WorkflowStage.FACTIONS, generate_factions_node, "factions"),
            WorkflowStage.FACTIONS: (WorkflowStage.CHARACTERS, generate_characters_node, "characters"),
            WorkflowStage.CHARACTERS: (WorkflowStage.PLOT_ARCS, generate_plot_arcs_node, "plot_arcs"),
            WorkflowStage.PLOT_ARCS: (WorkflowStage.QUESTLINES, generate_questlines_node, "questlines"),
            WorkflowStage.QUESTLINES: (WorkflowStage.COMPLETE, None, None),
        }
        
        if current_stage not in stage_progression:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot continue from stage: {current_stage.value}"
            )
        
        next_stage, node_func, state_key = stage_progression[current_stage]
        
        # Mark current stage as not awaiting feedback
        session_manager.update_session(request.session_id, {
            "awaiting_feedback": False
        })
        
        # If we've reached completion
        if next_stage == WorkflowStage.COMPLETE:
            session_manager.update_session(request.session_id, {
                "current_stage": WorkflowStage.COMPLETE,
                "awaiting_feedback": False
            })
            
            return WorkflowResponse(
                session_id=request.session_id,
                current_stage=WorkflowStage.COMPLETE,
                awaiting_feedback=False,
                data=session.get("state", {}),
                message="Saga workflow completed! All stages finished."
            )
        
        # Run next stage
        result = await run_saga_stage(
            request.session_id,
            next_stage,
            node_func,
            state_key
        )
        
        return WorkflowResponse(
            session_id=request.session_id,
            current_stage=next_stage,
            awaiting_feedback=True,
            data=result["full_state"],
            message=f"Moved to stage: {next_stage.value}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Error continuing workflow: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflow/state/{session_id}", response_model=WorkflowResponse)
async def get_workflow_state(session_id: str):
    """
    Get the current state of a workflow session
    
    Returns the current stage, state data, and whether the workflow is awaiting feedback.
    """
    try:
        session = session_manager.get_session(session_id)
        
        return WorkflowResponse(
            session_id=session_id,
            current_stage=session.get("current_stage"),
            awaiting_feedback=session.get("awaiting_feedback", False),
            data=session.get("state", {}),
            message="Current workflow state"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/research/execute", response_model=ResearchResponse)
async def execute_research(topic: str, research_question: Optional[str] = None):
    """
    Execute research independently without starting a full workflow
    
    This endpoint allows you to perform research without committing to a full
    saga generation workflow.
    """
    try:
        # Create temporary session for research
        temp_session_id = str(uuid.uuid4())
        session_manager.sessions[temp_session_id] = {
            "topic": topic,
            "research_question": research_question or topic,
        }
        
        # Perform research
        research_results = await perform_research(temp_session_id)
        
        # Clean up temporary session
        session_manager.delete_session(temp_session_id)
        
        return ResearchResponse(
            session_id=temp_session_id,
            compressed_research=research_results["compressed_research"],
            raw_notes=research_results.get("raw_notes", []),
            message="Research completed successfully"
        )
    
    except Exception as e:
        print(f"[ERROR] Error executing research: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/workflow/{session_id}")
async def delete_workflow(session_id: str):
    """Delete a workflow session"""
    try:
        session_manager.delete_session(session_id)
        return {"message": f"Session {session_id} deleted successfully"}
    except HTTPException:
        raise


@app.get("/workflow/{session_id}/export")
async def export_workflow(session_id: str, format: str = "markdown"):
    """
    Export workflow results in various formats
    
    This endpoint allows clients to export the completed workflow results
    in markdown or JSON format using the SagaAgent export service.
    """
    try:
        session = session_manager.get_session(session_id)
        current_stage = session.get("current_stage")
        
        if current_stage != WorkflowStage.COMPLETE:
            raise HTTPException(
                status_code=400,
                detail=f"Workflow must be complete to export. Current stage: {current_stage.value}"
            )
        
        state = session.get("state", {})
        
        if format.lower() == "markdown":
            # Export all stages as markdown
            export_results = ExportService.export_all_markdown(state)
            return {
                "session_id": session_id,
                "format": "markdown",
                "files": export_results.get("markdown_files", []),
                "message": "Saga exported to markdown files"
            }
        
        elif format.lower() == "json":
            # Export all stages as JSON
            export_results = ExportService.export_all_json(state)
            return {
                "session_id": session_id,
                "format": "json",
                "files": export_results.get("json_files", []),
                "message": "Saga exported to JSON files"
            }
        
        else:
            raise HTTPException(
                status_code=400,
                detail="Format must be 'markdown' or 'json'"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Error exporting workflow: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time workflow updates
    
    This allows frontend clients to receive real-time updates as the workflow progresses.
    """
    await websocket.accept()
    
    try:
        # Verify session exists
        session = session_manager.get_session(session_id)
        
        # Send initial state
        await websocket.send_json({
            "type": "state_update",
            "current_stage": session.get("current_stage").value,
            "awaiting_feedback": session.get("awaiting_feedback", False),
            "data": session.get("state", {})
        })
        
        # Listen for client messages
        while True:
            data = await websocket.receive_json()
            
            message_type = data.get("type")
            
            if message_type == "feedback":
                # Handle feedback submission via WebSocket
                feedback = data.get("feedback", "")
                # Process feedback (similar to submit_feedback endpoint)
                await websocket.send_json({
                    "type": "feedback_received",
                    "message": "Feedback received and processing"
                })
            
            elif message_type == "continue":
                # Handle continue request via WebSocket
                await websocket.send_json({
                    "type": "continuing",
                    "message": "Moving to next stage"
                })
            
            elif message_type == "get_state":
                # Send current state
                session = session_manager.get_session(session_id)
                await websocket.send_json({
                    "type": "state_update",
                    "current_stage": session.get("current_stage").value,
                    "awaiting_feedback": session.get("awaiting_feedback", False),
                    "data": session.get("state", {})
                })
    
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()


# === MAIN ===

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("API_PORT", 8001))
    host = os.environ.get("API_HOST", "0.0.0.0")
    
    print(f"\n[START] Starting SagaEngine API Server")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"\n📚 API Documentation:")
    print(f"   Swagger UI: http://{host}:{port}/docs")
    print(f"   ReDoc: http://{host}:{port}/redoc")
    
    uvicorn.run(app, host=host, port=port)



