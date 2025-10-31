# World Lore Agent - LangGraph Workflow
from typing import TypedDict, Literal
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

class WorldLore(BaseModel):
    """Structured world lore document for fictional universes."""
    world_name: str = Field(description="Evocative name for this world or realm.")
    setting_overview: str = Field(description="High-level description: genre, tone, and core concept.")
    
    # Physical World
    geography: str = Field(description="Major continents, regions, terrain, natural barriers, landmarks.")
    climate_cosmology: str = Field(description="Climate zones, celestial bodies, astronomical phenomena.")
    flora_fauna: str = Field(description="Unique creatures, ecosystems, magical beasts, sentient species.")
    
    # History & Timeline
    creation_myth: str = Field(description="Origin story: how the world came to be, creation deities.")
    historical_eras: str = Field(description="Major historical periods, wars, golden ages, cataclysms.")
    current_age: str = Field(description="Present era setting: what's happening now, recent events.")
    
    # Cultural & Social
    civilizations: str = Field(description="Major nations, empires, tribes, city-states and their cultures.")
    social_structures: str = Field(description="Class systems, governance, power distribution, hierarchies.")
    religions_beliefs: str = Field(description="Pantheons, religious systems, spiritual practices, taboos.")
    
    # Systems & Mechanics
    magic_or_technology: str = Field(description="Magic system OR tech level: rules, limitations, accessibility.")
    economy_resources: str = Field(description="Currency, trade, valuable resources, economic systems.")
    conflicts_tensions: str = Field(description="Current wars, political tensions, faction rivalries.")
    
    # Narrative Hooks
    mysteries_legends: str = Field(description="Unsolved mysteries, lost artifacts, legendary locations.")
    story_potential: str = Field(description="Key narrative opportunities and dramatic possibilities.")

class LoreReview(BaseModel):
    """Evaluator review for world lore document."""
    decision: Literal["accept", "revise"] = Field(description="Accept if coherent, rich, and internally consistent; otherwise revise.")
    feedback: str = Field(description="Specific improvements needed: inconsistencies, weak areas, missing depth.")

class LoreState(TypedDict):
    world_prompt: str
    lore_md: str
    feedback: str
    decision: str

# Prepare evaluator
evaluator = llm.with_structured_output(LoreReview, method="json_schema")

def generate_lore(state: LoreState):
    """Generate structured world lore as markdown."""
    world_prompt = state["world_prompt"]
    
    guidance = (
        f"You are a master worldbuilder and game narrative designer. Create rich, internally consistent "
        f"world lore based on: '{world_prompt}'. "
        "Be specific with names, dates, and details. Ensure geography influences culture. "
        "Make conflicts organic and history layered. Avoid generic fantasy tropes."
    )
    
    if state.get("feedback"):
        guidance += f"\n\nIMPORTANT - Address this feedback: {state['feedback']}"
    
    schema = llm.with_structured_output(WorldLore, method="json_schema")
    lore = schema.invoke(guidance)
    
    md = (
        f"# {lore.world_name}\n\n"
        f"**Overview**: {lore.setting_overview}\n\n"
        f"---\n\n"
        f"## Physical World\n\n"
        f"### Geography\n{lore.geography}\n\n"
        f"### Climate & Cosmology\n{lore.climate_cosmology}\n\n"
        f"### Flora & Fauna\n{lore.flora_fauna}\n\n"
        f"---\n\n"
        f"## History & Timeline\n\n"
        f"### Creation Myth\n{lore.creation_myth}\n\n"
        f"### Historical Eras\n{lore.historical_eras}\n\n"
        f"### Current Age\n{lore.current_age}\n\n"
        f"---\n\n"
        f"## Civilizations & Culture\n\n"
        f"### Major Civilizations\n{lore.civilizations}\n\n"
        f"### Social Structures\n{lore.social_structures}\n\n"
        f"### Religions & Beliefs\n{lore.religions_beliefs}\n\n"
        f"---\n\n"
        f"## Systems & Mechanics\n\n"
        f"### Magic or Technology\n{lore.magic_or_technology}\n\n"
        f"### Economy & Resources\n{lore.economy_resources}\n\n"
        f"### Conflicts & Tensions\n{lore.conflicts_tensions}\n\n"
        f"---\n\n"
        f"## Narrative Elements\n\n"
        f"### Mysteries & Legends\n{lore.mysteries_legends}\n\n"
        f"### Story Potential\n{lore.story_potential}\n"
    )
    
    return {"lore_md": md}

def evaluate_lore(state: LoreState):
    """Evaluate world lore for consistency, depth, and narrative richness."""
    lore_md = state["lore_md"]
    rubric = (
        "Evaluate this world lore for:\n"
        "1. Internal consistency (geography→culture→history alignment)\n"
        "2. Specificity (proper names, concrete details vs generic descriptions)\n"
        "3. Depth (layered history, organic conflicts, believable systems)\n"
        "4. Narrative potential (hooks, mysteries, dramatic opportunities)\n"
        "5. Originality (avoids clichés, has unique elements)\n\n"
        "Accept if all criteria are strong. Otherwise, provide specific revision guidance."
    )
    review = evaluator.invoke(f"{rubric}\n\nWORLD LORE:\n{lore_md}")
    return {"decision": review.decision, "feedback": review.feedback}

def route_lore(state: LoreState):
    """Route to finish on accept; loop back with feedback to revise."""
    if state["decision"] == "accept":
        return "Accepted"
    else:
        return "Revise"

# Build workflow
builder = StateGraph(LoreState)
builder.add_node("generate_lore", generate_lore)
builder.add_node("evaluate_lore", evaluate_lore)
builder.add_edge(START, "generate_lore")
builder.add_edge("generate_lore", "evaluate_lore")
builder.add_conditional_edges(
    "evaluate_lore",
    route_lore,
    {
        "Accepted": END,
        "Revise": "generate_lore",
    },
)

lore_workflow = builder.compile()

# Example invocations
if __name__ == "__main__":
    # Example 1: Fantasy world
    result1 = lore_workflow.invoke({
        "world_prompt": "A dying desert world where water is currency and ancient machines control oases"
    })
    print(result1["lore_md"])
    print("\n" + "="*80 + "\n")
    
    # Example 2: Sci-fi world
    result2 = lore_workflow.invoke({
        "world_prompt": "Post-singularity solar system where uploaded consciousness fight over computing substrate"
    })
    print(result2["lore_md"])
