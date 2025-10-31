# Project X: SagaAgent Multi-Agent LangGraph Implementation

## ✅ COMPLETED

### 1. Model Layer (`SagaAgent/models/`)
- ✅ `concept.py` - ConceptDoc Pydantic model
- ✅ `lore.py` - WorldLore Pydantic model  
- ✅ `faction.py` - GameFaction Pydantic model
- ✅ `character.py` - GameCharacter Pydantic model
- ✅ `plot.py` - PlotArc Pydantic model
- ✅ `quest.py` - Questline Pydantic model
- ✅ `render_prep.py` - RenderPrep models (CharacterVisualPrompt, EnvironmentPrompt, ItemPrompt, StoryboardFrame)
- ✅ `models/__init__.py` - Package exports

### 2. State Definition (`SagaAgent/utils/`)
- ✅ `state.py` - SagaState TypedDict with all narrative + visual fields
  - Annotated list reducers for: factions, characters, plot_arcs, questlines
  - Feedback fields for HITL interrupts after each stage
  - Render prep output fields

### 3. Configuration (`SagaAgent/`)
- ✅ `config.py` - AgentConfig, ExportConfig, ModelConfig
  - Thread ID management for checkpoint persistence
  - Environment variable integration
  - to_state_dict() helper for CLI args

### 4. Agent Assembly (`SagaAgent/`)
- ✅ `agent.py` - Main SagaAgent graph
  - StateGraph with sequential pipeline
  - Interrupts after each stage: concept → world_lore → factions → characters → plot_arcs → questlines
  - SqliteSaver checkpoints for HITL restarts
  - _handle_interrupt() for feedback collection
  - main() CLI entry point

### 5. Node Layer (Partial - Concept Node)
- ✅ `nodes/__init__.py` - Node function exports (stubs for remaining nodes)
- ✅ `nodes/concept_node.py` - generate_concept_node() with structured output
  - Uses LLMService.create_structured_llm()
  - Generates ConceptDoc + markdown
  - Incorporates research_summary when available

---

## ⏳ TO DO (Priority Order for Token Budget)

### A. Complete Node Layer (Critical - Dependency for agent.py)

**Node Files to Create:**

1. `nodes/lore_node.py` - generate_world_lore_node()
   - Input: state with concept, research_summary
   - Output: world_lore dict + world_lore_md
   - References: concept to ensure consistency

2. `nodes/faction_nodes.py` - generate_factions_node()
   - Input: state with world_lore, concept
   - Output: factions list (appends to state.factions)
   - Parameterize faction count from config

3. `nodes/character_nodes.py` - generate_characters_node()
   - Input: state with concept, factions, world_lore
   - Output: characters list (appends to state.characters)
   - Use persona_type from factions/lore context

4. `nodes/plot_nodes.py` - generate_plot_arcs_node()
   - Input: state with characters, world_lore, concept
   - Output: plot_arcs list (appends to state.plot_arcs)
   - Reference faction/character IDs in branching structure

5. `nodes/quest_nodes.py` - generate_questlines_node()
   - Input: state with plot_arcs, characters, factions
   - Output: questlines list (appends to state.questlines)
   - Link to plot arcs via quest_dependencies

6. `nodes/render_prep_nodes.py` - RenderPrep nodes
   - prepare_characters_node(): Characters → CharacterVisualPrompts
   - prepare_locations_node(): World Lore → EnvironmentPrompts  
   - prepare_items_node(): Artifacts from plot arcs → ItemPrompts
   - assemble_storyboards_node(): Plot arcs → StoryboardFrames

### B. LLM Service
`services/llm_service.py` or `utils/llm_service.py`:
- LLMService class with create_structured_llm() method
- Support OpenAI + Google models
- Temperature control (creative=0.9, analytical=0.3)
- Fallback graceful error handling

### C. RenderPrepAgent (Optional but Recommended)
- `RenderPrepAgent/agent.py` - Graph for render prep pipeline
- Nodes already partially defined in step A above
- Export service for JSON/markdown outputs

### D. Extended SupervisorAgent
Update `supervisor_agent.py`:
- Add SagaAgent orchestration (research → concept → render prep)
- Route to SagaAgent instead of/alongside ArcueAgent
- Compress research findings for concept prompt

### E. Extended OrchestratorAgent  
Update `OrchestratorAgent/orchestrator.py`:
- Add saga components to component_map:
  - 'concept', 'world_lore', 'factions', 'plot_arcs', 'questlines'
- Add surgical update helpers (_update_specific_faction, _update_specific_plot_arc, etc.)
- Preserve quest-count logic similar to scene-count preservation
- Update ComponentIdentification to recognize saga keywords

---

## Architecture Decisions Made

### State Management
- **List Reducers**: Using `Annotated[List, operator.add]` for factions, characters, plot_arcs, questlines
  - Allows multiple node invocations to append without overwriting
  - Cleaner than manual list concat logic

### Interrupts Strategy
- **One interrupt per stage** (not per item in list)
  - Simpler UX (6 interrupts max: concept, lore, factions, characters, plots, quests)
  - User feedback applied to entire batch, LLM re-generates if needed
  - Mirrors ArcueAgent pattern for consistency

### Feedback Loop
- Feedback stored as `{stage}_feedback` fields
- Passed to node functions for context-aware regeneration
- Alternative: Store in `feedback` dict with component keys

### Checkpoint Persistence
- SqliteSaver by default (falls back to MemorySaver if import fails)
- Thread ID uniqueness for parallel runs
- Checkpoint resumption via `--checkpoint-id` CLI flag

---

## Node Implementation Template

Each node should follow this pattern:

```python
def generate_{stage}_node(state: SagaState) -> Dict[str, Any]:
    """
    Generate {stage} content.
    
    Args:
        state: Current SagaState with prerequisite fields
        
    Returns:
        Updated state dict with {stage} output
    """
    # 1. Extract prerequisites from state
    concept = state.get("concept", {})
    feedback = state.get("{stage}_feedback", "")
    
    # 2. Build prompt incorporating prerequisites
    system_prompt = "..."
    human_prompt = f"... {concept['title']} ..."
    
    # 3. Call LLM with structured output
    llm = LLMService.create_structured_llm(state, {OutputModel}, creative=True)
    output = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])
    
    # 4. Convert and format
    output_dict = output.model_dump()
    output_md = "..."  # Markdown version
    
    # 5. Return state update
    return {
        "{stage}": output_dict,  # or list for multiple items
        "{stage}_md": output_md,
    }
```

---

## Testing Checklist

- [ ] Create test saga with concept → lore → factions → characters → plot → quests
- [ ] Verify interrupts work at each stage
- [ ] Test checkpoint saving/resuming
- [ ] Test feedback incorporation (concept feedback re-runs concept node)
- [ ] Verify downstream stages reference upstream outputs
- [ ] Test render prep node generation
- [ ] Test supervisor routing to SagaAgent
- [ ] Test orchestrator updates for saga components
- [ ] Verify list reducer behavior (factions append, not replace)

---

## CLI Usage

```bash
# Basic execution
python -m SagaAgent.agent TOPIC="epic fantasy game"

# With research context
python -m SagaAgent.agent TOPIC="cyberpunk noir" RESEARCH_SUMMARY="..."

# Auto-continue (no interrupts)
python -m SagaAgent.agent TOPIC="..." AUTO_CONTINUE=true

# Resume from checkpoint
python -m SagaAgent.agent CHECKPOINT_ID=<id>

# List checkpoint history
python -m SagaAgent.agent LIST_HISTORY=true

# Custom model
python -m SagaAgent.agent TOPIC="..." MODEL="gpt-4o" MODEL_TEMPERATURE=0.8
```

---

## Next Priority: LLMService

The LLMService is imported by all node files but not yet created. This is the critical dependency blocking full implementation.

Location: `SagaAgent/utils/llm_service.py` or `SagaAgent/services/llm_service.py`

Key method needed:
```python
@staticmethod
def create_structured_llm(state: dict, output_schema: Type, creative: bool = True):
    """Create LLM with structured output."""
    # Initialize model based on state['model'] or env defaults
    # Apply temperature: creative=0.9, analytical=0.3
    # Return model.with_structured_output(output_schema)
```
