# Graph state
from typing import TypedDict, Literal
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")


class GameConcept(BaseModel):
    """Structured video game concept document."""
    title: str = Field(description="A catchy working title for the game.")
    genre: str = Field(description="Primary and sub-genres, e.g., 'Action RPG, Roguelite'.")
    elevator_pitch: str = Field(description="1-2 sentence pitch capturing the essence and hook.")
    core_loop: str = Field(description="Bullet-style description of what players repeatedly do.")
    key_mechanics: str = Field(description="Key mechanics and systems that define gameplay.")
    progression: str = Field(description="How players progress: meta, unlocks, difficulty, story.")
    world_setting: str = Field(description="Setting, tone, and brief world lore.")
    art_style: str = Field(description="Art direction references and visual style notes.")
    target_audience: str = Field(description="Intended players and platforms.")
    monetization: str = Field(description="Premium/Free-to-Play model and ethical considerations.")
    usp: str = Field(description="Unique Selling Proposition: what makes this stand out.")


class ConceptReview(BaseModel):
    """Evaluator review for the concept document."""
    decision: Literal["accept", "revise"] = Field(description="Accept if clear and complete; otherwise revise.")
    feedback: str = Field(description="Specific, actionable feedback to improve weak areas.")


class ConceptState(TypedDict):
    idea: str
    concept_md: str
    feedback: str
    decision: str


# Prepare evaluator with structured output (force JSON schema to avoid tool-calling)
evaluator = llm.with_structured_output(ConceptReview, method="json_schema")


def generate_concept(state: ConceptState):
    """Generate a structured video game concept (as markdown)."""
    idea = state["idea"]

    guidance = (
        f"You are a veteran game designer. Create a concise but complete video game concept based on: '{idea}'. "
        "Return each section clearly labeled. Be specific, avoid clichés, and ensure a strong core loop."
    )

    if state.get("feedback"):
        guidance += f" Incorporate the following feedback: {state['feedback']}"

    # Force JSON schema method to avoid tool-calling on Groq
    schema = llm.with_structured_output(GameConcept, method="json_schema")
    concept = schema.invoke(guidance)

    md = (
        f"# {concept.title}\n\n"
        f"**Genre**: {concept.genre}\n\n"
        f"**Elevator Pitch**: {concept.elevator_pitch}\n\n"
        f"## Core Loop\n{concept.core_loop}\n\n"
        f"## Key Mechanics\n{concept.key_mechanics}\n\n"
        f"## Progression\n{concept.progression}\n\n"
        f"## World & Setting\n{concept.world_setting}\n\n"
        f"## Art Style\n{concept.art_style}\n\n"
        f"## Target Audience\n{concept.target_audience}\n\n"
        f"## Monetization\n{concept.monetization}\n\n"
        f"## Unique Selling Proposition\n{concept.usp}\n"
    )

    return {"concept_md": md}


def evaluate_concept(state: ConceptState):
    """Evaluate the concept for clarity and completeness; request revision if needed."""
    concept_md = state["concept_md"]
    rubric = (
        "Evaluate this video game concept for: clear core loop, concrete mechanics, distinct USP, "
        "coherent progression, feasible monetization. Accept if all are solid and specific; else request revision."
    )
    review = evaluator.invoke(f"{rubric}\n\nCONCEPT:\n{concept_md}")
    return {"decision": review.decision, "feedback": review.feedback}


def route_concept(state: ConceptState):
    """Route to finish on accept; otherwise loop back to generator with feedback."""
    if state["decision"] == "accept":
        return "Accepted"
    else:
        return "Revise"


# Build workflow
builder = StateGraph(ConceptState)
builder.add_node("generate_concept", generate_concept)
builder.add_node("evaluate_concept", evaluate_concept)
builder.add_edge(START, "generate_concept")
builder.add_edge("generate_concept", "evaluate_concept")
builder.add_conditional_edges(
    "evaluate_concept",
    route_concept,
    {
        "Accepted": END,
        "Revise": "generate_concept",
    },
)

concept_workflow = builder.compile()


# Example invocation
if __name__ == "__main__":
    result = concept_workflow.invoke({"idea": "Grand theft auto vice city"})
    print(result["concept_md"])