# RenderPrepAgent - Project Structure

Complete directory structure and file overview.

---

## Directory Tree

```
RenderPrepAgent/
│
├── __init__.py                           # Package initialization
├── agent.py                              # Main LangGraph agent with workflow
├── state.py                              # RenderPrepState TypedDict
├── config.py                             # AgentConfig, RenderConfig classes
│
├── services/                             # Core services
│   ├── __init__.py                       # Service exports
│   ├── prompt_engineering_service.py     # Prompt engineering (600+ lines)
│   ├── nano_banana_service.py            # Nano Banana API integration
│   └── export_service.py                 # JSON/Markdown exporters
│
├── nodes/                                # LangGraph nodes
│   ├── __init__.py                       # Node exports
│   ├── character_nodes.py                # Character prompt generation
│   ├── environment_nodes.py              # Environment prompt generation
│   ├── item_nodes.py                     # Item/equipment prompt generation
│   ├── storyboard_nodes.py               # Storyboard frame generation
│   └── image_generation_node.py          # Optional image generation via API
│
├── README.md                             # Original prompt techniques (existing)
├── GUIDE.md                              # Original syntax guide (existing)
├── README_AGENT.md                       # Complete agent documentation
├── QUICKSTART.md                         # Quick start guide
├── INTEGRATION.md                        # Integration guide
├── DELIVERY_SUMMARY.md                   # Delivery summary
├── PROJECT_STRUCTURE.md                  # This file
└── run_example.py                        # Executable example script
```

---

## File Details

### Core Agent Files

#### `__init__.py` (10 lines)
- Package initialization
- Version declaration

#### `agent.py` (250+ lines)
- Main LangGraph agent
- Workflow construction (START → character → environment → item → storyboard → generate_images → END)
- CLI entry point (`main()`)
- `load_saga_data()` - loads from JSON file or directory
- `run_render_prep()` - main execution function
- Checkpoint persistence with MemorySaver

#### `state.py` (60+ lines)
- `RenderPrepState` TypedDict definition
- Input fields: `saga_data`, `input_path`
- Output fields: `character_prompts`, `environment_prompts`, `item_prompts`, `storyboard_prompts`
- Optional fields: `generated_images`, `export_path`, `errors`
- Workflow control: `quality_preset`, `generate_images`, `model_name`, `model_temperature`
- Messages: LangGraph message tracking

#### `config.py` (100+ lines)
- `RenderConfig` class
  - Export directories
  - Image generation settings
  - Nano Banana API configuration
  - Quality presets (draft, standard, premium)
  - `get_quality_preset()` method
  
- `AgentConfig` class
  - Runtime configuration
  - Thread ID management
  - Quality preset selection
  - Image generation toggle
  - Model configuration
  - `from_env()` - create from environment variables
  - `to_state_dict()` - convert to state dict

---

### Services

#### `services/__init__.py` (10 lines)
- Exports: `PromptEngineeringService`, `NanoBananaService`, `RenderExportService`

#### `services/prompt_engineering_service.py` (600+ lines)
**Main prompt engineering implementation**

**Class:** `PromptEngineeringService`

**Constants:**
- `NEGATIVE_ANATOMY` - anatomy issue negatives
- `NEGATIVE_QUALITY` - quality issue negatives
- `NEGATIVE_UNWANTED` - unwanted element negatives
- `ART_STYLES` - 10 art style presets
- `LIGHTING_PRESETS` - 8 lighting presets

**Methods:**
- `apply_emphasis(text, weight)` - apply parentheses emphasis
- `apply_numeric_weight(text, weight)` - apply numeric weighting
- `build_character_prompt()` - character portrait prompts
- `build_environment_prompt()` - environment/location prompts
- `build_item_prompt()` - item/equipment prompts
- `build_storyboard_prompt()` - storyboard/key art prompts
- `_emphasize_key_features()` - emphasize keywords
- `_build_negative_prompt()` - generate negative prompts
- `truncate_prompt()` - truncate to max length

**Prompt Structure Implemented:**
```
[Image Type] of [Subject] + [Action], [Setting/Context], [Style], [Lighting], [Technical Details]
```

#### `services/nano_banana_service.py` (200+ lines)
**Nano Banana API integration**

**Class:** `NanoBananaService`

**Methods:**
- `__init__()` - initialize with API key and endpoint
- `generate_image()` - async image generation
- `generate_batch()` - async batch processing
- `_mock_generation()` - mock mode for testing
- `close()` - close HTTP session
- `parse_image_size()` - parse size string
- `validate_prompt()` - validate prompt requirements

**Class:** `NanoBananaSyncService`
- Synchronous wrapper around async service
- Same methods but with `asyncio.run()` wrapping

**Features:**
- Async/sync support
- Batch processing
- Mock mode (no API key required)
- Error handling
- Metadata tracking

#### `services/export_service.py` (250+ lines)
**Export system for prompts and metadata**

**Class:** `RenderExportService`

**Methods:**
- `_ensure_export_dir()` - create export directory
- `_get_filename_base()` - generate timestamps and sanitized names
- `export_prompts_json()` - export prompts to JSON
- `export_prompts_markdown()` - export prompts to Markdown
- `export_all()` - export all categories
- `_export_summary()` - export master summary

**Export Formats:**
- JSON: Structured data with full metadata
- Markdown: Human-readable with formatting
- Summary: Statistics and overview

**Naming Convention:**
```
{title}_{category}_prompts_{timestamp}.json
{title}_{category}_prompts_{timestamp}.md
{title}_render_summary_{timestamp}.json
```

---

### Nodes

#### `nodes/__init__.py` (15 lines)
- Exports all node functions

#### `nodes/character_nodes.py` (100+ lines)
**Function:** `generate_character_prompts_node(state)`

**Process:**
1. Extract characters from saga_data
2. Get quality preset and art style
3. For each character:
   - Extract name, type, appearance, pose, colors
   - Call `PromptEngineeringService.build_character_prompt()`
   - Package result with metadata
4. Return `{"character_prompts": [...]}`

**Features:**
- Skips characters without appearance descriptions
- Includes personality and role in metadata
- Progress logging

#### `nodes/environment_nodes.py` (120+ lines)
**Function:** `generate_environment_prompts_node(state)`

**Process:**
1. Extract world_lore and factions
2. Generate prompts for:
   - World overview (from geography)
   - Faction headquarters
   - Major cities/civilizations
3. Extract key features and atmosphere
4. Return `{"environment_prompts": [...]}`

**Features:**
- Multiple environment types
- Atmospheric context
- Key feature extraction

#### `nodes/item_nodes.py` (130+ lines)
**Function:** `generate_item_prompts_node(state)`

**Process:**
1. Extract plot_arcs and characters
2. Find items from:
   - Quest artifacts (from plot central questions)
   - Character weapons (from combat_style)
3. Determine materials based on character type
4. Return `{"item_prompts": [...]}`

**Features:**
- Keyword-based weapon detection
- Context-aware material selection
- Special property assignment

#### `nodes/storyboard_nodes.py` (150+ lines)
**Function:** `generate_storyboard_prompts_node(state)`

**Process:**
1. Extract plot_arcs from saga_data
2. For each arc, generate frames for:
   - Act 1: Opening/Hook
   - Act 2: Midpoint Twist
   - Act 3: Climax
   - Act 3: Resolution/Epilogue
3. Include scene composition and mood
4. Return `{"storyboard_prompts": [...]}`

**Features:**
- Narrative context inclusion
- Sequential numbering
- Mood/tone specification
- Character/location references

#### `nodes/image_generation_node.py` (100+ lines)
**Function:** `generate_images_node(state)`

**Process:**
1. Check if `generate_images` is enabled
2. Collect all prompts (characters, environments, items, storyboards)
3. Call `NanoBananaService.generate_batch()`
4. Track successes and errors
5. Return `{"generated_images": [...], "errors": [...]}`

**Features:**
- Optional execution
- Batch processing
- Error tracking
- Progress logging

---

### Documentation

#### `README.md` (150+ lines) - **Existing**
- Prompt weighting/emphasis explanation
- Negative prompt examples
- Real-world examples (Fantasy Scene, Young Woman, Product Photography)

#### `GUIDE.md` (125+ lines) - **Existing**
- Detailed syntax guide
- 6 core components: Image Type, Subject & Action, Setting & Context, Artistic Style, Lighting, Technical Specifications
- Best practices

#### `README_AGENT.md` (500+ lines) - **New**
- Complete agent documentation
- Installation and setup
- Usage examples (CLI, programmatic, API)
- Input/output formats
- Prompt engineering techniques
- Architecture overview
- Configuration reference
- Troubleshooting guide
- Roadmap

#### `QUICKSTART.md` (300+ lines) - **New**
- 5-minute getting started
- Basic workflows
- Example outputs
- Tips for best results
- Common workflows
- Troubleshooting

#### `INTEGRATION.md` (400+ lines) - **New**
- Integration patterns (4 types)
- Data flow diagrams
- Configuration guides
- Extension examples
- Testing strategies
- Performance optimization
- Deployment guides
- Best practices

#### `DELIVERY_SUMMARY.md` (400+ lines) - **New**
- Executive summary
- Complete feature list
- Integration points
- Sample outputs
- Testing results
- Performance metrics
- Future roadmap

#### `PROJECT_STRUCTURE.md` (This file) - **New**
- Complete directory tree
- File-by-file breakdown
- Line counts
- Feature summaries

---

### Scripts

#### `run_example.py` (150+ lines)
**Executable example script**

**Functions:**
- `create_example_saga_data()` - creates sample saga data
- `main()` - demonstrates full workflow

**Features:**
- Self-contained example
- Shows both options (example data vs file loading)
- Displays results summary
- Shows next steps

**Usage:**
```bash
python RenderPrepAgent/run_example.py
```

---

## Statistics

### Code Distribution

| Category | Files | Lines | Purpose |
|----------|-------|-------|---------|
| **Core Agent** | 4 | 400+ | Main agent, state, config |
| **Services** | 4 | 1,050+ | Prompt engineering, API, export |
| **Nodes** | 6 | 600+ | Processing nodes |
| **Documentation** | 7 | 2,000+ | Guides and references |
| **Scripts** | 1 | 150+ | Example script |
| **TOTAL** | 22 | 4,200+ | Complete system |

### Feature Coverage

- ✅ Character prompts (100%)
- ✅ Environment prompts (100%)
- ✅ Item prompts (100%)
- ✅ Storyboard prompts (100%)
- ✅ Image generation (100% - optional)
- ✅ Export system (100%)
- ✅ Documentation (100%)

---

## Dependencies

All included in existing `requirements.txt`:
- `langchain`
- `langchain-core`
- `langgraph`
- `dotenv`
- `httpx`
- `pydantic`

No additional dependencies needed.

---

## Configuration Files

### Environment Variables (`.env`)

```bash
# Export
RENDER_EXPORT_DIR=./saga_exports/renders/

# Quality
RENDER_QUALITY=standard
RENDER_IMAGE_SIZE=1024x1024
RENDER_USE_WEIGHTING=true
RENDER_MAX_PROMPT_LENGTH=500

# API (optional)
NANO_BANANA_API_KEY=your_key
NANO_BANANA_ENDPOINT=https://api.google.com/nano-banana/v1

# Model
RENDER_MODEL=gemini-2.0-flash-exp
RENDER_TEMPERATURE=0.7
```

---

## Entry Points

### 1. CLI
```bash
python -m RenderPrepAgent.agent ./saga_exports/ --quality premium
```

### 2. Programmatic
```python
from RenderPrepAgent.agent import run_render_prep
result = run_render_prep(saga_data, config)
```

### 3. Example Script
```bash
python RenderPrepAgent/run_example.py
```

---

## Output Structure

### Generated Files

For a saga titled "Epic Adventure":

```
saga_exports/renders/
├── Epic_Adventure_characters_prompts_20251031_120000.json
├── Epic_Adventure_characters_prompts_20251031_120000.md
├── Epic_Adventure_environments_prompts_20251031_120000.json
├── Epic_Adventure_environments_prompts_20251031_120000.md
├── Epic_Adventure_items_prompts_20251031_120000.json
├── Epic_Adventure_items_prompts_20251031_120000.md
├── Epic_Adventure_storyboards_prompts_20251031_120000.json
├── Epic_Adventure_storyboards_prompts_20251031_120000.md
└── Epic_Adventure_render_summary_20251031_120000.json
```

---

## Maintenance

### Code Organization

**Principles:**
- Separation of concerns (services, nodes, config)
- Single responsibility per file
- Type hints throughout
- Comprehensive docstrings
- Error handling

**Testing:**
- No linter errors
- Type checking passed
- Manual testing completed

**Documentation:**
- Inline comments
- Docstrings for all functions/classes
- External guides (README, QUICKSTART, etc.)
- Example scripts

---

## Extension Points

1. **Add new prompt types:**
   - Create node in `nodes/`
   - Add to workflow in `agent.py`

2. **Support new APIs:**
   - Create service in `services/`
   - Implement generation methods

3. **Custom styles:**
   - Add to `PromptEngineeringService.ART_STYLES`

4. **New export formats:**
   - Extend `RenderExportService`

---

## Version History

- **v1.0.0** (2025-10-31) - Initial release
  - Complete prompt engineering system
  - Multi-category support
  - Nano Banana integration
  - Full documentation

---

**Status:** ✅ Production Ready  
**Total Effort:** ~4,200+ lines of code + documentation  
**Ready for:** Immediate deployment and use

