# SagaAgent: Multi-Stage Narrative Generation with LangGraph

## Overview

SagaAgent is a LangGraph-powered multi-agent system for generating comprehensive game narratives from concept through questline design, with human-in-the-loop (HITL) feedback interrupts at each stage.

**Pipeline:** `Concept → World Lore → Factions → Characters → Plot Arcs → Questlines → RenderPrep`

All outputs are structured Pydantic models ready for downstream visual asset generation (Veo/Genie).

---

## Features

✅ **Sequential Pipeline with HITL Interrupts**
- Interrupt after each stage (concept, lore, factions, characters, plot arcs, questlines)
- User provides feedback; LLM re-generates if needed
- Continue with `AUTO_CONTINUE=true` for non-interactive mode

✅ **Checkpoint Persistence**
- SqliteSaver for checkpoint management
- Resume from any stage via `CHECKPOINT_ID`
- List checkpoint history with `LIST_HISTORY=true`

✅ **Dependency-Aware Generation**
- Each stage references upstream outputs
- Characters contextualized by factions/lore
- Quests linked to plot arcs and characters

✅ **Render-Ready Output**
- Built-in RenderPrep nodes convert narrative to visual prompts
- Character sheets, environment boards, key art concepts
- Ready for Veo/Genie ingestion

✅ **Flexible Model Support**
- OpenAI (GPT-4o, GPT-4, etc.)
- Google (Gemini 2.0, etc.)
- Auto-detection based on API key availability

---

## Architecture

### State Management (`SagaState`)
```python
class SagaState(TypedDict):
    topic: str                                    # Input topic
    research_summary: Optional[str]               # From upstream research
    
    concept: Dict[str, Any]                       # Stage 1: ConceptDoc
    world_lore: Dict[str, Any]                    # Stage 2: WorldLore
    factions: Annotated[List[Dict], operator.add] # Stage 3: GameFaction[]
    characters: Annotated[List[Dict], operator.add] # Stage 4: GameCharacter[]
    plot_arcs: Annotated[List[Dict], operator.add]  # Stage 5: PlotArc[]
    questlines: Annotated[List[Dict], operator.add] # Stage 6: Questline[]
    
    # Feedback fields (one per stage)
    concept_feedback: str
    world_lore_feedback: str
    # ... etc
```

**List Reducers:** Using `Annotated[List, operator.add]` allows multiple LLM invocations to append without overwriting.

### Node Functions
Each node:
1. Extracts prerequisites from state
2. Builds context-aware prompt
3. Calls LLM with structured output (Pydantic model)
4. Returns `{stage}: output_dict` update

Example:
```python
def generate_concept_node(state: SagaState) -> Dict[str, Any]:
    topic = state.get("topic", "")
    research = state.get("research_summary", "")
    
    llm = LLMService.create_structured_llm(state, ConceptDoc, creative=True)
    concept = llm.invoke([...prompt...])
    
    return {"concept": concept.model_dump()}
```

### Checkpoint Flow
```
START
  ↓
[concept] → INTERRUPT (collect feedback)
  ↓
[world_lore] → INTERRUPT
  ↓
[factions] → INTERRUPT
  ↓
[characters] → INTERRUPT
  ↓
[plot_arcs] → INTERRUPT
  ↓
[questlines] → INTERRUPT
  ↓
END
```

Each interrupt allows user to provide feedback that gets passed to the node function for context-aware regeneration.

---

## Quick Start

### Installation
```bash
cd E:\Hackman
pip install -r requirements.txt  # Ensure langchain, langgraph, pydantic installed
```

### Basic Execution
```bash
# Interactive mode (prompts for feedback at each stage)
python -m SagaAgent.agent TOPIC="Epic fantasy game"

# With research context
python -m SagaAgent.agent TOPIC="Cyberpunk noir RPG" RESEARCH_SUMMARY="Inspired by Blade Runner and Neuromancer"

# Auto-continue (no interrupts)
python -m SagaAgent.agent TOPIC="..." AUTO_CONTINUE=true

# Resume from checkpoint
python -m SagaAgent.agent CHECKPOINT_ID=<checkpoint_id>

# List checkpoint history
python -m SagaAgent.agent LIST_HISTORY=true THREAD_ID=<thread_id>
```

### Environment Variables
```bash
# API Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o  # Optional, defaults to gpt-4o

# OR Google
GOOGLE_API_KEY=...
GOOGLE_MODEL=gemini-2.0-flash

# Workflow
TOPIC="Your saga idea"
RESEARCH_SUMMARY="Optional research context"
AUTO_CONTINUE=false  # true for non-interactive mode

# Checkpoints
THREAD_ID=<unique-id>  # Defaults to UUID
CHECKPOINT_ID=<id>     # Resume from checkpoint
LIST_HISTORY=false     # Show checkpoint history

# Model Control
MODEL=gpt-4o           # Override model
MODEL_TEMPERATURE=0.8  # Custom temperature

# Rendering
ENABLE_RENDER_PREP=true  # Generate visual prompts
```

---

## Output Structure

### Outputs per Stage

**Concept**
```json
{
  "title": "The Last Sentinel",
  "genre": "Action RPG, Roguelike",
  "core_loop": "Explore → Combat → Upgrade → Repeat",
  "usp": "Procedural world with meaningful NPC relationships",
  ...
}
```

**World Lore**
```json
{
  "world_name": "Aethermoor",
  "geography": "Three continents with ancient rifts...",
  "magic_or_technology": "Dual magic system: Rune Magic and Tech Artifacts",
  ...
}
```

**Factions** (List)
```json
[
  {
    "faction_name": "The Luminous Order",
    "core_ideology": "Protect the light against darkness",
    "reputation_system": "Hostile → Neutral → Friendly → Honored",
    ...
  },
  ...
]
```

**Characters** (List)
```json
[
  {
    "character_name": "Theron Blackblade",
    "character_type": "Protagonist",
    "appearance": "Tall, scarred, with silver eyes",
    "backstory": "Exiled warrior seeking redemption",
    ...
  },
  ...
]
```

**Plot Arcs** (List)
```json
[
  {
    "arc_title": "The Sundered Kingdom",
    "arc_type": "Main Quest",
    "act1_hook": "The kingdom falls to shadow...",
    "major_choice_points": 3,
    "multiple_endings": 4,
    ...
  }
]
```

**Questlines** (List)
```json
[
  {
    "quest_name": "Fragments of Hope",
    "quest_type": "Faction Quest",
    "primary_objectives": "Retrieve 3 ancient fragments",
    "choice_points": 2,
    ...
  },
  ...
]
```

### Files Generated
```
./
├── saga_concept.json          (Concept output)
├── saga_concept.md            (Concept markdown)
├── saga_world_lore.json       (World lore output)
├── saga_world_lore.md         (World lore markdown)
├── saga_factions.json         (Factions list)
├── saga_characters.json       (Characters list)
├── saga_plot_arcs.json        (Plot arcs list)
├── saga_questlines.json       (Questlines list)
└── SagaAgent/exports/
    └── <timestamp>/
        ├── saga_complete.json  (All combined)
        └── saga_brief.md       (Executive summary)
```

---

## Integration with Supervisor

The SagaAgent is designed to integrate with SupervisorAgent:

```python
# In supervisor_agent.py
def research_to_saga_node(state: SupervisorState) -> dict:
    """Route research findings to SagaAgent."""
    research = state.get("compressed_research", "")
    
    saga_input = {
        "topic": state.get("topic", ""),
        "research_summary": research,
        "messages": []
    }
    
    saga_result = saga_agent.invoke(saga_input, config={...})
    
    return {
        "concept": saga_result.get("concept"),
        "world_lore": saga_result.get("world_lore"),
        "factions": saga_result.get("factions"),
        ...
    }
```

---

## Temperature Control

SagaAgent uses intelligent temperature tuning:

| Task | Temperature | Purpose |
|------|-------------|---------|
| Concept generation | 0.9 (Creative) | Novelty, unexpected ideas |
| World lore | 0.9 (Creative) | Rich, imaginative worldbuilding |
| Factions | 0.9 (Creative) | Unique identities and mechanics |
| Characters | 0.9 (Creative) | Distinctive personalities |
| Plot arcs | 0.9 (Creative) | Branching narratives, twists |
| Questlines | 0.9 (Creative) | Varied quest types |
| RenderPrep | 0.7 (Balanced) | Clear visual descriptions |

Override with `MODEL_TEMPERATURE=X` env var.

---

## Node Dependencies

```
concept
  ↓ (inputs to)
world_lore
  ↓ (inputs to)
factions ←─────┐
  ↓            │
characters ←───┤ (context)
  ↓            │
plot_arcs ←────┤
  ↓            │
questlines ←───┘
  ↓
render_prep_nodes
```

Each downstream node can reference ALL upstream outputs for context.

---

## Extending SagaAgent

### Adding New Nodes
1. Create `SagaAgent/nodes/new_stage_node.py`
2. Define `generate_new_stage_node(state: SagaState) -> Dict[str, Any]`
3. Add to `workflow.add_node("new_stage", generate_new_stage_node)`
4. Update edges in `agent.py`

### Adding New Feedback Types
1. Add field to `SagaState`: `new_stage_feedback: NotRequired[str]`
2. Pass to node: `node_func({...state, new_stage_feedback: user_input})`
3. Use in node prompt to inform regeneration

### Custom Export Services
Extend `RenderPrepOutput` models and create export service:
```python
class ExportService:
    @staticmethod
    def export_saga(state: SagaState, output_dir: str):
        # Export narrative + visual prompts
        pass
```

---

## Testing Checklist

- [ ] Run concept generation on test topic
- [ ] Verify concept feeds into lore generation
- [ ] Test interrupt flow (provide feedback, re-generate)
- [ ] Verify checkpoint saving/resuming
- [ ] Test list history functionality
- [ ] Verify list reducer behavior (factions append, not replace)
- [ ] Test downstream dependencies (characters reference factions)
- [ ] Test render prep node generation
- [ ] Verify markdown exports
- [ ] Test with different models (OpenAI, Google)

---

## Troubleshooting

### "No API keys found"
```bash
export OPENAI_API_KEY=sk-...
# OR
export GOOGLE_API_KEY=...
```

### "LLM does not support structured output"
Model may not support `json_schema` method. Try:
- `MODEL=gpt-4o` (always works)
- `MODEL=gemini-2.0-flash`
- Fallback uses `.with_structured_output()` without method param

### Checkpoint not resuming
```bash
# List available checkpoints
python -m SagaAgent.agent LIST_HISTORY=true

# Resume with exact checkpoint ID
python -m SagaAgent.agent CHECKPOINT_ID=<exact-id>
```

### Memory errors with large outputs
- Reduce batch sizes in node functions (currently 2-3 items per stage)
- Stream outputs to disk instead of holding in memory
- Use `ENABLE_RENDER_PREP=false` to skip visual prep

---

## Next: Integration Steps

1. **Extend SupervisorAgent** to route research → SagaAgent
2. **Extend OrchestratorAgent** to handle saga components (surgical updates)
3. **Build RenderPrepAgent** full pipeline (prep → Veo/Genie)
4. **Create CLI wrapper** for `python -m SagaAgent.agent`
5. **Add telemetry** (token counts, generation times)

---

## Files Reference

```
SagaAgent/
├── agent.py                    # Main graph + CLI
├── config.py                   # AgentConfig, ExportConfig, ModelConfig
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── concept.py             # ConceptDoc
│   ├── lore.py                # WorldLore
│   ├── faction.py             # GameFaction
│   ├── character.py           # GameCharacter
│   ├── plot.py                # PlotArc
│   ├── quest.py               # Questline
│   └── render_prep.py         # Visual prompt models
├── nodes/
│   ├── __init__.py
│   ├── concept_node.py        # generate_concept_node()
│   ├── lore_node.py           # generate_world_lore_node()
│   ├── faction_nodes.py       # generate_factions_node()
│   ├── character_nodes.py     # generate_characters_node()
│   ├── plot_nodes.py          # generate_plot_arcs_node()
│   ├── quest_nodes.py         # generate_questlines_node()
│   └── render_prep_nodes.py   # Visual prep nodes
├── utils/
│   ├── __init__.py
│   ├── state.py               # SagaState TypedDict
│   └── llm_service.py         # LLMService class
└── README.md                  # This file
```

---

## License

Project X - Internal Use Only

**Version:** 1.0.0 (Beta)
**Status:** Fully Functional - Ready for Integration
