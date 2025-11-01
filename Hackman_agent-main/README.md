# ScriptEngineX

> A multi-agent LangGraph-based system for story generation and research.

## 🚀 Overview

ScriptEngineX provides three primary capabilities:
- **Supervisor Agent**: orchestrates end-to-end workflows from research to story generation
- **ArcueAgent**: an interactive, checkpointed story-generation workflow  
- **Research**: a web-research workflow with iterative search and synthesis

All components are orchestrated with LangGraph and use structured state to ensure resumability and clear outputs. The system supports both interactive human-in-the-loop workflows and fully automated end-to-end generation.

## ✨ Key Features

### 🎯 Supervisor Architecture
- End-to-end workflow orchestration from research to story generation
- Intelligent routing decisions based on topic complexity
- Seamless integration of Research and ArcueAgent workflows
- Unified state management across all components

### 🎭 Interactive Story Generation (ArcueAgent)
- Checkpointed workflow: draft → characters → plot → locations → scenes
- Human-in-the-loop feedback at each stage
- Structured outputs using Pydantic models
- Optional export utilities for assembling outputs

### 📚 Research Capabilities
- Iterative web search using Tavily API
- Multi-model support (Google Gemini, OpenAI, Anthropic optional)
- Intelligent content summarization and synthesis
- Compressed research summaries + raw notes preservation
- Strategic reflection tools for research quality control

### 🔧 Technical
- LangGraph-based graphs with interrupts/checkpoints
- Programmatic and CLI entry points
- Environment-based configuration

## 🏗️ Current Project Structure

```text
ScriptEngineX/
├── supervisor_agent.py        # Main supervisor orchestration
├── supervisor_state.py        # Supervisor state definitions
├── ArcueAgent/                # Story generation system
│   ├── agent.py              # Core LangGraph agent
│   ├── config.py             # Configuration helpers
│   ├── langgraph.json        # LangGraph CLI mapping
│   ├── models/               # Pydantic data models
│   │   ├── draft.py
│   │   ├── characters.py
│   │   ├── plot.py
│   │   ├── locations.py
│   │   ├── scenes.py
│   │   ├── dialogue.py
│   │   ├── script.py
│   │   ├── ad.py
│   │   └── visual_lookbook.py
│   ├── nodes/                # Graph node implementations
│   │   ├── draft_node.py
│   │   ├── characters_node.py
│   │   ├── plot_node.py
│   │   ├── locations_node.py
│   │   ├── scenes_node.py
│   │   ├── dialogue_node.py
│   │   ├── compilation_node.py
│   │   ├── export_nodes.py
│   │   ├── ad_nodes.py
│   │   └── visual_lookbook_node.py
│   ├── prompts/              # Prompt templates
│   │   └── prompt_templates.py
│   ├── services/             # Supporting services
│   │   ├── llm_service.py
│   │   ├── export_service.py
│   │   └── user_export_service.py
│   ├── utils/                # Utilities
│   │   ├── state.py
│   │   └── tools.py
│   └── README.md
├── Research/                  # Research agent
│   ├── research_agent.py
│   ├── run_research.py
│   ├── prompts.py
│   ├── llm.py
│   ├── state_research.py
│   └── utils.py
├── main.py                    # Simple entry point
├── pyproject.toml             # Project metadata and dependencies
├── LICENSE
└── README.md                  # This file
```

## 🛠️ Installation

### Prerequisites
- **Python**: 3.12+
- **API Keys**:
  - `GOOGLE_API_KEY` (required - primary model)
  - `OPENAI_API_KEY` (optional - alternative model)
  - `TAVILY_API_KEY` (required for research)

### Install
Using pip (editable install recommended during development):

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Or with `uv` if available:

```bash
uv sync
```

### Configure Environment
Create a `.env` in the project root:

```env
# API Keys - At least one model provider required
# Priority: OPENAI_API_KEY > GOOGLE_API_KEY
OPENAI_API_KEY=your_openai_api_key      # For GPT-5, GPT-4, etc. (default if provided)
GOOGLE_API_KEY=your_google_api_key      # For Gemini models (fallback)

# Required for Research functionality
TAVILY_API_KEY=your_tavily_api_key

# Model Selection (optional - auto-selects based on API keys if not set)
MODEL=gpt-5                              # Main model for ArcueAgent story generation
                                         # Options: gpt-5, gpt-5-mini, gpt-4, gpt-4-turbo, gpt-4o,
                                         #          gemini-2.5-pro, gemini-2.5-flash, etc.

SUPERVISOR_MODEL=gpt-5                   # Model for supervisor orchestration

RESEARCH_MODEL=gpt-5                     # Model for research agent
RESEARCH_EVALUATOR_MODEL=gpt-5           # Model for research evaluation

# Model Configuration (optional)
MODEL_TEMPERATURE=0.7                    # Creativity level (0.0 - 1.0)
RANDOM_SEED=42                           # For reproducible outputs

# Film Configuration (optional)
FILM_LENGTH_SECONDS=90                   # Target film length
NUMBER_OF_SCENES=12                      # Number of scenes to generate
```

## 🎯 Usage

### Supervisor Agent (End-to-End Workflow)
Run the complete workflow from topic to finished story:

```bash
python supervisor_agent.py
```

The supervisor will:
1. **Topic Analysis**: Analyze your topic and intelligently decide if research is needed
2. **Research Phase** (if required): Conduct comprehensive research using Tavily web search
3. **Draft Generation**: Create an enriched initial draft incorporating research insights
4. **Story Development**: Generate characters, plot, dialogue, locations, and scenes
5. **Final Assembly**: Compile and export the complete screenplay

**Key Features:**
- Intelligent routing based on topic complexity
- Research-enriched creative writing
- Fully automated end-to-end generation
- Structured outputs with comprehensive metadata

### Supervisor Agent (Programmatic)
```python
from supervisor_agent import supervisor_graph
import uuid

# Initialize state
initial_state = {
    "topic": "AI ethics in healthcare",
    "workflow_stage": "initial",
    "needs_research": False,
    "research_complete": False,
    "writing_complete": False,
    "raw_notes": [],
    "researcher_messages": [],
    "messages": []
}

# Run complete workflow
result = supervisor_graph.invoke(initial_state)

# Access results
print(f"Research completed: {result.get('research_complete', False)}")
print(f"Writing completed: {result.get('writing_complete', False)}")
print(f"Final script: {result.get('final_script')}")
print(f"Export path: {result.get('export_path')}")
```

### Supervisor Agent (Advanced Configuration)
```python
# Custom configuration for specific use cases
initial_state = {
    "topic": "Historical drama about the Renaissance",
    "workflow_stage": "initial",
    "film_length_seconds": 120,  # 2-hour film
    "number_of_scenes": 15,
    "model": "gpt-5",  # Specify model
    "model_temperature": 0.7,
    "ad_mode": False,  # Set to True for advertisement generation
}

result = supervisor_graph.invoke(initial_state)
```

### ArcueAgent (Interactive CLI)
Run the interactive, checkpointed story workflow:

```bash
python -m ArcueAgent.agent
```

You'll progress through 7 checkpoints:
1) **Initial Draft**: Create the foundational story concept
2) **Characters**: Develop detailed character profiles
3) **Plot**: Structure the narrative arc and plot points
4) **Dialogue**: Generate key dialogue scenes
5) **Locations**: Design story world and settings
6) **Visual Lookbook**: Define visual style and aesthetics
7) **Scenes**: Create detailed scene breakdowns

At each step, provide feedback or press Enter to continue. Generated outputs are saved to Markdown files.

### ArcueAgent (Programmatic)
```python
from ArcueAgent.agent import story_agent
import uuid

# Basic usage
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

initial_state = {
    "log_line": "A robot discovers it has emotions",
    "film_length_seconds": 90,
    "number_of_scenes": 12
}

final_state = story_agent.invoke(initial_state, config=config)
print(final_state.get("final_script"))
```

### ArcueAgent (Advanced Configuration)
```python
# Custom configuration for specific requirements
initial_state = {
    "log_line": "Historical drama about Renaissance artists",
    "film_length_seconds": 120,  # 2-hour film
    "number_of_scenes": 15,
    "model": "gpt-5",
    "model_temperature": 0.7,
    "ad_mode": False,  # Set to True for advertisement generation
}

# Ad mode configuration
ad_state = {
    "log_line": "Brand advertisement concept",
    "ad_mode": True,
    "ad_total_seconds": 30,
    "ad_scene_seconds": 5,
    "ad_brand": "TechCorp",
    "ad_product": "AI Assistant",
    "ad_goal": "Brand awareness",
    "ad_audience": "Tech professionals",
    "ad_tone": "Professional yet approachable",
    "ad_offer": "Free trial",
    "ad_constraints": "Must include call-to-action"
}

result = story_agent.invoke(ad_state, config=config)
```

**ArcueAgent Features:**
- **Checkpointed Workflow**: Resume from any stage using thread_id
- **Human-in-the-Loop**: Interactive feedback at each stage
- **Structured Outputs**: Pydantic models ensure consistent data structure
- **Export Options**: Multiple export formats (JSON, Markdown, user-friendly views)
- **Ad Mode**: Specialized workflow for advertisement generation
- **Visual Lookbook**: AI-generated visual style guidelines

### LangGraph CLI (Dev and API)
This repo includes a `langgraph.json` for the ArcueAgent graph.

```bash
# Start development UI
langgraph dev

# Start API server
langgraph api start
```

### Research Agent (CLI)
```bash
python -m Research.run_research
```

### Research Agent (Programmatic)
```python
from Research.research_agent import researcher_agent
from langchain_core.messages import HumanMessage

# Initialize research state
initial_state = {
    "researcher_messages": [HumanMessage(content="Impact of AI on creative industries")],
    "research_topic": "Impact of AI on creative industries",
    "tool_call_iterations": 0,
    "compressed_research": "",
    "raw_notes": []
}

# Run research workflow
result = researcher_agent.invoke(initial_state)

# Access results
print(f"Compressed research: {result['compressed_research']}")
print(f"Raw notes: {len(result['raw_notes'])} notes")
print(f"Research messages: {len(result['researcher_messages'])} messages")
```

### Research Agent (Advanced Usage)
```python
# Custom research with specific parameters
from Research.utils import tavily_search

# Direct tool usage
search_results = tavily_search.invoke({
    "query": "AI ethics in healthcare 2024",
    "max_results": 3,
    "topic": "general"
})

print(search_results)
```

**Research Features:**
- **Intelligent Search**: Uses Tavily API for comprehensive web search
- **Content Summarization**: Automatically summarizes web content for better processing
- **Strategic Reflection**: Built-in reflection tools for research quality control
- **Multi-iteration Research**: Continues searching until comprehensive coverage
- **Structured Output**: Compressed summaries + raw notes preservation

## 🔧 Configuration

Key dependencies and versions (from `pyproject.toml`):
- `langgraph>=0.6.7`
- `langchain>=0.3.27`
- `langchain-core>=0.3.75`
- `langchain-openai>=0.3.32`
- `langchain-google-genai>=2.0.0`
- `tavily-python>=0.7.11`
- `ipython>=9.5.0`
- `dotenv>=0.9.9`

Python requirement: `>=3.12`.

### Environment Variables

#### API Keys (Required)
At least one model provider API key is required:

| Variable | Description | Priority |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-5, GPT-4, etc. | **Primary** (used if present) |
| `GOOGLE_API_KEY` | Google API key for Gemini models | Fallback |
| `TAVILY_API_KEY` | Required for research functionality | - |

#### Model Selection (Optional)
If not specified, models are auto-selected based on available API keys:

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL` | Main model for ArcueAgent story generation | `gpt-5` (if OPENAI_API_KEY set), else `gemini-2.5-pro` |
| `SUPERVISOR_MODEL` | Model for supervisor orchestration | Same as `MODEL` |
| `RESEARCH_MODEL` | Model for research agent | Same as `MODEL` |
| `RESEARCH_EVALUATOR_MODEL` | Model for research evaluation | Same as `RESEARCH_MODEL` |

**Supported Models:**
- **OpenAI**: `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `gpt-4`, `gpt-4-turbo`, `gpt-4o`, `gpt-3.5-turbo`
- **Google**: `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-1.5-pro`, `gemini-1.5-flash`

#### Model Configuration (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_TEMPERATURE` | Creativity level (0.0 - 1.0) | `0.5` |
| `RANDOM_SEED` | For reproducible outputs | None |

#### Film Configuration (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `FILM_LENGTH_SECONDS` | Target film length in seconds | `90` |
| `NUMBER_OF_SCENES` | Number of scenes to generate | `12` |

#### Runtime Settings (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `THREAD_ID` | Custom thread ID for checkpointing | Auto-generated UUID |
| `AUTO_CONTINUE` | Auto-continue through stages | `true` |
| `CHECKPOINT_ID` | Resume from specific checkpoint | None |
| `TIME_TRAVEL_LIST` | List checkpoint history | `false` |
| `LOG_LINE` | Custom log line/story concept | None |

#### Ad Mode Configuration (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `AD_MODE` | Enable advertisement generation mode | `false` |
| `AD_BRAND` | Brand name for ad | None |
| `AD_PRODUCT` | Product name for ad | None |
| `AD_GOAL` | Advertisement goal | None |
| `AD_AUDIENCE` | Target audience | None |
| `AD_TONE` | Ad tone/style | None |
| `AD_OFFER` | Special offer/CTA | None |
| `AD_CONSTRAINTS` | Creative constraints | None |
| `AD_TOTAL_SECONDS` | Total ad duration | `90` |
| `AD_SCENE_SECONDS` | Duration per scene | `8` |

#### API Server Configuration (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |

## 📊 Workflows

### Supervisor End-to-End Workflow
1. Topic Analysis & Research Decision
2. Research (if needed) using Tavily web search
3. Story Generation using ArcueAgent
4. Final Assembly & Export

### Story Generation (ArcueAgent)
1. **Initial Draft**: Foundation story concept and structure
2. **Character Development**: Detailed character profiles and arcs
3. **Plot Structure**: Narrative arc, plot points, and dramatic structure
4. **Dialogue Generation**: Key dialogue scenes and character voice
5. **World Building**: Locations, settings, and environmental design
6. **Visual Lookbook**: Visual style, aesthetics, and mood boards
7. **Scene Creation**: Detailed scene breakdowns and transitions
8. **Final Assembly**: Script compilation and export

### Research (Standalone)
1. **Query Analysis**: Understanding research requirements and scope
2. **Iterative Search**: Multi-round web search using Tavily API
3. **Content Summarization**: Intelligent summarization of web content
4. **Strategic Reflection**: Quality control and gap analysis
5. **Synthesis**: Compressed research summary generation
6. **Notes Preservation**: Raw research data retention

## 🤝 Contributing
- Fork, create a feature branch, and open a PR
- Add/adjust nodes or services under `ArcueAgent/` as needed
- Keep README sections in sync with structure and `pyproject.toml`

## 📝 License
Licensed under the terms in `LICENSE`.

---

**ScriptEngineX** — Intelligent multi-agent collaboration for creative work.
