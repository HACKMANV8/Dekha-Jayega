"""
Re-export saga with properly sanitized filenames.
This script reads the temporary saga files and exports them properly.
"""
import ast
from pathlib import Path
from SagaAgent.services import ExportService

def main():
    print("="*70)
    print("RE-EXPORTING SAGA WITH FIXED FILENAMES")
    print("="*70)
    
    # Load all saga components
    root = Path("E:/Hackman")
    state = {}
    
    # Load concept
    concept_file = root / "saga_concept.json"
    if concept_file.exists():
        with open(concept_file) as f:
            data = ast.literal_eval(f.read())
            state["concept"] = data if not isinstance(data, dict) or "concept" not in data else data.get("concept")
        print(f"[OK] Loaded concept: {state['concept'].get('title', 'Unknown')}")
    
    # Load world lore
    lore_file = root / "saga_world_lore.json"
    if lore_file.exists():
        with open(lore_file) as f:
            data = ast.literal_eval(f.read())
            state["world_lore"] = data if not isinstance(data, dict) or "world_lore" not in data else data.get("world_lore")
        print(f"[OK] Loaded world lore: {state['world_lore'].get('world_name', 'Unknown')}")
    
    # Load factions
    factions_file = root / "saga_factions.json"
    if factions_file.exists():
        with open(factions_file) as f:
            data = ast.literal_eval(f.read())
            state["factions"] = data if isinstance(data, list) else data.get("factions", [])
        print(f"[OK] Loaded {len(state['factions'])} factions")
    
    # Load characters
    chars_file = root / "saga_characters.json"
    if chars_file.exists():
        with open(chars_file) as f:
            data = ast.literal_eval(f.read())
            state["characters"] = data if isinstance(data, list) else data.get("characters", [])
        print(f"[OK] Loaded {len(state['characters'])} characters")
    
    # Load plot arcs
    plot_file = root / "saga_plot_arcs.json"
    if plot_file.exists():
        with open(plot_file) as f:
            data = ast.literal_eval(f.read())
            state["plot_arcs"] = data if isinstance(data, list) else data.get("plot_arcs", [])
        print(f"[OK] Loaded {len(state['plot_arcs'])} plot arcs")
    
    # Load questlines
    quest_file = root / "saga_questlines.json"
    if quest_file.exists():
        with open(quest_file) as f:
            data = ast.literal_eval(f.read())
            state["questlines"] = data if isinstance(data, list) else data.get("questlines", [])
        print(f"[OK] Loaded {len(state['questlines'])} questlines")
    
    print("\n" + "="*70)
    print("EXPORTING WITH PROPER FILENAMES")
    print("="*70)
    
    # Export all as JSON
    json_result = ExportService.export_all_json(state)
    print(f"\n[OK] JSON files exported to: {json_result['export_path']}")
    for json_file in json_result.get('json_files', []):
        print(f"  - {Path(json_file).name}")
    
    # Export all as Markdown
    md_result = ExportService.export_all_markdown(state)
    print(f"\n[OK] Markdown files exported to: {json_result['export_path']}")
    for md_file in md_result.get('markdown_files', []):
        print(f"  - {Path(md_file).name}")
    
    print("\n" + "="*70)
    print("[SUCCESS] RE-EXPORT COMPLETE!")
    print("="*70)
    print(f"\nYour files are now in: SagaAgent/exports/")
    print(f"With proper names like: San_Andreas_Echoes_of_Liberty_concept_*.json")

if __name__ == "__main__":
    main()

