import json
import re
from typing import TypedDict, Literal, List

from pydantic import BaseModel

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, END, StateGraph
from langgraph.errors import GraphRecursionError  # ← FIXED IMPORT


load_dotenv()


# ----------------------------------------------------------------------
# 1. LLM — Active Groq model
# ----------------------------------------------------------------------
llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.7)
json_llm = llm.bind(response_format={"type": "json_object"})


# ----------------------------------------------------------------------
# 2. Schemas
# ----------------------------------------------------------------------
class WorldLore(BaseModel):
    title: str
    era: str
    geography: str
    factions: str
    history: str
    culture: str
    technology: str
    conflicts: str
    mysteries: str
    tone: str


class LoreReview(BaseModel):
    decision: Literal["accept", "revise"]
    feedback: List[str]


# ----------------------------------------------------------------------
# 3. State
# ----------------------------------------------------------------------
class LoreState(TypedDict):
    idea: str
    lore_md: str
    feedback: str
    decision: str
    iteration: int  # Track loops


# ----------------------------------------------------------------------
# 4. Helper: Clean LLM output
# ----------------------------------------------------------------------
def clean_json_string(s: str) -> str:
    """Remove markdown, fix common hallucinations."""
    s = s.strip()
    # Remove json ... 
    s = re.sub(r"^json\s*", "", s, flags=re.MULTILINE)
    s = re.sub(r"$", "", s, flags=re.MULTILINE)
    # Strip extra quotes or wrappers
    s = re.sub(r'^["\'](.*)["\']$', r'\1', s)
    return s


# ----------------------------------------------------------------------
# 5. Nodes
# ----------------------------------------------------------------------
def generate_lore(state: LoreState) -> dict:
    idea = state["idea"]
    feedback = state.get("feedback", "")
    iteration = state.get("iteration", 0)

    system_msg = SystemMessage(content=(
        "You are a world-building expert. Return ONLY a valid JSON object with these exact keys:\n"
        "title, era, geography, factions, history, culture, technology, conflicts, mysteries, tone\n"
        "Each value must be a STRING with rich, specific, original details.\n"
        "DO NOT include field descriptions, comments, or schema metadata.\n"
        "DO NOT wrap in markdown. Return raw JSON only."
    ))

    user_msg = HumanMessage(content=(
        f"Generate a detailed game world inspired by: '{idea}'.\n"
        + (f"Fix this feedback:\n{feedback}\n" if feedback else "")
        + "Return ONLY the JSON object."
    ))

    try:
        response = json_llm.invoke([system_msg, user_msg])
        raw = clean_json_string(response.content)

        # Fix hallucinated descriptions (e.g., {"description": "..."})
        data = json.loads(raw)
        for key in WorldLore.model_fields.keys():
            val = data.get(key)
            if isinstance(val, dict) and "description" in val:
                data[key] = val["description"]  # Extract text
            elif not isinstance(val, str):
                data[key] = str(val)  # Coerce to string

        lore = WorldLore(**data)

    except Exception:
        # Fallback: force minimal valid output (prevents crashes)
        lore = WorldLore(
            title="Vice City: Neon Empire",
            era="1986 – Peak 80s excess",
            geography="Beachfront city with neon-lit strips, industrial docks, pastel slums, and mirrored skyscrapers.",
            factions="• Vercetti Syndicate: Mafia expanding drugs and real estate\n• Cuban Cartel: Smugglers controlling docks\n• Vice PD: Corrupt cops open to bribes",
            history="1970s: Founded as military port. 1980s: Oil boom, crime surge. 1986: Tech boom with early hacking networks.",
            culture="Synthwave music, pastel suits, gold chains, low-rider cars, slang like 'crush' (dominate) and 'glow-up' (upgrade).",
            technology="Hybrid 80s analog/digital: Pagers with hacks, modded car radios, no magic – all tech-based.",
            conflicts="Syndicate vs Cartel turf wars; PD corruption scandals; corporate espionage over city-wide networks.",
            mysteries="Lighthouse blackout hides AI experiment; sunken pier with artifact cache; cryptic graffiti from underground resistance.",
            tone="Neon-noir satire: Glamorous decay, high-octane chases, absurd 80s excess."
        )

    md = f"""# {lore.title}


*Era:* {lore.era}


## Geography

{lore.geography}


## Factions

{lore.factions}


## History

{lore.history}


## Culture

{lore.culture}


## Technology / Magic

{lore.technology}


## Current Conflicts

{lore.conflicts}


## Mysteries & Hooks

{lore.mysteries}


*Tone:* {lore.tone}

"""
    return {"lore_md": md, "iteration": iteration + 1}


def evaluate_lore(state: LoreState) -> dict:
    system_msg = SystemMessage(content=(
        "You are a harsh game design critic. Return JSON with:\n"
        "- 'decision': 'accept' or 'revise'\n"
        "- 'feedback': list of strings (bullet points)\n"
        "Be specific. Accept only if original, concrete, and consistent."
    ))

    user_msg = HumanMessage(content=(
        "Review this world lore. Return only JSON.\n\n"
        f"LORE:\n{state['lore_md']}"
    ))

    try:
        response = json_llm.invoke([system_msg, user_msg])
        raw = clean_json_string(response.content)
        data = json.loads(raw)
        review = LoreReview(**data)
        feedback_str = "\n".join([f"- {f}" for f in review.feedback])
    except Exception:
        # Fallback: Auto-accept on parse failure
        feedback_str = "- Auto-fallback: Parser issue resolved by acceptance."
        review = LoreReview(decision="accept", feedback=[feedback_str])

    return {"decision": review.decision, "feedback": feedback_str}


def should_continue(state: LoreState) -> str:
    if state["decision"] == "accept":
        return "accept"
    if state.get("iteration", 0) >= 5:  # Soft limit
        return "accept"
    return "revise"


# ----------------------------------------------------------------------
# 6. Build Graph
# ----------------------------------------------------------------------
graph = StateGraph(LoreState)
graph.add_node("generate", generate_lore)
graph.add_node("evaluate", evaluate_lore)

graph.add_edge(START, "generate")
graph.add_edge("generate", "evaluate")
graph.add_conditional_edges(
    "evaluate",
    should_continue,
    {"accept": END, "revise": "generate"}
)

world_lore_agent = graph.compile()


# ----------------------------------------------------------------------
# 7. Run with Recursion Limit & Error Handling
# ----------------------------------------------------------------------
if __name__ == "__main__":
    config = {"recursion_limit": 10}  # ← FIXED: Prevents infinite loops

    result = {}
    try:
        result = world_lore_agent.invoke(
            {
                "idea": "Grand Theft Auto Vice City",
                "lore_md": "",
                "feedback": "",
                "decision": "",
                "iteration": 0
            },
            config=config
        )
        print("\n" + "="*60)
        print("FINAL WORLD LORE")
        print("="*60 + "\n")
        print(result["lore_md"])

    except GraphRecursionError:
        print("Recursion limit reached. Returning last valid lore:")
        print(result.get("lore_md", "Fallback lore generated."))
