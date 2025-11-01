# Orchestrator Agent for SagaAgent

## Overview

The **Orchestrator Agent for SagaAgent** is an intelligent game narrative revision system that analyzes existing saga narrative files, provides structured LLM feedback, and selectively updates only the components that need improvement.

## Key Features

- 🤖 **AI-Powered Analysis**: Uses OpenAI or Gemini models to analyze game narrative quality
- 🎯 **Selective Updates**: Only updates components that need improvement
- 📊 **Structured Feedback**: Provides detailed, actionable feedback for each component
- 🔄 **Iterative Refinement**: Can be run multiple times for continuous improvement
- ⚡ **Auto Mode**: Fully automated revision workflow
- 🎮 **Game-Focused**: Designed specifically for game narrative components

## Architecture

The orchestrator consists of:

1. **Models** (`models/orchestrator.py`):
   - `UserViewAnalysis`: Structured analysis with component feedback
   - `ComponentFeedback`: Feedback for individual components
   - `ComponentIdentification`: LLM-powered component identification

2. **Prompts** (`prompts/orchestrator_prompts.py`):
   - Analysis prompts for game narrative LLM evaluation
   - Formatting utilities for saga data

3. **Agent** (`orchestrator_saga.py`):
   - Main orchestration logic for SagaAgent
   - Component update workflows
   - State management for game narratives

4. **Tools** (`tools/component_tools.py`):
   - LangChain tools for component analysis
   - Dependency checking
   - Component information retrieval

## SagaAgent Components

The orchestrator can update these game narrative components:

- **concept**: Game concept, elevator pitch, core loop, mechanics, USP
- **world_lore**: World history, culture, geography, key themes
- **factions**: Faction definitions, ideologies, goals, relationships
- **characters**: Character profiles, backstories, motivations, relationships
- **plot_arcs**: Major narrative arcs, stakes, resolutions
- **questlines**: Individual quests, objectives, rewards, branches

## Usage

### Basic Usage

Analyze a saga file or directory and apply updates automatically:

```bash
python -m OrchestratorAgent.orchestrator_saga SagaAgent/exports/ --auto
```

### With User Feedback

Provide specific feedback for targeted updates:

```bash
python -m OrchestratorAgent.orchestrator_saga SagaAgent/exports/ --feedback "Add a faction called The Shadow Council"
```

### Single Component File

Update a specific component file:

```bash
python -m OrchestratorAgent.orchestrator_saga saga_characters.json --feedback "Add a character named Marcus, a rebel leader"
```

### Programmatic Usage

You can also use the orchestrator in your own scripts:

```python
from OrchestratorAgent.orchestrator_saga import OrchestratorAgent
from SagaAgent.config import AgentConfig

# Create orchestrator
config = AgentConfig.from_env()
orchestrator = OrchestratorAgent(config)

# Run revision workflow
json_files, markdown_files = orchestrator.orchestrate_revision(
    saga_filepath="SagaAgent/exports/",
    user_feedback="Make the world more dystopian",
    auto_apply=True
)

print(f"Updated files: {json_files}")
```

## Environment Setup

Create a `.env` file with your API keys:

```bash
# OpenAI (if using OpenAI models)
OPENAI_API_KEY=your_openai_key_here

# Google (if using Gemini models)
GOOGLE_API_KEY=your_google_key_here

# Model selection (optional, auto-detects based on available keys)
MODEL=gpt-4o
# or
MODEL=gemini-2.0-flash-exp

# Temperature (optional)
MODEL_TEMPERATURE=0.3

# Random seed for reproducibility (optional)
RANDOM_SEED=42
```

## Workflow

1. **Load**: Reads saga component files (JSON format)
2. **Analyze**: LLM analyzes narrative and provides structured feedback
3. **Display**: Shows analysis with coherence score and component feedback
4. **Update**: Selectively updates only the components that need improvement
5. **Export**: Generates new saga files with timestamp

## Component Dependencies

The orchestrator respects component dependencies:

1. **concept** → Everything (foundational)
2. **world_lore** → factions, characters, plot_arcs (establishes setting)
3. **factions** → characters, plot_arcs (affects allegiances)
4. **characters** → plot_arcs, questlines (drive stories)
5. **plot_arcs** → questlines (manifest as quests)
6. **questlines** → No dependencies (final implementation)

**Note**: By default, the orchestrator is **extremely conservative** and only updates what you explicitly request. Dependencies are suggested but not automatically updated unless you explicitly ask for them.

## Examples

### Example 1: Add a New Faction

```bash
python -m OrchestratorAgent.orchestrator_saga saga_factions.json --feedback "Add a faction called The Crimson Order, a religious militant group" --auto
```

**Result**: Only the factions component is updated. Characters, plot arcs, and quests remain unchanged.

### Example 2: Enhance World Lore

```bash
python -m OrchestratorAgent.orchestrator_saga saga_world_lore.json --feedback "Make the world history more detailed, focusing on the ancient war" --auto
```

**Result**: Only the world lore component is updated. Other components remain unchanged.

### Example 3: Add a Character

```bash
python -m OrchestratorAgent.orchestrator_saga saga_characters.json --feedback "Add a character named Elena, a tech genius who works for the resistance" --auto
```

**Result**: Only the characters component is updated. The character is added to the roster but not automatically integrated into quests or plot arcs.

### Example 4: Update Multiple Files in a Directory

```bash
python -m OrchestratorAgent.orchestrator_saga SagaAgent/exports/ --feedback "Make all factions more morally gray" --auto
```

**Result**: The orchestrator loads all saga components from the directory and updates only the factions based on your feedback.

## Output

The orchestrator generates new saga files with timestamps:

```
SagaAgent/exports/
  - GTA_Vice_City_Saga_concept_20241031_143022.json
  - GTA_Vice_City_Saga_factions_20241031_143022.json
  - GTA_Vice_City_Saga_factions_20241031_150133.json (NEW - revised)
  - GTA_Vice_City_Saga_factions_20241031_150133.md (NEW - revised)
```

You can run the orchestrator again on the new files for further refinement.

## Integration with SagaAgent Workflow

The orchestrator complements the main SagaAgent workflow:

1. **Initial Generation**: Run `python -m SagaAgent.agent` to create initial narrative
2. **Review**: Check the generated saga files in `SagaAgent/exports/`
3. **Refine**: Run orchestrator to improve specific components
4. **Iterate**: Run orchestrator multiple times for continuous refinement

## Best Practices

1. **Targeted Updates**: Use specific feedback to update only what you need
2. **Iterative Refinement**: Run the orchestrator multiple times for incremental improvements
3. **Conservative Approach**: By default, only the explicitly mentioned component is updated
4. **Explicit Dependencies**: If you want to update related components, mention them explicitly
5. **Review Output**: Always review the generated files before using them
6. **Backup Files**: The orchestrator preserves original files by creating new timestamped versions

## Comparison: ArcueAgent vs SagaAgent Orchestrator

| Feature | ArcueAgent Orchestrator | SagaAgent Orchestrator |
|---------|------------------------|------------------------|
| **Domain** | Screenplay/Film | Game Narrative |
| **Components** | draft, characters, dialogue, locations, visual_lookbook, scenes | concept, world_lore, factions, characters, plot_arcs, questlines |
| **Focus** | Visual storytelling | Interactive narrative |
| **Dependencies** | Linear (draft → characters → scenes) | Hierarchical (concept → lore → factions/characters → arcs → quests) |
| **Output Format** | USER_VIEW JSON + Markdown | Individual component JSON + Markdown |

## Advanced Usage

### Custom Analysis

For custom analysis logic, you can use the components directly:

```python
from OrchestratorAgent.orchestrator_saga import OrchestratorAgent

orchestrator = OrchestratorAgent()

# Load and analyze
saga_data = orchestrator._load_saga_directory("SagaAgent/exports/")
analysis = orchestrator.analyze_saga(saga_data, "Custom feedback")

# Display results
orchestrator.display_analysis(analysis)

# Manually update specific components
components = analysis.get_components_to_update()
orchestrator.update_state_from_saga(saga_data)

for component in components:
    feedback = analysis.get_feedback_for_component(component)
    orchestrator.update_component(component, feedback)

# Export
orchestrator.export_saga()
```

## Troubleshooting

### Issue: "No API key found"

**Solution**: Make sure you have set either `OPENAI_API_KEY` or `GOOGLE_API_KEY` in your `.env` file.

### Issue: "File not found"

**Solution**: Provide the full path to the saga file or directory, or run from the project root directory.

### Issue: "Model not recognized"

**Solution**: Use a supported model name. See `SagaAgent/config.py` for the list of supported models.

### Issue: Updates not applying

**Solution**: Check that the components exist in the saga files. The orchestrator can only update components that are present.

### Issue: Too many components updated

**Solution**: By default, the orchestrator is conservative and only updates what you explicitly mention. If too many components are being updated, your feedback might be too general. Be more specific about which component you want to update.

## Contributing

To extend the orchestrator:

1. Add new models to `models/orchestrator.py`
2. Add new prompts to `prompts/orchestrator_prompts.py`
3. Add new update logic to `orchestrator_saga.py`
4. Update tests and documentation

## License

Same as SagaAgent main project.


