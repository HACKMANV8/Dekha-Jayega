# Orchestrator Agent

## Overview

The **Orchestrator Agent** is an intelligent story revision system for ArcueAgent that analyzes existing `user_view` files, provides structured LLM feedback, and selectively updates only the components that need improvement.

## Key Features

- 🤖 **AI-Powered Analysis**: Uses OpenAI or Gemini models to analyze story quality
- 🎯 **Selective Updates**: Only updates components that need improvement
- 📊 **Structured Feedback**: Provides detailed, actionable feedback for each component
- 🔄 **Iterative Refinement**: Can be run multiple times for continuous improvement
- 💬 **Interactive Mode**: Component-by-component confirmation and editing
- ⚡ **Auto Mode**: Fully automated revision workflow

## Architecture

The orchestrator consists of:

1. **Models** (`models/orchestrator.py`):
   - `UserViewAnalysis`: Structured analysis with component feedback
   - `ComponentFeedback`: Feedback for individual components
   - `RevisionPlan`: Plan for applying updates

2. **Prompts** (`prompts/orchestrator_prompts.py`):
   - Analysis prompts for LLM
   - Formatting utilities for user_view data

3. **Agent** (`orchestrator.py`):
   - Main orchestration logic
   - Component update workflows
   - State management

4. **CLI** (`run_orchestrator.py`):
   - User-friendly command-line interface
   - Multiple operation modes

## Usage

### Basic Usage

Analyze a user_view file and prompt for confirmation before updates:

```bash
python run_orchestrator.py ArcueAgent/exports/Story_USER_VIEW_20231022.json
```

### Auto Mode

Automatically apply all updates without confirmation:

```bash
python run_orchestrator.py ArcueAgent/exports/Story_USER_VIEW_20231022.json --auto
```

### Interactive Mode

Get component-by-component confirmation and editing:

```bash
python run_orchestrator.py ArcueAgent/exports/Story_USER_VIEW_20231022.json --interactive
```

### Custom Model

Use a specific model (OpenAI or Gemini):

```bash
python run_orchestrator.py ArcueAgent/exports/Story_USER_VIEW_20231022.json --model gemini-2.5-pro
```

### With Custom Feedback

Provide your own feedback in addition to AI analysis:

```bash
python run_orchestrator.py ArcueAgent/exports/Story_USER_VIEW_20231022.json --feedback
```

## Environment Setup

Create a `.env` file with your API keys:

```bash
# OpenAI (if using OpenAI models)
OPENAI_API_KEY=your_openai_key_here

# Google (if using Gemini models)
GOOGLE_API_KEY=your_google_key_here

# Model selection (optional, auto-detects based on available keys)
MODEL=gpt-5
# or
MODEL=gemini-2.5-pro

# Temperature (optional)
MODEL_TEMPERATURE=0.3

# Random seed for reproducibility (optional)
RANDOM_SEED=42
```

## Workflow

1. **Load**: Reads the existing user_view JSON file
2. **Analyze**: LLM analyzes story and provides structured feedback
3. **Display**: Shows analysis with coherence score and component feedback
4. **Confirm**: User confirms which components to update (unless --auto)
5. **Update**: Selectively updates only the components that need improvement
6. **Export**: Generates new user_view files with timestamp

## Component Updates

The orchestrator can update these components:

- **draft**: Initial story draft
- **characters**: Character profiles
- **dialogue**: Character dialogue
- **locations**: Story locations
- **visual_lookbook**: Visual style and aesthetics
- **scenes**: Individual scenes with camera work

### Update Priority

Components are updated in priority order:
- Priority 1 (High): Critical issues affecting story coherence
- Priority 2 (Medium): Important improvements
- Priority 3 (Low): Nice-to-have refinements

### Dependency Handling

The orchestrator respects component dependencies:
1. Draft is updated first (foundation)
2. Characters, locations, visual_lookbook can run in parallel
3. Dialogue depends on characters
4. Scenes depend on all other components

## Output

The orchestrator generates new user_view files with timestamps:

```
ArcueAgent/exports/
  - Story_USER_VIEW_20231022_143022.json    (original)
  - Story_USER_VIEW_20231022_150133.json    (revised - new)
  - Story_USER_VIEW_20231022_150133.md      (revised - new)
```

You can run the orchestrator again on the new files for further refinement.

## Examples

### Example 1: Quick Revision

```bash
# Analyze and auto-apply updates
python run_orchestrator.py exports/MyStory_USER_VIEW.json --auto
```

### Example 2: Careful Review

```bash
# Interactive mode with step-by-step confirmation
python run_orchestrator.py exports/MyStory_USER_VIEW.json --interactive
```

### Example 3: Specific Model with Feedback

```bash
# Use Gemini with custom feedback
python run_orchestrator.py exports/MyStory_USER_VIEW.json --model gemini-2.5-pro --feedback
```

## Integration with Main Workflow

The orchestrator complements the main story generation workflow:

1. **Initial Generation**: Run `python main.py` to create initial story
2. **Review**: Check the generated `USER_VIEW` files
3. **Refine**: Run orchestrator to improve specific components
4. **Iterate**: Run orchestrator multiple times for continuous refinement

## Programmatic Usage

You can also use the orchestrator in your own scripts:

```python
from ArcueAgent.orchestrator import OrchestratorAgent
from ArcueAgent.config import AgentConfig

# Create orchestrator
config = AgentConfig.from_env()
orchestrator = OrchestratorAgent(config)

# Run revision workflow
new_json, new_markdown = orchestrator.orchestrate_revision(
    user_view_filepath="exports/Story_USER_VIEW.json",
    user_feedback="Make the dialogue more natural",
    auto_apply=True
)

print(f"New files: {new_json}, {new_markdown}")
```

## Advanced: Custom Analysis

For custom analysis logic, you can use the components directly:

```python
from ArcueAgent.orchestrator import OrchestratorAgent

orchestrator = OrchestratorAgent()

# Load and analyze
user_view = orchestrator.load_user_view("path/to/file.json")
analysis = orchestrator.analyze_user_view(user_view, "Custom feedback")

# Display results
orchestrator.display_analysis(analysis)

# Manually update specific components
components = analysis.get_components_to_update()
orchestrator.update_state_from_user_view(user_view)

for component in components:
    feedback = analysis.get_feedback_for_component(component)
    orchestrator.update_component(component, feedback)

# Export
orchestrator.compile_and_export()
```

## Troubleshooting

### Issue: "No API key found"

**Solution**: Make sure you have set either `OPENAI_API_KEY` or `GOOGLE_API_KEY` in your `.env` file.

### Issue: "File not found"

**Solution**: Provide the full path to the user_view JSON file, or run from the project root directory.

### Issue: "Model not recognized"

**Solution**: Use a supported model name. See `ArcueAgent/config.py` for the list of supported models.

### Issue: Updates not applying

**Solution**: Check that the components exist in the user_view file. The orchestrator can only update components that are present.

## Best Practices

1. **Iterative Refinement**: Run the orchestrator multiple times on the same story for continuous improvement
2. **Start with Auto Mode**: Use `--auto` for quick revisions, then switch to `--interactive` for fine-tuning
3. **Model Selection**: Use faster models (gpt-5-mini, gemini-2.5-flash) for quick iterations
4. **Backup Files**: The orchestrator preserves original files by creating new timestamped versions
5. **Review Analysis**: Always review the analysis output before applying updates

## Contributing

To extend the orchestrator:

1. Add new models to `models/orchestrator.py`
2. Add new prompts to `prompts/orchestrator_prompts.py`
3. Add new update logic to `orchestrator.py`
4. Update tests and documentation

## License

Same as ArcueAgent main project.

